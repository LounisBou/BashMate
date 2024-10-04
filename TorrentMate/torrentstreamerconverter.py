#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import subprocess
import logging
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
        self.file_extensions = file_extensions or ['.mp4', '.mkv', '.avi', '.mov', '.flv']
        self.ffmpeg_params = ffmpeg_params or ['-c:v', 'libx265', '-preset', 'fast', '-x265-params', 'log-level=error', '-c:a', 'copy']

        # Set up logging
        logging.basicConfig(
            filename='torrent_streamer_converter.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        self.session = lt.session()
        self.handle = self._add_torrent()
        self.conversion_semaphore = threading.Semaphore(self.max_simultaneous_conversions)
        self.file_queue = []

    def _add_torrent(self) -> lt.torrent_handle:
        """
        Adds the torrent to the session and waits for metadata.

        Returns:
            lt.torrent_handle: Handle of the added torrent.
        """
        params = {'save_path': self.output_directory, 'storage_mode': lt.storage_mode_t.storage_mode_sparse}

        if self.source.startswith('magnet:'):
            logging.info("Adding magnet link...")
            handle = lt.add_magnet_uri(self.session, self.source, params)
        elif os.path.isfile(self.source) and self.source.endswith('.torrent'):
            logging.info("Adding .torrent file...")
            info = lt.torrent_info(self.source)
            handle = self.session.add_torrent({'ti': info, 'save_path': self.output_directory})
        else:
            logging.error("Invalid source provided. Must be a magnet link or a .torrent file.")
            raise ValueError("Invalid source provided. Must be a magnet link or a .torrent file.")

        logging.info("Downloading torrent metadata...")
        while not handle.has_metadata():
            time.sleep(1)
        logging.info("Metadata received, starting download...")
        return handle

    def start(self) -> None:
        """
        Starts streaming and converting the files from the torrent.
        """
        torrent_info = self.handle.get_torrent_info()
        files = torrent_info.files()
        total_files = files.num_files()

        # Build a queue of files to convert
        for index in range(total_files):
            file_path = files.file_path(index)
            full_file_path = os.path.join(self.output_directory, file_path)
            file_extension = os.path.splitext(full_file_path)[1].lower()

            if file_extension in self.file_extensions:
                self.file_queue.append((index, full_file_path))

        # Start conversion threads
        for _ in range(self.max_simultaneous_conversions):
            threading.Thread(target=self._conversion_worker, daemon=True).start()

        self._monitor_download()

    def _conversion_worker(self) -> None:
        """
        Worker function to process files from the conversion queue.
        """
        while True:
            with self.conversion_semaphore:
                try:
                    file_index, input_file_path = self.file_queue.pop(0)
                except IndexError:
                    break  # No more files to process

                logging.info(f"Preparing file: {input_file_path}")
                self._wait_for_download_start(file_index)
                self._convert_file(file_index, input_file_path)

    def _wait_for_download_start(self, file_index: int) -> None:
        """
        Waits until the file starts downloading.

        Args:
            file_index (int): Index of the file in the torrent.
        """
        while self.handle.file_progress()[file_index] == 0:
            time.sleep(1)
        logging.info(f"Download started for file index {file_index}")

    def _convert_file(self, file_index: int, input_file_path: str) -> None:
        """
        Converts the file to H.265 while managing pause if necessary.

        Args:
            file_index (int): Index of the file in the torrent.
            input_file_path (str): Full path of the file to convert.
        """
        output_file = os.path.join(
            self.output_directory,
            f"converted_{os.path.basename(input_file_path)}"
        )

        ffmpeg_command = ['ffmpeg', '-y', '-i', input_file_path] + self.ffmpeg_params + [output_file]

        logging.info(f"Starting conversion: {input_file_path} -> {output_file}")
        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Progress bar for conversion
        pbar = tqdm(total=100, desc=f"Converting {os.path.basename(input_file_path)}", unit='%')

        try:
            while process.poll() is None:
                if not self._is_enough_data_downloaded(file_index):
                    logging.info(f"Pausing conversion for {input_file_path}, waiting for more data.")
                    time.sleep(5)
                    continue
                # Update progress bar
                conversion_progress = self._get_conversion_progress(process.stderr)
                if conversion_progress is not None:
                    pbar.update(conversion_progress - pbar.n)
                time.sleep(1)
        except Exception as e:
            logging.error(f"Error converting file {input_file_path}: {e}")
        finally:
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
        line = stderr_pipe.readline().decode('utf-8')
        if 'frame=' in line:
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
        # Convert time_str (e.g., '00:01:23.45') to seconds
        try:
            h, m, s = time_str.split(':')
            total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
            # For demonstration, assume total duration is 100 seconds
            # In a real scenario, you would extract the total duration from the media info
            total_duration = 100
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
        file_progress = self.handle.file_progress()[file_index]
        file_size = self.handle.get_torrent_info().files().file_size(file_index)
        unconverted_size = file_size - file_progress
        unconverted_ratio = unconverted_size / file_size

        return unconverted_ratio <= (1 - self.pause_threshold)

    def _monitor_download(self) -> None:
        """
        Monitors the overall download progress of the torrent until completion.
        """
        pbar = tqdm(total=100, desc="Overall Download Progress", unit='%')
        while self.handle.status().state != lt.torrent_status.seeding:
            status = self.handle.status()
            progress = status.progress * 100
            pbar.update(progress - pbar.n)
            logging.info(
                f"Overall Progress: {progress:.2f}% | "
                f"Download Speed: {status.download_rate / 1000:.2f} kB/s | "
                f"Upload Speed: {status.upload_rate / 1000:.2f} kB/s"
            )
            time.sleep(5)
        pbar.update(100 - pbar.n)
        pbar.close()
        logging.info("Torrent download completed.")


def main() -> None:
    """
    Main entry point of the program.
    """
    if len(sys.argv) < 3:
        print("Usage: python torrent_to_h265.py <magnet_link_or_torrent_file> <output_directory> [additional ffmpeg parameters]")
        sys.exit(1)

    source = sys.argv[1]
    output_directory = sys.argv[2]
    ffmpeg_params = sys.argv[3:]  # Additional ffmpeg parameters from command line

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    streamer_converter = TorrentStreamerConverter(
        source=source,
        output_directory=output_directory,
        max_simultaneous_conversions=2,  # Adjust this parameter as needed
        pause_threshold=0.05,  # Adjust this parameter (default is 5%)
        ffmpeg_params=ffmpeg_params if ffmpeg_params else None
    )
    streamer_converter.start()


if __name__ == "__main__":
    main()
