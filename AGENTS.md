# AGENTS.md

Small Python project for audio-based file transfer using ggwave (acoustic modem).

## Directory structure

- `src/giggle_transfer/` — Python package with `__init__.py`, `sender.py`, `receiver.py`
- Package name uses **underscore** (`giggle_transfer`), **not** hyphen (`giggle-transfer`). The build failed on `uv sync` when the directory was named with a hyphen.

## Requirements

- Python 3.13+ (see `.python-version`)
- `uv` as package manager; PyPI mirror configured to `pypi.tuna.tsinghua.edu.cn`
- System PortAudio library:
  - macOS: `brew install portaudio`
  - Linux: `apt install portaudio19-dev`
  - Windows: follow [PyAudio Windows guide](https://pypi.org/project/PyAudio/)
- Python dependencies: `ggwave>=0.4.3`, `pyaudio>=0.2.14`

## Commands

```bash
# Install/resolve dependencies
uv sync

# Send a file via speaker (sound mode)
uv run python src/giggle_transfer/sender.py -i <file> -m sound

# Send a file to WAV
uv run python src/giggle_transfer/sender.py -i <file> -m file -o output.wav

# Receive via microphone
uv run python src/giggle_transfer/receiver.py -m mic

# Receive from WAV file
uv run python src/giggle_transfer/receiver.py -m file -i <input.wav> -o <output_dir>
```

## Notes

- Two EOF markers are sent intentionally for reliability
- Protocol 0 = audible sound, protocol 3 = ultrasound
- All user-facing output and comments use Chinese (zh-CN)