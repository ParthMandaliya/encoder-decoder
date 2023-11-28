import os
import math
import cv2
import base64
import json
import numpy as np

from pathlib import Path
from tqdm import tqdm


class Encoder:
    def __init__(self) -> None:
        self.__dimensions = (720, 720)
        self.__frame_shape = self.__dimensions + (3,)
        self.__chunksize = math.prod(self.__frame_shape)

    def read_file_chunks(self, file_path: str) -> bytes:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(self.__chunksize)
                if not data:
                    break
                yield data

    def encode(self, filepath: Path, output_dir: Path):
        filename = filepath.name
        video_filepath = output_dir / (filename + ".mkv")

        filesize = os.stat(str(filepath)).st_size

        video_writer = cv2.VideoWriter(
            str(video_filepath),
            cv2.VideoWriter_fourcc(*"FFV1"),  # Lossless codec
            60.0, self.__dimensions,
        )
        total_frames = math.ceil(filesize / self.__chunksize)

        metadata = {
            "filename": filename,
        }
        metadata = base64.b64encode(str(json.dumps(metadata)).encode())
        metadata = metadata.ljust(self.__chunksize, b"\x00")

        video_writer.write(
            np.frombuffer(metadata, dtype=np.uint8).reshape(self.__frame_shape)
        )

        pbar = tqdm(total=total_frames, desc="Creating video")
        for data in self.read_file_chunks(str(filepath)):

            if len(data) < self.__chunksize:
                data = data.ljust(self.__chunksize, b'\x00')

            frame = np.frombuffer(data, dtype=np.uint8).reshape(
                self.__frame_shape)
            video_writer.write(frame)
            pbar.update(1)

        video_writer.release()
        pbar.close()


if __name__ == "__main__":
    import sys

    Encoder().encode(
        Path(sys.argv[1]).resolve(strict=True),
        Path(sys.argv[2]).resolve(strict=True)
    )
