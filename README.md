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

安装好依赖项后，将`config.template.json`复制一份，并将复制的那份重命名为`config.json`。用文本编辑器将其打开，
修改里面的参数（可以参考下面的文档）。修改完毕保存之后，执行`python ascii_animation.py -br`即可。

## JSON配置文件

```jsonc
{
    "input_file": "path/to/video",
    "sound_output_file": "path/for/save/audio",
    "frames_output_directory": "directory/for/save/frames",
    "custom_fps": 0,              // 自定义动画帧率；0代表使用原视频帧率
    "frames_output_format": "png",
    "frames_output_width": -1,    // 对于宽度和高度的设置请参考FFmpeg的文档
    "frames_output_height": 160,  // https://trac.ffmpeg.org/wiki/Scaling
    "json_output_file": "path/for/save/json",
    "ascii_mapping": "@%#*+=-:. ",
    "ffmpeg_executable": "ffmpeg",  // `ffmpeg`这个可执行文件的路径
    "ffprob_executable": "ffprob"   // `ffprob`这个可执行文件的路径
}
```

一般来讲，将`frames_output_width`设置为`-1`，将`frames_output_height`设置为ASCII动画的行数（或者你的终端/控制台）的行数即可。

## 命令行参数

**在启动程序时，必须设置`-b`（`--is-building`）或`-r` （`--is-running`）两个选项中的至少一个。**

| 选项 | 描述 |
|:-|:-|
|`-h`, `--help`| 显示帮助信息，然后退出程序 |
|`-c JSON_CONFIG`, `--json-config JSON_CONFIG`| 使用自定义的`JSON_CONFIG`文件作为参数文件（默认文件为`./config.json`）|
|`-o`, `--overwrite-existing-files`| 覆盖已存在的文件 (通过往FFmpeg的选项中加入`-y`来实现）|
|`-b`, `--is-building`| 生成并保存ASCII动画 |
|`-r`, `--is-running`| 播放ASCII动画 |
