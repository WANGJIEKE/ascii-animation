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

Once you have install all dependencies, make a copy of `config.template.json` and rename the copy into `config.json`.
Then open the json file, modify it accordingly, then execute `python ascii_animation.py -br`.

## JSON Configuration File Documentation

```jsonc
{
    "input_file": "path/to/video",
    "sound_output_file": "path/for/save/audio",
    "frames_output_directory": "directory/for/save/frames",
    "custom_fps": 0,              // custom fps for animation; 0 for using original video's frame rate
    "frames_output_format": "png",
    "frames_output_width": -1,    // please refer FFmpeg's documentation for the width and height option
    "frames_output_height": 160,  // https://trac.ffmpeg.org/wiki/Scaling
    "json_output_file": "path/for/save/json",
    "ascii_mapping": "@%#*+=-:. ",
    "ffmpeg_executable": "ffmpeg",  // path to your `ffmpeg` and `ffprob` executable
    "ffprob_executable": "ffprob"
}
```

For the `frames_output_width` and `frames_output_height`, the simplest way to do this is setting `frames_output_width` to `-1`,
and setting `frames_output_height` to the number of rows of the ASCII animation (or the number of rows of your terminal/console).

## Command Line Parameters

**You must set at least one of `-b` (`--is-building`) or `-r` (`--is-running`).**

| Option | Description |
|:-|:-|
|`-h`, `--help`| Print help message and exit |
|`-c JSON_CONFIG`, `--json-config JSON_CONFIG`| Use file `JSON_CONFIG` instead of default `./config.json` as parameter file |
|`-o`, `--overwrite-existing-files`| Overwrite existing files (implemented by adding `-y` option to FFmpeg) |
|`-b`, `--is-building`| Build ASCII frames and store them |
|`-r`, `--is-running`| Play ASCII frames |
