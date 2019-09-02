"""ASCII Animation

Easily convert your video into ASCII art animation.

See run.py in the same directory for usage.
I'm going to add a complete command line interface later.
"""

__author__ = 'WANGJIEKE'

from typing import Optional, Tuple, List, Dict, Union, Any
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import argparse
import os
import json
import base64
import subprocess as sp
import sys
import shutil
import shlex
import time


_is_windows = sys.platform == 'win32'
_is_macos = sys.platform == 'darwin'

if _is_windows:
    import winsound as ws


def get_frame_rate(file: Path, ffprobe: str) -> float:
    """Get the frame rate of the given video using `ffprobe`

    :param file: path to the video
    :param ffmpeg: path to `ffprobe` executable
    :return: frame rate of the video
    """
    cmd = f'ffprobe -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate "{file}"'
    print(f'[Info] executing "{cmd}"')
    p = sp.Popen(shlex.split(cmd), stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    if p.returncode == 0:
        frame_rate = eval(p.communicate()[0])
        print(f'[Success] frame rate is {frame_rate}')
        return frame_rate
    else:
        print(p.communicate()[1].decode(), file=sys.stderr)
        raise RuntimeError('failed to get the frame rate')


def change_frame_rate(src: Path, dst: Path, new_fps: int, ffmpeg: str, overwrite_exist: Optional[bool] = True) -> None:
    """Change the frame rate of the given video

    :param src: source video
    :param dst: output video w/ new frame rate (recommend to use mp4 format)
    :param new_fps: new frame rate
    :param ffmpeg: ffmpeg executable path
    """
    cmd = f'{ffmpeg} {"-y" if overwrite_exist else ""} -i "{src}" -filter:v fps=fps={new_fps} "{dst}"'
    print(f'[Info] executing "{cmd}"')
    p = sp.Popen(shlex.split(cmd))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError('failed to change the frame rate')
    print(f'[Success] new video file is {dst}')


def extract_audio(src: Path, dst: Path, ffmpeg: str, overwrite_exist: Optional[bool] = True) -> None:
    """Extract audio from video

    :param src: source video
    :param dst: output audio
    :param ffmpeg: ffmpeg executable path
    """
    cmd = f'{ffmpeg} {"-y" if overwrite_exist else ""} -i "{src}" -map a:0 "{dst}"'
    print(f'[Info] executing "{cmd}"')
    p = sp.Popen(shlex.split(cmd))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError('failed to extract audio')
    print(f'[Success] sound file is {dst}')


def extract_grayscale_frames(
    src: Path,
    dst_dir: Path,
    output_format: str,
    new_size: Tuple[int, int],
    ffmpeg: str,
    overwrite_exist: Optional[bool] = True
) -> None:
    """Extract all frames from given video files and store them to given directory

    :param src: source video
    :param dst_dir: output directory
    :param output_format: image format
    :param new_size: new resolution for frames (using ffmpeg-style size)
    :param ffmpeg: ffmpeg executable path
    """
    cmd = f'{ffmpeg} {"-y" if overwrite_exist else ""} -i "{src}" -vf scale={new_size[0]}:{new_size[1]},' \
        f'format=gray "{dst_dir.resolve(strict=True) / src.name}_frame_%05d.{output_format}"'
    print(f'[Info] executing "{cmd}"')
    p = sp.Popen(shlex.split(cmd))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError('failed to extract frames')
    print(f'[Success] frames are inside {dst_dir}')


def grayscale256_to_ascii(val: int, ascii_mapping: str) -> str:
    """Map grayscale value (which is in range(256)) to given ASCII mapping

    :param val: grayscale value
    :param ascii_mapping: ASCII mapping (index 0 is darkest)
    :return: corresponding ASCII character
    """
    return ascii_mapping[round(val / 255 * (len(ascii_mapping) - 1))]


def image_to_ascii_frame(file: Path, ascii_mapping: str) -> List[str]:
    """Convert single image to a list of ASCII character strings

    :param file: image file path
    :param ascii_mapping: ASCII mapping (index 0 is darkest)
    :return: corresponding single frame in ASCII characters
    """
    img = Image.open(file)
    pixels = img.load()
    return [''.join(grayscale256_to_ascii(pixels[i, j], ascii_mapping) for i in range(img.size[0])) for j in range(img.size[1])]


def images_to_ascii_frames(dir: Path, ascii_mapping: str) -> List[List[str]]:
    """
    Convert all images (frames) to a nested list of ASCII character strings

    Info: tqdm here is used to show the progress bar

    :param dir: input dir (the dir passed into extract_grayscale_frames function)
    :param ascii_mapping: ASCII mapping (index 0 is darkest)
    :return: corresponding ASCII frames
    """
    return [image_to_ascii_frame(path, ascii_mapping) for path in tqdm(sorted(dir.iterdir()), ascii=_is_windows)]


def save_data_to_json(path: Union[Path, str], frames: List[List[str]], frame_rate: float) -> None:
    """Store converted ASCII frames using JSON so that next time you needn't to convert it again

    :param path: JSON file path
    :param frames: ASCII frames
    """
    with open(path, 'w') as file:
        json.dump({'frames': frames, 'frame_rate': frame_rate}, file)


def load_data_from_json(path: Union[Path, str]) -> Dict[str, Any]:
    """Load ASCII frames from JSON

    :param path: JSON file path
    :return: ASCII frames
    """
    with open(path, 'r') as file:
        return json.load(file)


def play_ascii_frames_with_sound(ascii_frames: List[List[str]], frame_rate: float, sound_file: str) -> None:
    """Play ASCII frames with sound extracted from the video

    Sound is not supported in Linux yet (I don't have any Linux device that can make a sound)

    :param ascii_frames: ASCII frames
    :param frame_rate: the fps of ASCII frames
    :param sound_file: path to the sound file
    """
    frame_len = 1 / frame_rate
    if _is_windows:
        os.system('cls')
        ws.PlaySound(sound_file, ws.SND_FILENAME | ws.SND_ASYNC)
    else:
        os.system('clear')
        if _is_macos:
            cmd = f'afplay -q 1 "{sound_file}"'
            p = sp.Popen(shlex.split(cmd))
    start_time = time.time()
    try:
        for frame in ascii_frames:
            # go to the row=1,col=1 cell
            print('\x1b[;H', end='')
            print(*frame, sep='\n', end='')
            time.sleep(frame_len - ((time.time() - start_time) % frame_len))
    finally:  # send SIGTERM to child process when finish
        if _is_macos:
            p.terminate()
            p.wait()
