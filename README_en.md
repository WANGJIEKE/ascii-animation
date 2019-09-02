# ASCII Animation

Easily convert your video into ASCII art animation.

## Features

- Generate ASCII art animation from any FFmpeg-supported video
- Customizable output framerate and size
- Synchronized audio supported

## Get Started

This program is written in Python 3.7. Tested on Windows 10 1903 and macOS Mojave 10.14.6.

First, install FFmpeg. You can get it from its [official website](https://ffmpeg.org/).

If you are on Windows, you may install it from [Chocolatey](https://chocolatey.org/) by typing `choco install ffmpeg`.

If you are on macOS, you may install it from [Homebrew](https://brew.sh/) by typing `brew install ffmpeg`.

Then, type following commands

```sh
git clone https://github.com/WANGJIEKE/ascii-animation.git
cd ascii-animation
python -m pip install -r requirements.txt
```

Once all requirements are installed, assume the video file is `video.mp4` (in the same directory as `ascii_animation.py`) and the height
of current terminal/console is 139 rows, type `python build.py video.mp4 139 && python play.py video.out` to generate and play the ASCII
animation.
