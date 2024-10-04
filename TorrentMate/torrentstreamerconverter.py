#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import os
import sys
import time
import threading
import subprocess
import logging
import argparse
from typing import Optional, List
import libtorrent as lt
from tqdm import tqdm


class TorrentStreamerConverter:
    """
    Class to stream and convert files from a torrent to H.265 on the fly.
    """

    def __init__(
        self,
        source: str,
        output_directory: str,
        max_simultaneous_conversions: int = 2,
        pause_threshold: float = 0.05,
        file_extensions: Optional[List[str]] = None,
        ffmpeg_params: Optional[List[str]] = None,
    ) -> None:
        """
        Initializes the TorrentStreamerConverter with the given parameters.

        Args:
            source (str): Magnet link or path to a .torrent file.
            output_directory (str): Output directory for the converted files.
            max_simultaneous_conversions (int, optional): Maximum number of simultaneous conversions. Defaults to 2.
            pause_threshold (float, optional): Pause threshold as a percentage (0 to 1). Defaults to 0.05 (5%).
            file_extensions (list of str, optional): List of file extensions to convert. Defaults to common video formats.
            ffmpeg_params (list of str, optional): Additional parameters to pass to ffmpeg.
        """
        self.source = source
        self.output_directory = output_directory
        self.max_simultaneous_conversions = max_simultaneous_conversions
        self.pause_threshold = pause_threshold
        # Set default file extensions if none provided
        self.file_extensions = file_extensions or ['.mp4', '.mkv', '.avi', '.mov', '.flv']
        # Set default ffmpeg parameters if none provided
        self.ffmpeg_params = ffmpeg_params or [
            '-c:v', 'libx265',
            '-preset', 'fast',
            '-x265-params', 'log-level=error',
            '-c:a', 'copy'
        ]

        # Set up logging to a file with DEBUG level
        logging.basicConfig(
            filename='torrent_streamer_converter.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Initialize libtorrent session
        self.session = lt.session()
        # Add torrent to the session and get the handle
        self.handle = self._add_torrent()
        # Semaphore to limit simultaneous conversions
        self.conversion_semaphore = threading.Semaphore(self.max_simultaneous_conversions)
        # Queue of files to be converted
        self.file_queue = []

    def _add_torrent(self) -> lt.torrent_handle:
        """
        Adds the torrent to the session and waits for metadata.

        Returns:
            lt.torrent_handle: Handle of the added torrent.
        """
        # Parameters for the torrent
        params = {
            'save_path': self.output_directory,
            'storage_mode': lt.storage_mode_t.storage_mode_sparse
        }

        if self.source.startswith('magnet:'):
            # If the source is a magnet link
            logging.info("Adding magnet link...")
            handle = lt.add_magnet_uri(self.session, self.source, params)
        elif os.path.isfile(self.source) and self.source.endswith('.torrent'):
            # If the source is a .torrent file
            logging.info("Adding .torrent file...")
            info = lt.torrent_info(self.source)
            handle = self.session.add_torrent({'ti': info, 'save_path': self.output_directory})
        else:
            # Invalid source provided
            logging.error("Invalid source provided. Must be a magnet link or a .torrent file.")
            raise ValueError("Invalid source provided. Must be a magnet link or a .torrent file.")

        # Wait for metadata to be downloaded
        logging.info("Downloading torrent metadata...")
        while not handle.has_metadata():
            time.sleep(1)
        logging.info("Metadata received, starting download...")
        return handle

    def start(self) -> None:
        """
        Starts streaming and converting the files from the torrent.
        """
        # Get torrent information
        torrent_info = self.handle.get_torrent_info()
        files = torrent_info.files()
        total_files = files.num_files()

        # Build a queue of files to convert
        for index in range(total_files):
            file_path = files.file_path(index)
            full_file_path = os.path.join(self.output_directory, file_path)
            file_extension = os.path.splitext(full_file_path)[1].lower()

            if file_extension in self.file_extensions:
                # Add video files to the queue
                self.file_queue.append((index, full_file_path))

        # Start conversion worker threads
        for _ in range(self.max_simultaneous_conversions):
            threading.Thread(target=self._conversion_worker, daemon=True).start()

        # Monitor the overall download progress
        self._monitor_download()

    def _conversion_worker(self) -> None:
        """
        Worker function to process files from the conversion queue.
        """
        while True:
            with self.conversion_semaphore:
                try:
                    # Get the next file from the queue
                    file_index, input_file_path = self.file_queue.pop(0)
                except IndexError:
                    # No more files to process
                    break

                logging.info(f"Preparing file: {input_file_path}")
                # Wait until the file starts downloading
                self._wait_for_download_start(file_index)
                # Convert the file
                self._convert_file(file_index, input_file_path)

    def _wait_for_download_start(self, file_index: int) -> None:
        """
        Waits until the file starts downloading.

        Args:
            file_index (int): Index of the file in the torrent.
        """
        while self.handle.file_progress()[file_index] == 0:
            # Wait until some data has been downloaded
            time.sleep(1)
        logging.info(f"Download started for file index {file_index}")

    def _convert_file(self, file_index: int, input_file_path: str) -> None:
        """
        Converts the file to H.265 while managing pause if necessary.

        Args:
            file_index (int): Index of the file in the torrent.
            input_file_path (str): Full path of the file to convert.
        """
        # Output file path
        output_file = os.path.join(
            self.output_directory,
            f"converted_{os.path.basename(input_file_path)}"
        )

        # Construct the ffmpeg command
        ffmpeg_command = ['ffmpeg', '-y', '-i', input_file_path] + self.ffmpeg_params + [output_file]

        logging.info(f"Starting conversion: {input_file_path} -> {output_file}")
        # Start the ffmpeg process
        process = subprocess.Popen(
            ffmpeg_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

        # Progress bar for conversion
        pbar = tqdm(total=100, desc=f"Converting {os.path.basename(input_file_path)}", unit='%')

        try:
            while process.poll() is None:
                if not self._is_enough_data_downloaded(file_index):
                    # Pause conversion if not enough data is downloaded
                    logging.info(f"Pausing conversion for {input_file_path}, waiting for more data.")
                    time.sleep(5)
                    continue
                # Update progress bar
                conversion_progress = self._get_conversion_progress(process.stderr)
                if conversion_progress is not None:
                    # Update the progress bar with new progress
                    pbar.update(conversion_progress - pbar.n)
                time.sleep(1)
        except Exception as e:
            logging.error(f"Error converting file {input_file_path}: {e}")
        finally:
            # Terminate the ffmpeg process
            process.terminate()
            pbar.close()

    def _get_conversion_progress(self, stderr_pipe) -> Optional[float]:
        """
        Parses ffmpeg stderr output to extract conversion progress.

        Args:
            stderr_pipe: The stderr pipe from the ffmpeg subprocess.

        Returns:
            Optional[float]: The conversion progress percentage.
        """
        # Read a line from ffmpeg stderr output
        line = stderr_pipe.readline()
        if 'frame=' in line:
            # Parse the line to find the current time
            parts = line.strip().split()
            time_part = next((part for part in parts if part.startswith('time=')), None)
            if time_part:
                time_str = time_part.split('=')[1]
                return self._calculate_progress(time_str)
        return None

    def _calculate_progress(self, time_str: str) -> Optional[float]:
        """
        Calculates the progress percentage based on the current timestamp.

        Args:
            time_str (str): The timestamp string from ffmpeg output.

        Returns:
            Optional[float]: The conversion progress percentage.
        """
        # Convert time_str (e.g., '00:01:23.45') to total seconds
        try:
            h, m, s = time_str.split(':')
            total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
            # For demonstration, assume total duration is 100 seconds
            # In a real scenario, you would extract the total duration from the media info
            total_duration = 100
            # Calculate the percentage progress
            return (total_seconds / total_duration) * 100
        except Exception as e:
            logging.error(f"Error calculating progress: {e}")
            return None

    def _is_enough_data_downloaded(self, file_index: int) -> bool:
        """
        Checks if enough data has been downloaded to continue the conversion.

        Args:
            file_index (int): Index of the file in the torrent.

        Returns:
            bool: True if enough data has been downloaded, False otherwise.
        """
        # Get the amount of data downloaded for the file
        file_progress = self.handle.file_progress()[file_index]
        # Get the total file size
        file_size = self.handle.get_torrent_info().files().file_size(file_index)
        # Calculate the ratio of unconverted data
        unconverted_size = file_size - file_progress
        unconverted_ratio = unconverted_size / file_size

        # Return True if the unconverted ratio is less than or equal to (1 - pause_threshold)
        return unconverted_ratio <= (1 - self.pause_threshold)

    def _monitor_download(self) -> None:
        """
        Monitors the overall download progress of the torrent until completion.
        """
        # Progress bar for overall download progress
        pbar = tqdm(total=100, desc="Overall Download Progress", unit='%')
        while self.handle.status().state != lt.torrent_status.seeding:
            status = self.handle.status()
            # Calculate the progress percentage
            progress = status.progress * 100
            # Update the progress bar
            pbar.update(progress - pbar.n)
            logging.info(
                f"Overall Progress: {progress:.2f}% | "
                f"Download Speed: {status.download_rate / 1000:.2f} kB/s | "
                f"Upload Speed: {status.upload_rate / 1000:.2f} kB/s"
            )
            time.sleep(5)
        # Finish the progress bar when download is complete
        pbar.update(100 - pbar.n)
        pbar.close()
        logging.info("Torrent download completed.")

def main() -> None:
    """
    Main entry point of the program.
    """

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Torrent to H.265 converter")
    # Positional arguments
    parser.add_argument("source", help="Magnet link or path to a .torrent file")
    parser.add_argument("output_directory", help="Output directory for the converted files")
    # Optional arguments for max_simultaneous_conversions and pause_threshold
    parser.add_argument(
        "--max-simultaneous-conversions",
        type=int,
        default=1,
        help="Maximum number of simultaneous conversions (default: 1)"
    )
    parser.add_argument(
        "--pause-threshold",
        type=float,
        default=0.05,
        help="Pause threshold as a percentage (0 to 1), default is 0.05 (5%%)"
    )
    # Collect any additional ffmpeg parameters
    parser.add_argument(
        "ffmpeg_params",
        nargs=argparse.REMAINDER,
        help="Additional ffmpeg parameters"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Extract the arguments
    source = args.source
    output_directory = args.output_directory
    max_simultaneous_conversions = args.max_simultaneous_conversions
    pause_threshold = args.pause_threshold
    ffmpeg_params = args.ffmpeg_params

    if not os.path.exists(output_directory):
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory)

    # Instantiate the TorrentStreamerConverter with the parsed arguments
    streamer_converter = TorrentStreamerConverter(
        source=source,
        output_directory=output_directory,
        max_simultaneous_conversions=max_simultaneous_conversions,
        pause_threshold=pause_threshold,
        ffmpeg_params=ffmpeg_params if ffmpeg_params else None
    )
    # Start the conversion process
    streamer_converter.start()


if __name__ == "__main__":
    main()
