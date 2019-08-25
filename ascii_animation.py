"""ASCII Animation

Easily convert your video into ASCII art animation.

See run.py in the same directory for usage.
I'm going to add a complete command line interface later.
"""


from typing import Optional, Tuple, List, Dict, Union
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import argparse
import os
import pickle
import subprocess as sp
import sys
import shutil
import shlex
import time


_is_windows = sys.platform == 'win32'
_is_macos = sys.platform == 'darwin'

if _is_windows:
    import winsound as ws


def get_frame_rate(file: str, ffprobe: str) -> float:
    """Get the frame rate of the given video using `ffprobe`

    :param file: path to the video
    :param ffmpeg: path to `ffprobe` executable
    :return: frame rate of the video
    """
    cmd = f'ffprobe -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate {file}'
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


def change_frame_rate(src: str, dst: str, new_fps: int, ffmpeg: str) -> None:
    """Change the frame rate of the given video

    :param src: source video
    :param dst: output video w/ new frame rate (recommend to use mp4 format)
    :param new_fps: new frame rate
    :param ffmpeg: ffmpeg executable path
    """
    cmd = f'{ffmpeg} -y -i {src} -filter:v fps=fps={new_fps} {dst}'
    print(f'[Info] executing "{cmd}"')
    p = sp.Popen(shlex.split(cmd))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError('failed to change the frame rate')
    print(f'[Success] new video file is {dst}')


def extract_audio(src: str, dst: str, ffmpeg: str) -> None:
    """Extract audio from video

    :param src: source video
    :param dst: output audio
    :param ffmpeg: ffmpeg executable path
    """
    cmd = f'{ffmpeg} -y -i {src} -map a:0 {dst}'
    print(f'[Info] executing "{cmd}"')
    p = sp.Popen(shlex.split(cmd))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError('failed to extract audio')
    print(f'[Success] sound file is {dst}')


def extract_grayscale_frames(
    src: str,
    dst_dir: str,
    output_format: str,
    new_size: Tuple[int, int],
    ffmpeg: str
) -> None:
    """Extract all frames from given video files and store them to given directory

    :param src: source video
    :param dst_dir: output directory
    :param output_format: image format
    :param new_size: new resolution for frames (using ffmpeg-style size)
    :param ffmpeg: ffmpeg executable path
    """
    cmd = f'{ffmpeg} -i {src} -vf scale={new_size[0]}:{new_size[1]},' \
        f'format=gray {dst_dir}/{src}_frame_%04d.{output_format}'
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
    return ascii_mapping[int((len(ascii_mapping) - 1) * val / 256)]


def image_to_ascii_frame(file: str, ascii_mapping: str) -> List[str]:
    """Convert single image to a list of ASCII character strings

    :param file: image file path
    :param ascii_mapping: ASCII mapping (index 0 is darkest)
    :return: corresponding single frame in ASCII characters
    """
    img = Image.open(file)
    pixels = img.load()
    return [''.join(grayscale256_to_ascii(pixels[i, j], ascii_mapping) for i in range(img.size[0])) for j in range(img.size[1])]


def images_to_ascii_frames(dir: str, ascii_mapping: str) -> List[List[str]]:
    """
    Convert all images (frames) to a nested list of ASCII character strings

    Info: tqdm here is used to show the progress bar

    :param dir: input dir (the dir passed into extract_grayscale_frames function)
    :param ascii_mapping: ASCII mapping (index 0 is darkest)
    :return: corresponding ASCII frames
    """
    return [image_to_ascii_frame(path, ascii_mapping) for path in tqdm(sorted(Path(dir).iterdir()), ascii=_is_windows)]


def save_data_to_pickle(path: str, frames: List[List[str]]) -> None:
    """Store converted ASCII frames using pickle so that next time you needn't to convert it again

    :param path: pickle file path
    :param frames: ASCII frames
    """
    with open(path, 'wb') as file:
        pickle.dump(frames, file)


def load_data_from_pickle(path) -> List[List[str]]:
    """Load ASCII frames from pickle

    :param path: pickle file path
    :return: ASCII frames
    """
    with open(path, 'rb') as file:
        return pickle.load(file)


def play_ascii_frames_with_sound(ascii_frames: List[List[str]], frame_rate: float, sound_file: str) -> None:
    """Play ASCII frames with sound extracted from the video

    Sound is not supported in Linux yet (I don't have any Linux device that can make a sound)

    :param ascii_frames: ASCII frames
    :param frame_rate: the fps of ASCII frames
    :param sound_file: path to the sound file
    """
    frame_len = 1 / frame_rate
    start_time = time.time()
    if _is_windows:
        os.system('cls')
        ws.PlaySound(sound_file, ws.SND_FILENAME | ws.SND_ASYNC)
    else:
        os.system('clear')
        if _is_macos:
            p = sp.Popen(['afplay', '-q', '1', sound_file])
    try:
        for frame in ascii_frames:
            # go to the row=1,col=1 cell
            print('\x1b[;f' if _is_windows else '\033[1;1H', end='')
            print(*frame, sep='\n')
            time.sleep(frame_len - ((time.time() - start_time) % frame_len))
    finally:  # send SIGTERM to child process when finish
        if _is_macos:
            p.terminate()
            p.wait()

__author__ = 'WANGJIEKE'
