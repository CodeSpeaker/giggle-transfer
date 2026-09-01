# Giggle Transfer

[中文](README_zh.md)

### What is it?

Giggle Transfer is a Python-based file transfer tool that uses **acoustic modem** technology to send and receive files through sound waves. It compresses files with zlib, encodes them into audio signals using [ggwave](https://github.com/ggerganov/ggwave), and can transmit via speaker/microphone or save to WAV files.

### How does it work?

```
File → zlib compress → ggwave encode → audio (speaker/WAV)
                                          ↓
                                    microphone/WAV → ggwave decode → zlib decompress → File
```

### Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- System PortAudio library:
  - macOS: `brew install portaudio`
  - Linux: `apt install portaudio19-dev`
  - Windows: follow [PyAudio Windows guide](https://pypi.org/project/PyAudio/)

### Quick Start

```bash
# Install dependencies
uv sync

# Send a file via speaker
uv run python src/giggle_transfer/sender.py -i document.pdf -m sound

# Receive via microphone
uv run python src/giggle_transfer/receiver.py -m mic
```

### Usage

#### Sender

```bash
uv run python src/giggle_transfer/sender.py -i <file> -m <mode> [-o output.wav] [-p protocol]
```

| Argument | Description |
|----------|-------------|
| `-i, --input` | Input file path (required) |
| `-m, --mode` | `sound` (speaker) or `file` (WAV) |
| `-o, --output` | Output WAV filename (default: `ultra_output.wav`) |
| `-p, --protocol` | Protocol ID: `0` (audible) or `3` (ultrasound) |

#### Receiver

```bash
uv run python src/giggle_transfer/receiver.py -m <mode> [-i input.wav] [-o output_dir]
```

| Argument | Description |
|----------|-------------|
| `-m, --mode` | `mic` (microphone) or `file` (WAV) |
| `-i, --input` | Input WAV filename (default: `ultra_output.wav`) |
| `-o, --outdir` | Output directory (default: `.`) |

### Protocol Options

| ID | Name | Description |
|----|------|-------------|
| 0 | Audible Normal | Standard audio range, most reliable |
| 3 | Ultrasound | Near-ultrasonic, less audible but shorter range |

### Example Workflow

```bash
# Sender: compress and encode file to WAV
uv run python src/giggle_transfer/sender.py -i photo.jpg -m file -o transfer.wav

# Receiver: decode WAV file
uv run python src/giggle_transfer/receiver.py -m file -i transfer.wav -o ./
```