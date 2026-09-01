import ggwave
import pyaudio
import wave
import os
import sys
import time
import zlib
import argparse

def send_file_ultra(input_file, mode, output_wav, protocol_id=0):
    if not os.path.exists(input_file):
        print(f"[!] 文件不存在: {input_file}")
        return

    file_name = os.path.basename(input_file)

    with open(input_file, "rb") as f:
        raw_bytes = f.read()

    orig_size = len(raw_bytes)

    # 1. 在内存中进行最高级别 zlib 压缩
    compressed_bytes = zlib.compress(raw_bytes, level=9)
    comp_size = len(compressed_bytes)
    ratio = (1 - comp_size / orig_size) * 100

    print(f"[+] 启动 Ultra 传输 | 文件: {file_name}")
    print(f"    - 原始大小: {orig_size} Bytes")
    print(f"    - 压缩后大小: {comp_size} Bytes (体积压缩了 {ratio:.1f}%)")

    sample_rate = 48000
    pcm_frames = []

    # 2. 针对 ggwave 的最佳 Chunk 长度设置为 16-24 字节（防止底层的过载拆包）
    chunk_size = 136

    payloads = []
    # 标头带上 ZLIB 压缩标记以及解压尺寸
    payloads.append(f"HDR_Z:{file_name}:{orig_size}:{comp_size}".encode('utf-8'))

    for i in range(0, comp_size, chunk_size):
        chunk = compressed_bytes[i:i + chunk_size]
        payloads.append(b"DAT:" + chunk)

    payloads.append(b"EOF:END")
    payloads.append(b"EOF:END")

    print(f"[+] 正在进行声波调制 (使用 Protocol {protocol_id})...")
    start_time = time.time()

    for pld in payloads:
        # volume 设为 80 增强信噪比
        wf = ggwave.encode(pld, protocolId=protocol_id, volume=80)
        if wf:
            pcm_frames.append(wf)

    full_pcm_data = b"".join(pcm_frames)
    audio_duration = len(full_pcm_data) / (sample_rate * 4)

    effective_speed = orig_size / audio_duration if audio_duration > 0 else 0

    print(f"[✓] 声波调制完成！")
    print(f"    - 音频总时长: {audio_duration:.1f} 秒")
    print(f"    - **等效实际传输速率: {effective_speed:.1f} Bytes/s**")

    if mode == "sound":
        print("\n[+] 正在通过扬声器播放...")
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        stream.write(full_pcm_data, len(full_pcm_data) // 4)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(f"\n[✓] 播放完成！总用时: {time.time() - start_time:.1f} 秒")

    elif mode == "file":
        with wave.open(output_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(4)
            wf.setframerate(sample_rate)
            wf.writeframes(full_pcm_data)
        print(f"\n[✓] WAV 文件保存至: {output_wav}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="文件路径")
    parser.add_argument("-m", "--mode", choices=["sound", "file"], default="sound")
    parser.add_argument("-o", "--output", default="ultra_output.wav")
    parser.add_argument("-p", "--protocol", type=int, default=0, help="推荐: 0 (Audible Normal) 或 3 (Ultrasound Normal)")

    args = parser.parse_args()
    send_file_ultra(args.input, args.mode, args.output, args.protocol)