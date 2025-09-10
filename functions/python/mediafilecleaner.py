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
    [--intro-sample intro.mp3] [--intro-sample-rate 22050] [--intro-threshold 0.35] \
    [--intro-trim-db 30.0] [--analysis_window_seconds 180] [--min-silence-ms 600] [--silence-db-offset 14] \
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
from typing import Optional, Tuple, List, Union

from pydub import AudioSegment, silence
import numpy as np
import librosa

class MediaFileCleaner:
    """Helper for ad-boundary detection and optional trimming."""

    # Constants
    MEDIA_FILE_EXTENSIONS = {".mp3", ".m4a", ".wav",
                             ".flac", ".ogg", ".opus", ".wma", ".aac"}
    DEFAULT_ANALYSIS_WINDOW_SEC = 180               # analyze first 3 minutes
    DEFAULT_MIN_SILENCE_MS = 500                    # min silence length in ms
    DEFAULT_SILENCE_DB_OFFSET = 18                  # dBFS offset for silence threshold
    DEFAULT_WARMUP_SEC = 10                         # warmup time before detecting ads
    DEFAULT_MERGE_GAP_MS = 1200                     # max gap to merge silences
    DEFAULT_SILENT_PAD_MS = 0                       # silence padding for output
    DEFAULT_POST_CHECK_SEC = 3                      # short window to confirm content resumes
    DEFAULT_FALLBACK_MIN_CONTENT_SEC = 8            # min content length for fallback

    DEFAULT_INTRO_SAMPLE = "intro_sample.mp3"       # default intro sample file
    DEFAULT_INTRO_MATCH_THRESHOLD = 0.35             # default intro match threshold
    DEFAULT_INTRO_SAMPLE_RATE = 22050                # default sample rate for intro matching
    DEFAULT_INTRO_TRIM_DB = 30.0                     # default trim dB for intro sample

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
    def parse_timecode(time_code: Union[str, float, int]) -> float:
        """
        Parse timecode to seconds (float).
        Accepts: "SS", "MM:SS", "HH:MM:SS", each optionally with .mmm
                or numeric seconds (int/float).
                
        Args:
            time_code: Timecode as string or numeric seconds.
        Returns:
            Time in seconds as float.
        Raises:
            ValueError: On invalid format.
        """
        if isinstance(time_code, (int, float)):
            return float(time_code)
        s = time_code.strip()
        parts = s.split(":")
        if len(parts) == 1:
            return float(parts[0])
        if len(parts) == 2:
            m, sec = parts
            return float(m) * 60 + float(sec)
        if len(parts) == 3:
            h, m, sec = parts
            return float(h) * 3600 + float(m) * 60 + float(sec)
        raise ValueError(f"Invalid timecode: {time_code!r}")

    @staticmethod
    def detect_ads_end(
        file_path: str,
        analysis_window_seconds: int = DEFAULT_ANALYSIS_WINDOW_SEC,
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
        if analysis_window_seconds <= 0:
            raise ValueError("--seconds must be > 0")

        audio = AudioSegment.from_file(file_path)
        window = audio[: analysis_window_seconds * 1000]

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
    def detect_intro(
        file_path: str,
        intro_sample: str = DEFAULT_INTRO_SAMPLE,
        sample_rate: int = DEFAULT_INTRO_SAMPLE_RATE,
        threshold: float = DEFAULT_INTRO_MATCH_THRESHOLD,
        trim_sample_db: float = DEFAULT_INTRO_TRIM_DB,
    ) -> float | None:
        """
        Try to find `intro_sample` inside `file_path` using normalized cross-correlation over waveforms.
        Returns start time (seconds) if match score >= threshold, else None.

        Args:
            file_path: Target media (podcast episode).
            intro_sample: Audio file containing the intro excerpt to search for.
            sample_rate: Resample rate for analysis (mono).
            threshold: Match threshold in [0, 1]. Typical 0.30–0.50. Increase to reduce false positives.
            trim_sample_db: Trim leading/trailing silence from sample (librosa.effects.trim top_db).

        Notes:
            - Works best if the sample is the *clean* intro (same mix). If heavy EQ/compression differs,
              consider a feature-based approach (e.g., chroma) as a next step.
        """
        # 1) Load target and sample (mono, same sampling rate)
        x, _ = librosa.load(file_path, sr=sample_rate, mono=True)
        y, _ = librosa.load(intro_sample, sr=sample_rate, mono=True)

        # Guard: sample longer than target
        if len(y) == 0 or len(y) > len(x):
            return None

        # 2) Trim silence on the sample to make matching sharper
        y, _ = librosa.effects.trim(y, top_db=trim_sample_db)
        m = len(y)
        if m < int(0.2 * sample_rate):  # too short (<~200ms) -> unreliable
            return None

        # 3) Zero-mean, unit-variance the template (sample)
        y_mean = y.mean()
        y_std = y.std() + 1e-9
        y0 = (y - y_mean) / y_std

        # 4) Precompute sliding window stats of x (for normalized correlation)
        n = len(x)
        if n < m:
            return None

        # cumulative sums for fast window mean/std
        csum = np.concatenate(([0.0], np.cumsum(x)))
        csum2 = np.concatenate(([0.0], np.cumsum(x * x)))

        # convolution for numerator: sum(x_k * y0)
        sxy = np.convolve(x, y0[::-1], mode="valid")  # length n - m + 1

        # per-window std of x
        # mean_xk = sum_x / m ; var_xk = E[x^2] - mean^2
        sum_x = csum[m:] - csum[:-m]                        # shape (n - m + 1,)
        sum_x2 = csum2[m:] - csum2[:-m]
        mean_x = sum_x / m
        var_x = (sum_x2 / m) - (mean_x * mean_x)
        std_x = np.sqrt(np.maximum(var_x, 1e-12))

        # ZNCC: r[k] = sum( (xk - mean_xk)*(y - mean_y) ) / (m*std_xk*std_y)
        # With y0 normalized to zero-mean and unit-std:
        # r[k] = sum( xk * y0 ) / (m * std_xk)
        r = sxy / (m * std_x)

        # 5) Find best match
        k = int(np.argmax(r))
        score = float(r[k])

        if score < threshold:
            return None

        # Start time in seconds
        start_sec = k / float(sample_rate)
        return start_sec

    @staticmethod
    def extract_intro_sample(
        file_path: str,
        start_timecode: Union[str, float, int],
        end_timecode:   Union[str, float, int],
        out_path: str = None,
    ) -> str:
        """
        Extract a segment [start, end) from `file_path` and save to `out_path`.

        Args:
            file_path: Input media (mp3/m4a/wav… supported by ffmpeg).
            start_timecode: Start (e.g., "00:00:05.250" or 5.25).
            end_timecode:   End   (e.g., "00:00:12.000" or 12.0).
            out_path:  Output file path; format inferred from extension. If None, defaults to "intro_sample.mp3" in file dir.
        Returns:
            The absolute output path as a string (URI can be built by caller).

        Raises:
            ValueError: On invalid bounds or empty segment.
            FileNotFoundError: If input does not exist.
        """
        
        # Set output path by default if not provided
        if out_path is None:
            out_path = os.path.join(os.path.dirname(file_path), MediaFileCleaner.DEFAULT_INTRO_SAMPLE)
            
        # Define absolute paths
        out_path = os.path.abspath(out_path)
        in_path = os.path.abspath(file_path)
        
        # Check input file exists
        if not os.path.isfile(in_path):
            raise FileNotFoundError(f"Input not found: {file_path}")
        
        # Parse timecodes
        start_second = MediaFileCleaner.parse_timecode(start_timecode)
        end_second = MediaFileCleaner.parse_timecode(end_timecode)
        if start_second < 0 or end_second <= 0 or end_second <= start_second:
            raise ValueError(f"Invalid range: start={start_second}s, end={end_second}s")

        # Load audio
        audio = AudioSegment.from_file(str(in_path))
        
        # Convert to ms and clamp to audio length
        start_ms = int(round(start_second * 1000))
        end_ms   = int(round(end_second   * 1000))
        if start_ms >= len(audio):
            raise ValueError("Start is beyond audio length.")
        end_ms = min(end_ms, len(audio))
        if end_ms - start_ms <= 0:
            raise ValueError("Empty segment after clamping.")

        # Extract segment
        segment = audio[start_ms:end_ms]
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        # Export using format inferred from extension (default mp3)
        fmt = (os.path.splitext(out_path)[1][1:].lower() or "mp3") if os.path.splitext(out_path)[1] else "mp3"
        segment.export(str(out_path), format=fmt)

        return str(out_path.resolve())

    @staticmethod
    def get_trim_duration(
        file_path: str,
        intro_sample: str | None = None,
        sample_rate: int = DEFAULT_INTRO_SAMPLE_RATE,
        threshold: float = DEFAULT_INTRO_MATCH_THRESHOLD,
        trim_sample_db: float = DEFAULT_INTRO_TRIM_DB,
        analysis_window_seconds: int = DEFAULT_ANALYSIS_WINDOW_SEC,
        min_silence_ms: int = DEFAULT_MIN_SILENCE_MS,
        silence_db_offset: int = DEFAULT_SILENCE_DB_OFFSET,
        warmup_sec: int = DEFAULT_WARMUP_SEC,
        merge_gap_ms: int = DEFAULT_MERGE_GAP_MS,
        post_check_sec: int = DEFAULT_POST_CHECK_SEC,
        fallback_min_content_sec: int = DEFAULT_FALLBACK_MIN_CONTENT_SEC
        
    ) -> float | None:
        """
        Get the duration (in seconds) to trim from the start of the file.
        Try different methods in order:
            1) Intro sample matching (if sample provided).
            2) Ad-end detection heuristic.
        Return None if no method works.
        
        Args:
            file_path: Input audio file.
        Returns:
            Duration in seconds to trim from start, or None if duration detection fails.
        """
        
        # Check if sample intro file exists
        if intro_sample is not None and os.path.isfile(intro_sample):
            intro_start = MediaFileCleaner.detect_intro(
                file_path,
                intro_sample=intro_sample,
                sample_rate=sample_rate,
                threshold=threshold,
                trim_sample_db=trim_sample_db,
            )
            if intro_start is not None:
                return intro_start
        else:
            print("No")
        
        # Fallback to ad-end detection heuristic
        try:
            ad_end = MediaFileCleaner.detect_ads_end(
                file_path,
                analysis_window_seconds=analysis_window_seconds,
                min_silence_ms=min_silence_ms,
                silence_db_offset=silence_db_offset,
                warmup_sec=warmup_sec,
                merge_gap_ms=merge_gap_ms,
                post_check_sec=post_check_sec,
                fallback_min_content_sec=fallback_min_content_sec
            )
            if ad_end is not None:
                return ad_end
        except (FileNotFoundError, ValueError, OSError):
            pass
        
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
        "--intro-sample",
        type=str,
        default=None,
        help="Path to intro sample audio file for matching (optional)"
    )
    ap.add_argument(
        "--intro-sample-rate",
        type=int,
        default=MediaFileCleaner.DEFAULT_INTRO_SAMPLE_RATE,
        help=f"Sample rate for intro matching (default: {MediaFileCleaner.DEFAULT_INTRO_SAMPLE_RATE})"
    )
    ap.add_argument(
        "--intro-threshold",
        type=float,
        default=MediaFileCleaner.DEFAULT_INTRO_MATCH_THRESHOLD,
        help=f"Threshold for intro matching (default: {MediaFileCleaner.DEFAULT_INTRO_MATCH_THRESHOLD})"
    )
    ap.add_argument(
        "--intro-trim-db",
        type=float,
        default=MediaFileCleaner.DEFAULT_INTRO_TRIM_DB,
        help=f"Trim silence below this dBFS for intro (default: {MediaFileCleaner.DEFAULT_INTRO_TRIM_DB})"
    )
    ap.add_argument(
        "--analysis-window-seconds",
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
    # Required arguments validation
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
            
    # Optionals arguments validation
    if args.intro_sample is not None and not os.path.isfile(args.intro_sample):
        args.intro_sample = None  # Ignore if not found
    if args.intro_sample_rate <= 0:
        raise ValueError("--intro-sample-rate must be > 0")
    if not (0.0 < args.intro_threshold < 1.0):
        raise ValueError("--intro-threshold must be in (0.0, 1.0)")
    if args.intro_trim_db < 0.0:
        raise ValueError("--intro-trim-db must be >= 0.0")
    if args.analysis_window_seconds <= 0:
        raise ValueError("--analysis-window-seconds must be > 0")
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

    # Default intro sample : <input_dir>/intro_sample.mp3
    if args.intro_sample is None:
        args.intro_sample = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            MediaFileCleaner.DEFAULT_INTRO_SAMPLE
        )

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
            trim_duration = MediaFileCleaner.get_trim_duration(
                file_path,
                intro_sample=args.intro_sample,
                sample_rate=args.intro_sample_rate,
                threshold=args.intro_threshold,
                trim_sample_db=args.intro_trim_db,
                analysis_window_seconds=args.analysis_window_seconds,
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
            payload = {"ad_end_seconds": trim_duration, "ad_end_hhmmss": None}
            if trim_duration is not None:
                payload["ad_end_hhmmss"] = MediaFileCleaner.format_to_time(
                    trim_duration)
            print(json.dumps(payload, ensure_ascii=False))
        else:
            if trim_duration is None:
                print("No reliable ad-end point found in the analysis window.")
            else:
                print(
                    f"Ads end ≈ {trim_duration:.3f} s ({MediaFileCleaner.format_to_time(trim_duration)})")

        # Calculate start time with optional padding
        pad_s = max(0, args.silence_pad_ms) / 1000.0
        start_s = trim_duration + pad_s
        # Determine trimmed file path
        trimmed_path = os.path.join(args.trim_output_path, os.path.basename(file_path))
        
        # Trim the file
        if not args.dry_run:
            if trim_duration is not None:
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
