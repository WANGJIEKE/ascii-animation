"""File for running ascii_animation

Please read the comments.
"""

import ascii_animation as aa
import os

INPUT_FILE = 'chika.flv'  # input video file name
SOUND_OUTPUT_FILE = 'chika.wav'

FRAMES_OUTPUT_DIRECTORY = 'chika.frames'
FRAMES_OUTPUT_FORMAT = 'png'
FRAMES_OUTPUT_SIZE = (-1, 160)  # see ffmpeg docs (https://trac.ffmpeg.org/wiki/Scaling) for details

PICKLE_OUTPUT_FILE = 'chika.pickle'

# Notice that left side is for dark color and right side is for bright color
# ASCII_MAPPING = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
ASCII_MAPPING = '@%#*+=-:. '  # I think this mapping is actually better
FFMPEG_EXECUTABLE_PATH = 'ffmpeg'  # ffmpeg executable path
FFPROB_EXECUTABLE_PATH = 'ffprob'  # ffprob executable path

BUILDING = True  # if you want to build the pickle file, set it to True
RUNNING = True  # if you want to load existed file, set it to True
# set thses two to both True to first build then run

CUSTOM_FPS = False

frame_rate = aa.get_frame_rate(INPUT_FILE, FFPROB_EXECUTABLE_PATH)

if CUSTOM_FPS:
    frame_rate = 12  # your custom fps here
    aa.change_frame_rate(INPUT_FILE, f'{INPUT_FILE}.{frame_rate}fps.mp4', frame_rate, FFMPEG_EXECUTABLE_PATH)
    INPUT_FILE = f'{INPUT_FILE}.{frame_rate}fps.mp4'  # use video w/ new fps as new input file

if BUILDING:
    aa.extract_audio(INPUT_FILE, SOUND_OUTPUT_FILE, FFMPEG_EXECUTABLE_PATH)
    os.makedirs(FRAMES_OUTPUT_DIRECTORY, exist_ok=True)
    aa.extract_grayscale_frames(INPUT_FILE, FRAMES_OUTPUT_DIRECTORY, FRAMES_OUTPUT_FORMAT, FRAMES_OUTPUT_SIZE, FFMPEG_EXECUTABLE_PATH)
    ascii_frames = aa.images_to_ascii_frames(FRAMES_OUTPUT_DIRECTORY, ASCII_MAPPING)

    aa.save_data_to_pickle(PICKLE_OUTPUT_FILE, ascii_frames)
if RUNNING and not BUILDING:
    ascii_frames = aa.load_data_from_pickle(PICKLE_OUTPUT_FILE)

if RUNNING:
    aa.play_ascii_frames_with_sound(ascii_frames, frame_rate, SOUND_OUTPUT_FILE)

__author__ = 'WANGJIEKE'
