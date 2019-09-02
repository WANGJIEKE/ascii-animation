# ASCII Animation

[English](./README_en.md)

轻松将视频转换为ASCII字符动画。

## 特性

- 从FFmpeg支持的视频格式中生成ASCII字符动画
- 可以自定字符动画的帧率和大小
- 同步音频输出

## 开始使用

本程序使用Python 3.7版本，低于该版本可能会导致不兼容。程序在Windows 10 1903版本以及macOS Mojave 10.14.6版本测试通过。

首先需要确保你的电脑上已经安装了FFmpeg，如果没有安装的话可以前往[官网](https://ffmpeg.org/)下载。

如果你是Windows用户，你也可以通过[Chocolatey](https://chocolatey.org/)来安装。首先安装Chocolatey，
然后在命令提示符（或PowerShell）中输入`choco install ffmpeg`进行安装。

如果你是macOS用户，你也可以通过[Homebrew](https://brew.sh/)来安装。首先安装Homebrew，然后在终端中输入`brew install ffmpeg`进行安装。

安装完FFmpeg后，通过以下命令下载代码并安装依赖项

```sh
git clone https://github.com/WANGJIEKE/ascii-animation.git
cd ascii-animation
python -m pip install -r requirements.txt
```

安装好依赖项后，假设视频文件名为`video.mp4`（与`ascii_animation.py`在同一目录下），当前终端/控制台的高度为139行，
输入`python build.py video.mp4 139 && python play.py video.out`即可。
