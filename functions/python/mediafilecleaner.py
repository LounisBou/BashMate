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
    [--seconds 180] [--min-silence-ms 600] [--silence-db-offset 14] \
    [--min-content-sec 20] [--warmup-sec 10] [--json] [--trim-output OUTFILE] \
    [--silence-pad-ms 0] [--dry-run]

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

    # Constants
    MEDIA_FILE_EXTENSIONS = {".mp3", ".m4a", ".wav",
                             ".flac", ".ogg", ".opus", ".wma", ".aac"}
    DEFAULT_ANALYSIS_WINDOW_SEC = 180       # analyze first 3 minutes
    DEFAULT_MIN_SILENCE_MS = 500            # min silence length in ms
    DEFAULT_SILENCE_DB_OFFSET = 18          # dBFS offset for silence threshold
    DEFAULT_WARMUP_SEC = 10                 # warmup time before detecting ads
    DEFAULT_MERGE_GAP_MS = 1200             # max gap to merge silences
    DEFAULT_SILENT_PAD_MS = 0               # silence padding for output
    DEFAULT_POST_CHECK_SEC = 3              # short window to confirm content resumes
    DEFAULT_FALLBACK_MIN_CONTENT_SEC = 8    # min content length for fallback

    @staticmethod
    def format_to_time(seconds: float) -> str:
        """Format seconds as HH:MM:SS. for display purposes.

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
        seconds: int = DEFAULT_ANALYSIS_WINDOW_SEC,
        min_silence_ms: int = DEFAULT_MIN_SILENCE_MS,
        silence_db_offset: int = DEFAULT_SILENCE_DB_OFFSET,
        warmup_sec: int = DEFAULT_WARMUP_SEC,
        merge_gap_ms: int = DEFAULT_MERGE_GAP_MS,
        post_check_sec: int = DEFAULT_POST_CHECK_SEC,
        fallback_min_content_sec: int = DEFAULT_FALLBACK_MIN_CONTENT_SEC
    ) -> float | None:
        """
        Detect the end of the first ad block at the start of a podcast audio file.
        
        Args:
            file_path: Input audio file.
            seconds: Analysis window in seconds from start.
            min_silence_ms: Minimum silence length in ms.
            silence_db_offset: Silence threshold offset in dBFS.
            warmup_sec: Ignore decisions before this time in sec.
            merge_gap_ms: Merge silences separated by gaps <= this in ms.
            post_check_sec: Short window to confirm content resumes after silence.
            fallback_min_content_sec: Min content length for fallback in sec.
        Returns:
            Detected ad-end time in seconds, or None if not found.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        if seconds <= 0:
            raise ValueError("--seconds must be > 0")

        audio = AudioSegment.from_file(file_path)
        window = audio[: seconds * 1000]

        # 1) Raw silence detection
        silences = silence.detect_silence(
            window,
            min_silence_len=min_silence_ms,
            silence_thresh=window.dBFS - silence_db_offset,
            # seek_step=10  # uncomment if you need speed with large files
        )
        if not silences:
            return None

        # 2) Merge adjacent silences separated by tiny non-silent gaps
        if merge_gap_ms and merge_gap_ms > 0 and len(silences) > 1:
            merged = []
            cur_s, cur_e = silences[0]
            for silence_start, silence_end in silences[1:]:
                if silence_start - cur_e <= merge_gap_ms:
                    cur_e = max(cur_e, silence_end)
                else:
                    merged.append((cur_s, cur_e))
                    cur_s, cur_e = silence_start, silence_end
            merged.append((cur_s, cur_e))
            silences = merged

        # Helper to check if short post window is "not silence" on average
        def is_post_window_contentful(end_ms: int) -> bool:
            start = end_ms
            stop = min(end_ms + post_check_sec * 1000, len(window))
            if stop <= start:
                return False
            segment = window[start:stop]
            # Consider contentful if average dBFS is noticeably above silence threshold
            # We compare to (window.dBFS - silence_db_offset + 3 dB) as a margin
            try:
                return segment.dBFS > (window.dBFS - silence_db_offset + 3)
            except (AttributeError, ValueError):
                return False

        # 3) Primary rule: earliest plausible silence-end where content actually resumes
        for (silence_start, silence_end) in silences:
            ad_end_sec = silence_end / 1000.0
            if ad_end_sec < warmup_sec:
                continue
            if is_post_window_contentful(silence_end):
                return ad_end_sec

        # 4) Fallback: choose the end of the longest silence after warmup,
        #    but require at least a small sustained non-silent afterward
        #    (fallback_min_content_sec) to avoid returning dead air.
        # Build non-silent segments for fallback only
        non_silent_segments = []
        prev_end = 0
        for silence_start, silence_end in silences:
            if silence_start > prev_end:
                non_silent_segments.append((prev_end, silence_start))
            prev_end = silence_end
        if prev_end < len(window):
            non_silent_segments.append((prev_end, len(window)))

        longest_silence: Optional[Tuple[int, int]] = None
        for (silence_start, silence_end) in silences:
            if (silence_end / 1000.0) >= warmup_sec:
                if longest_silence is None:
                    longest_silence = (silence_start, silence_end)
                elif (silence_end - silence_start) > (longest_silence[1] - longest_silence[0]):
                    longest_silence = (silence_start, silence_end)

        if longest_silence:
            longest_silence_end = longest_silence[1]
            # ensure there's some content after
            for (non_silent_start, non_silent_end) in non_silent_segments:
                if non_silent_start >= longest_silence_end and (non_silent_end - non_silent_start) / 1000.0 >= fallback_min_content_sec:
                    return longest_silence_end / 1000.0

        return None

    @staticmethod
    def trim_from(
        file_path: str,
        start_seconds: float,
        out_path: str,
    ) -> None:
        """
        Save a trimmed copy of the file starting at `start_seconds`.
        Output format is always the same as the original file.

        Args:
            file_path: Input audio file.
            start_seconds: Start offset in seconds.
            out_path: Output directory path (extension decides the format).

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
        # Determine file name and extension
        _, base_name = os.path.split(file_path)
        name, ext = os.path.splitext(base_name)
        if ext.lower() not in MediaFileCleaner.MEDIA_FILE_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {ext}")
        # Determine output format from extension
        fmt = ext.lstrip(".").lower() or "mp3"

        # Export trimmed audio to out_path directory using original file name
        trimmed.export(os.path.join(out_path, f"{name}{ext}"), format=fmt)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    Returns:
        Parsed arguments.
    Raises:
        SystemExit: If parsing fails.
    """
    ap = argparse.ArgumentParser(
        description="Detect end of first ad block at start of a podcast audio."
    )
    ap.add_argument(
        "file_or_path",
        help=f"Input media file or directory path (supported: {', '.join(sorted(MediaFileCleaner.MEDIA_FILE_EXTENSIONS))})"
    )
    ap.add_argument(
        "--seconds",
        type=int,
        default=MediaFileCleaner.DEFAULT_ANALYSIS_WINDOW_SEC,
        help=f"Analysis window in seconds (default: {MediaFileCleaner.DEFAULT_ANALYSIS_WINDOW_SEC})"
    )
    ap.add_argument(
        "--min-silence-ms",
        type=int,
        default=MediaFileCleaner.DEFAULT_MIN_SILENCE_MS,
        help=f"Min silence length in ms (default: {MediaFileCleaner.DEFAULT_MIN_SILENCE_MS})"
    )
    ap.add_argument(
        "--silence-db-offset",
        type=int,
        default=MediaFileCleaner.DEFAULT_SILENCE_DB_OFFSET,
        help=f"Silence threshold offset in dBFS (default: {MediaFileCleaner.DEFAULT_SILENCE_DB_OFFSET})"
    )
    ap.add_argument(
        "--warmup-sec",
        type=int,
        default=MediaFileCleaner.DEFAULT_WARMUP_SEC,
        help=f"Ignore decisions before this time in sec (default: {MediaFileCleaner.DEFAULT_WARMUP_SEC})"
    )
    ap.add_argument(
        "--merge-gap-ms", 
        type=int,
        default=MediaFileCleaner.DEFAULT_MERGE_GAP_MS,
        help=f"Merge silences separated by gaps <= this in ms (default: {MediaFileCleaner.DEFAULT_MERGE_GAP_MS})"   
    )
    ap.add_argument(
        "--post-check-sec", 
        type=int,
        default=MediaFileCleaner.DEFAULT_POST_CHECK_SEC,
        help=f"Short window to confirm content resumes after silence (default: {MediaFileCleaner.DEFAULT_POST_CHECK_SEC})"   
    )
    ap.add_argument(
        "--fallback-min-content-sec",
        type=int,
        default=MediaFileCleaner.DEFAULT_FALLBACK_MIN_CONTENT_SEC,
        help=f"Min content length for fallback in sec (default: {MediaFileCleaner.DEFAULT_FALLBACK_MIN_CONTENT_SEC})"   
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON"
    )
    ap.add_argument(
        "--trim-output-path",
        type=str,
        default=None,
        help="Path directory to save trimmed output (default: <file_to_trim_path>/trimmed)"
    )
    ap.add_argument(
        "--silence-pad-ms",
        type=int,
        default=MediaFileCleaner.DEFAULT_SILENT_PAD_MS,
        help="Extra pad after ad end before trimming (ms)"
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform analysis without trimming files"
    )
    return ap.parse_args()


def check_args(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments.
    Args:
        args: Parsed arguments.
    Raises:
        ValueError: If any argument is invalid.
    """
    if not os.path.exists(args.file_or_path):
        raise FileNotFoundError(f"Input path not found: {args.file_or_path}")
    if not os.path.isdir(args.file_or_path) and not os.path.isfile(args.file_or_path):
        raise FileNotFoundError(f"Input path is neither a file nor a directory: {args.file_or_path}")
    if os.path.isfile(args.file_or_path):
        _, ext = os.path.splitext(args.file_or_path)
        if ext.lower() not in MediaFileCleaner.MEDIA_FILE_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {ext}")
    if args.trim_output_path is not None:
        if not os.path.isdir(args.trim_output_path):
            try:
                os.makedirs(args.trim_output_path, exist_ok=True)
            except OSError as e:
                raise ValueError(f"Cannot create output directory: {args.trim_output_path}") from e
    if args.seconds <= 0:
        raise ValueError("--seconds must be > 0")
    if args.min_silence_ms <= 0:
        raise ValueError("--min-silence-ms must be > 0")
    if args.warmup_sec < 0:
        raise ValueError("--warmup-sec must be >= 0")
    if args.silence_pad_ms < 0:
        raise ValueError("--silence-pad-ms must be >= 0")
    if args.merge_gap_ms < 0:
        raise ValueError("--merge-gap-ms must be >= 0")
    if args.post_check_sec < 0:
        raise ValueError("--post-check-sec must be >= 0")
    if args.fallback_min_content_sec < 0:
        raise ValueError("--fallback-min-content-sec must be >= 0")


def set_default_args_values(args: argparse.Namespace) -> None:
    """
    Set default values for optional arguments if not provided.

    Args:
        args: Parsed arguments.
    """

    # Default trimmed output : <input_dir>/trimmed
    if args.trim_output_path is None and os.path.isfile(args.file_or_path):
        in_dir, _ = os.path.split(args.file_or_path)
        out_dir = os.path.join(in_dir, "trimmed")
        args.trim_output_path = out_dir
    elif args.trim_output_path is None and os.path.isdir(args.file_or_path):
        args.trim_output_path = os.path.join(args.file_or_path, "trimmed")


def define_files_to_process(args: argparse.Namespace) -> List[str]:
    """
    Define the list of files to process based on input path.

    Args:
        args: Parsed arguments.

    Returns:
        List of file paths to process.
    """
    if os.path.isdir(args.file_or_path):
        files_to_process = []
        for entry in os.listdir(args.file_or_path):
            full_path = os.path.join(args.file_or_path, entry)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(entry)
                if ext.lower() in MediaFileCleaner.MEDIA_FILE_EXTENSIONS:
                    files_to_process.append(full_path)
        if not files_to_process:
            raise FileNotFoundError(
                f"No supported media files found in directory: {args.file_or_path}")
        return files_to_process
    else:
        return [args.file_or_path]


def _main() -> int:
    """
    Command-line interface for ad-end detection and trimming.
    """

    # Parse arguments
    args = parse_args()
    
    # Set default values and validate args
    set_default_args_values(args)

    # Set default values and validate args
    try:
        check_args(args)
    except (FileNotFoundError, ValueError) as e:
        print(f"Argument error: {e}", file=sys.stderr)
        return 1
    set_default_args_values(args)

    # Define files to process
    files_to_process = define_files_to_process(args)
    
    # Check dry-run mode
    if args.dry_run:
        print("Dry-run mode: No files will be trimmed.")
    
    # Process each file
    for file_path in files_to_process:
        print(f"Processing file: {file_path}")
        try:
            ads_duration = MediaFileCleaner.detect_ads_end(
                file_path,
                seconds=args.seconds,
                min_silence_ms=args.min_silence_ms,
                silence_db_offset=args.silence_db_offset,
                warmup_sec=args.warmup_sec,
                merge_gap_ms=args.merge_gap_ms,
                post_check_sec=args.post_check_sec,
                fallback_min_content_sec=args.fallback_min_content_sec
            )
        except (FileNotFoundError, ValueError, OSError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

        if args.json:
            payload = {"ad_end_seconds": ads_duration, "ad_end_hhmmss": None}
            if ads_duration is not None:
                payload["ad_end_hhmmss"] = MediaFileCleaner.format_to_time(
                    ads_duration)
            print(json.dumps(payload, ensure_ascii=False))
        else:
            if ads_duration is None:
                print("No reliable ad-end point found in the analysis window.")
            else:
                print(
                    f"Ads end ≈ {ads_duration:.3f} s ({MediaFileCleaner.format_to_time(ads_duration)})")

        # Calculate start time with optional padding
        pad_s = max(0, args.silence_pad_ms) / 1000.0
        start_s = ads_duration + pad_s
        # Determine trimmed file path
        trimmed_path = os.path.join(args.trim_output_path, os.path.basename(file_path))
        
        # Trim the file
        if not args.dry_run:
            if ads_duration is not None:
                try:
                    MediaFileCleaner.trim_from(
                        file_path,
                        start_s,
                        args.trim_output_path
                    )
                    print(
                        f"Wrote trimmed file: {trimmed_path!r} (from {start_s:.3f}s)")
                except (FileNotFoundError, ValueError, OSError) as e:
                    print(f"Trim error: {e}", file=sys.stderr)
                    return 3
        else:
            print(
                f"Trimmed file would be saved to: {trimmed_path!r} (from {start_s:.3f}s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
