import ascii_animation as aa
from pathlib import Path
import os
import fire

def main(output_directory: str) -> None:
    output_directory = Path(os.path.expanduser(output_directory)).resolve(strict=True)
    json_path = output_directory / f'{output_directory.stem}.json'
    audio_path = Path(output_directory / f'{output_directory.stem}.wav').resolve(strict=True)
    animation = aa.load_data_from_json(json_path.resolve(strict=True))
    aa.play_ascii_frames_with_sound(animation['frames'], animation['frame_rate'], str(audio_path))


if __name__ == "__main__":
    fire.Fire(main)
