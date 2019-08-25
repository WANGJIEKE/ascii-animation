# ASCII Animation

[English](./README_en.md)

轻松将视频转换为ASCII字符动画。

## Get Started

首先需要确保你的电脑上已经安装了FFmpeg，如果没有安装的话可以前往[官网](https://ffmpeg.org/)下载。

如果你是Windows用户，你也可以通过[Chocolatey](https://chocolatey.org/)来安装。首先安装Chocolatey，然后在命令提示符（或PowerShell）中输入`choco install ffmpeg`进行安装。

如果你是macOS用户，你也可以通过[HomeBrew](https://brew.sh/)来安装。首先安装HomeBrew，然后在终端中输入`brew install ffmpeg`进行安装。

安装完FFmpeg后，通过以下命令下载代码并安装依赖项

```sh
git clone https://github.com/WANGJIEKE/ascii-animation.git
cd ascii-animation
python -m pip install -r requirements.txt
```

安装好依赖项后，打开`run.py`，根据注释对代码进行修改，然后运行这个文件即可。
