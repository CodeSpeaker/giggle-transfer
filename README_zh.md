# Giggle Transfer

[English](README.md)

### 简介

Giggle Transfer 是一个基于 Python 的文件传输工具，利用**声波调制解调**技术通过声音传输文件。它使用 zlib 压缩文件，通过 [ggwave](https://github.com/ggerganov/ggwave) 编码为音频信号，支持扬声器/麦克风实时传输或 WAV 文件中转。

### 工作原理

```
文件 → zlib 压缩 → ggwave 编码 → 音频（扬声器/WAV）
                                    ↓
                              麦克风/WAV → ggwave 解码 → zlib 解压 → 文件
```

### 环境要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 包管理器
- 系统 PortAudio 库：
  - macOS：`brew install portaudio`
  - Linux：`apt install portaudio19-dev`
  - Windows：参见 [PyAudio Windows 指南](https://pypi.org/project/PyAudio/)

### 快速开始

```bash
# 安装依赖
uv sync

# 通过扬声器发送文件
uv run python src/giggle_transfer/sender.py -i document.pdf -m sound

# 通过麦克风接收
uv run python src/giggle_transfer/receiver.py -m mic
```

### 使用方法

#### 发送端

```bash
uv run python src/giggle_transfer/sender.py -i <文件> -m <模式> [-o output.wav] [-p 协议ID]
```

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入文件路径（必填） |
| `-m, --mode` | `sound`（扬声器）或 `file`（WAV） |
| `-o, --output` | 输出 WAV 文件名（默认：`ultra_output.wav`） |
| `-p, --protocol` | 协议 ID：`0`（可听声）或 `3`（超声波） |

#### 接收端

```bash
uv run python src/giggle_transfer/receiver.py -m <模式> [-i input.wav] [-o 输出目录]
```

| 参数 | 说明 |
|------|------|
| `-m, --mode` | `mic`（麦克风）或 `file`（WAV） |
| `-i, --input` | 输入 WAV 文件名（默认：`ultra_output.wav`） |
| `-o, --outdir` | 输出目录（默认：`.`） |

### 协议选项

| ID | 名称 | 说明 |
|----|------|------|
| 0 | 可听声（Normal） | 标准音频范围，最稳定 |
| 3 | 超声波（Ultrasound） | 接近超声频段，不易听到但传输距离较短 |

### 示例流程

```bash
# 发送端：压缩文件并编码为 WAV
uv run python src/giggle_transfer/sender.py -i photo.jpg -m file -o transfer.wav

# 接收端：解码 WAV 文件
uv run python src/giggle_transfer/receiver.py -m file -i transfer.wav -o ./
```