#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mediafilecleaner.py

Detect the end of the first ad block at the beginning of a podcast audio.

Heuristic:
1) Analyze the first N seconds from start.
2) Detect silences with pydub.
3) Pick the first silence whose NEXT non-silent interval lasts >= min_content_sec.
   -> return silence_end as "ad end" timestamp (in seconds).
If nothing matches, fallback to the longest silence after warmup_sec.

CLI:
  python mediafilecleaner.py /path/file.mp3 \
    --seconds 180 --min-silence-ms 600 --silence-db-offset 14 \
    --min-content-sec 20 --warmup-sec 10 [--json] [--trim-output OUTFILE] [--silence-pad-ms 0]

Requirements:
- ffmpeg must be available on PATH (pydub backend).
- pip install pydub

References:
- pydub silence detection: https://github.com/jiaaro/pydub
- ffmpeg: https://ffmpeg.org/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional, Tuple, List

from pydub import AudioSegment, silence


class MediaFileCleaner:
    """Helper for ad-boundary detection and optional trimming."""

    @staticmethod
    def fmt_hhmmss(seconds: float) -> str:
        """Format seconds as HH:MM:SS.

        Args:
            seconds: Time in seconds.

        Returns:
            Formatted string "HH:MM:SS".
        """
        s = int(round(seconds))
        h, rem = divmod(s, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02}:{m:02}:{s:02}"

    @staticmethod
    def detect_ads_end(
        file_path: str,
        seconds: int = 180,
        min_silence_ms: int = 600,
        silence_db_offset: int = 14,
        min_content_sec: int = 20,
        warmup_sec: int = 10
    ) -> Optional[float]:
        """Detect the end of the first ad block at the start of an audio file.

        Args:
            file_path: Input audio file (mp3, m4a, wav... supported by ffmpeg).
            seconds: Analysis window from start (seconds).
            min_silence_ms: Minimum silence duration to consider (ms).
            silence_db_offset: Silence threshold = segment.dBFS - silence_db_offset.
            min_content_sec: Minimal continuous non-silent duration right after a candidate silence.
            warmup_sec: Ignore decisions before this time to avoid micro-breaths / jingles.

        Returns:
            Ad-end timestamp (seconds from start) or None if not found/reliable.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        if seconds <= 0:
            raise ValueError("--seconds must be > 0")

        audio = AudioSegment.from_file(file_path)
        window = audio[: seconds * 1000]

        # Detect [start_ms, end_ms] silent intervals in the analysis window
        silences: List[Tuple[int, int]] = silence.detect_silence(
            window,
            min_silence_len=min_silence_ms,
            silence_thresh=window.dBFS - silence_db_offset
        )

        if not silences:
            return None

        # Build non-silent intervals between silences
        # Timeline: 0 ---- [s0,e0] ---- [s1,e1] ---- ... ---- end
        # Non-silent segments: [0,s0], [e0,s1], ..., [eN, end]
        non_silent_segments: List[Tuple[int, int]] = []
        prev_end = 0
        for start, end in silences:
            if start > prev_end:
                non_silent_segments.append((prev_end, start))
            prev_end = end
        if prev_end < len(window):
            non_silent_segments.append((prev_end, len(window)))

        # Heuristic: first silence whose NEXT non-silent duration is long enough,
        # and whose silence end is after warmup_sec.
        for (start, end) in silences:
            next_seg = None
            for (ns, ne) in non_silent_segments:
                if ns >= end:
                    next_seg = (ns, ne)
                    break
            if next_seg is None:
                continue

            dur_next = (next_seg[1] - next_seg[0]) / 1000.0
            ad_end_sec = end / 1000.0
            if ad_end_sec >= warmup_sec and dur_next >= min_content_sec:
                return ad_end_sec

        # Fallback: choose the end of the longest silence after warmup
        longest: Optional[Tuple[int, int]] = None
        for (start, end) in silences:
            if (end / 1000.0) >= warmup_sec:
                if longest is None:
                    longest = (start, end)
                elif (end - start) > (longest[1] - longest[0]):
                    longest = (start, end)

        return (longest[1] / 1000.0) if longest else None

    @staticmethod
    def trim_from(
        file_path: str,
        start_seconds: float,
        out_path: str,
    ) -> None:
        """Save a trimmed copy of the file starting at `start_seconds`.

        Args:
            file_path: Input audio file.
            start_seconds: Start offset in seconds.
            out_path: Output file path (extension decides the format).

        Raises:
            ValueError: If start_seconds is invalid.
        """
        if start_seconds < 0:
            raise ValueError("start_seconds must be >= 0")

        audio = AudioSegment.from_file(file_path)
        start_ms = int(start_seconds * 1000)
        if start_ms >= len(audio):
            raise ValueError("start_seconds beyond audio length")

        trimmed = audio[start_ms:]
        # Determine export format from output extension
        _, ext = os.path.splitext(out_path)
        fmt = ext.lstrip(".").lower() or "mp3"
        trimmed.export(out_path, format=fmt)


def _main() -> int:

    """Command-line interface for ad-end detection and optional trimming."""
    ap = argparse.ArgumentParser(
        description="Detect end of first ad block at start of a podcast audio."
    )
    ap.add_argument(
        "file", 
        help="Input audio file (e.g., .mp3)"
    )
    ap.add_argument(
        "--seconds", 
        type=int,
        default=180,
        help="Analysis window in seconds (default: 180)"
    )
    ap.add_argument(
        "--min-silence-ms", 
        type=int,
        default=600,
        help="Min silence length in ms (default: 600)"
    )
    ap.add_argument(
        "--silence-db-offset", 
        type=int,
        default=14,
        help="Silence threshold offset in dBFS (default: 14)"
    )
    ap.add_argument(
        "--min-content-sec", 
        type=int,
        default=20,
        help="Min content length after ad in sec (default: 20)"
    )
    ap.add_argument(
        "--warmup-sec", 
        type=int,
        default=10,
        help="Ignore decisions before this time in sec (default: 10)"
    )
    ap.add_argument(
        "--json", 
        action="store_true",
        help="Output machine-readable JSON"
    )
    ap.add_argument(
        "--trim-output", 
        help="If set, write a trimmed file starting at detected ad end (e.g., output.mp3)"
    )
    ap.add_argument(
        "--silence-pad-ms", 
        type=int,
        default=0,
        help="Extra pad after ad end before trimming (ms)"
    )
    args = ap.parse_args()

    try:
        t = MediaFileCleaner.detect_ads_end(
            file_path=args.file,
            seconds=args.seconds,
            min_silence_ms=args.min_silence_ms,
            silence_db_offset=args.silence_db_offset,
            min_content_sec=args.min_content_sec,
            warmup_sec=args.warmup_sec
        )
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if args.json:
        payload = {"ad_end_seconds": t, "ad_end_hhmmss": None}
        if t is not None:
            payload["ad_end_hhmmss"] = MediaFileCleaner.fmt_hhmmss(t)
        print(json.dumps(payload, ensure_ascii=False))
    else:
        if t is None:
            print("No reliable ad-end point found in the analysis window.")
        else:
            print(f"Ad end ≈ {t:.3f} s ({MediaFileCleaner.fmt_hhmmss(t)})")

    # Optional trimming step
    if args.trim_output and t is not None:
        pad_s = max(0, args.silence_pad_ms) / 1000.0
        start_s = t + pad_s
        try:
            MediaFileCleaner.trim_from(args.file, start_s, args.trim_output)
            print(f"Wrote trimmed file: {args.trim_output} (from {start_s:.3f}s)")
        except (FileNotFoundError, ValueError, OSError) as e:
            print(f"Trim error: {e}", file=sys.stderr)
            return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
