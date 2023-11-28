import json
import cv2
import base64
import math

from tqdm import tqdm
from pathlib import Path


class Decoder:
    def __init__(self) -> None:
        pass

    def decode(
        self, video_filepath: Path, output_filepath: Path
    ):
        video_reader = cv2.VideoCapture(str(video_filepath))
        total_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

        ret, metadata_frame = video_reader.read()
        assert ret, "Unable to read metadata frame"

        metadata = base64.b64decode(
            metadata_frame.flatten().tobytes()
        ).decode()
        metadata = json.loads(metadata)

        filename = metadata["filename"]

        output_file = output_filepath / filename
        i = 0
        while output_file.exists():
            output_file = (output_file.parent.joinpath(
                f"{output_file.stem}_{str(i)}{output_file.suffix}"
            ))
            i += 1

        pbar = tqdm(
            total=math.ceil(total_frames - 1), desc="Reconstructing data")
        with open(output_file, "wb") as o_file:
            reconstructed_data_length = 0
            for _ in range(total_frames - 1):
                _, frame = video_reader.read()

                # Reshape the frame to a 1D array
                array_1d = frame.flatten()

                reconstructed_data_length += len(array_1d)
                o_file.write(array_1d)
                pbar.update(1)

        pbar.close()
        video_reader.release()

        print(f"\nFile {str(output_file)} created.")


if __name__ == "__main__":
    import sys

    Decoder().decode(
        Path(sys.argv[1]).resolve(strict=True),
        Path(sys.argv[2]).resolve(strict=True),
    )
