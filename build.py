import ascii_animation as aa
from typing import Optional
from pathlib import Path
import os
import shutil
import fire


def main(
    input_video_path: str,
    output_frame_height: int,
    output_directory: Optional[str]='',
    fps: Optional[int]=0,
    output_frame_width: Optional[int]=-1,
    ascii_mapping: Optional[str]="@%#*+=-:. ",
    reversed: Optional[bool]=False,
    overwrite_exist: Optional[bool]=False,
    ffmpeg_path: Optional[str]="ffmpeg",
    ffprob_path: Optional[str]="ffprob"
) -> None:
    input_video_path = Path(os.path.expanduser(input_video_path)).resolve(strict=True)
    if output_directory:
        output_directory = Path(os.path.expanduser(output_directory))
    else:
        output_directory = Path(input_video_path.parent / f'{input_video_path.stem}.out')
    if output_directory.exists():
        if overwrite_exist:
            shutil.rmtree(output_directory)
        else:
            raise FileExistsError('output_directory exists; use --overwrite_exist option to overwrite')
    output_directory.mkdir(parents=True, exist_ok=False)
    output_directory = output_directory.resolve(strict=True)
    if fps > 0:
        new_fps_video_path = Path(output_directory / f'{input_video_path.stem}.{fps}fps.mp4')
        aa.change_frame_rate(input_video_path, new_fps_video_path, fps, ffmpeg_path, overwrite_exist)
        input_video_path = new_fps_video_path.resolve()
    else:
        fps = aa.get_frame_rate(input_video_path, ffprob_path)
    aa.extract_audio(input_video_path, Path(output_directory / f'{input_video_path.stem}.wav'), ffmpeg_path, overwrite_exist)
    frames_directory = Path(output_directory / f'{input_video_path.stem}.frames')
    frames_directory.mkdir()
    frames_directory = frames_directory.resolve(strict=True)
    aa.extract_grayscale_frames(
        input_video_path,
        frames_directory,
        'png',
        (output_frame_width, output_frame_height),
        ffmpeg_path, overwrite_exist
    )
    frames = aa.images_to_ascii_frames(frames_directory, ascii_mapping)
    aa.save_data_to_json(Path(output_directory / f'{input_video_path.stem}.json'), frames, fps)


if __name__ == "__main__":
    fire.Fire(main)
