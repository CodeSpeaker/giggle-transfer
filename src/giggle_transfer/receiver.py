import traceback

import ggwave
import pyaudio
import wave
import os
import sys
import time
import zlib
import argparse

def receive_file_ultra(mode, input_wav, output_dir="."):
    sample_rate = 48000
    frames_per_buffer = 1024

    instance = ggwave.init()

    file_handle = None
    file_name = ""
    orig_size = 0
    comp_size = 0
    compressed_data_chunks = []
    start_time = None

    def process_decoded_res(res):
        nonlocal file_name, orig_size, comp_size, compressed_data_chunks, start_time

        if res is None or len(res) == 0:
            return False

        # Header 提取
        if res.startswith(b"HDR_Z:"):
            try:
                header_str = res.decode('utf-8', errors='ignore')
                _, file_name, orig_sz, comp_sz = header_str.split(":")
                orig_size = int(orig_sz)
                comp_size = int(comp_sz)
                compressed_data_chunks = []
                start_time = time.time()
                print(f"\n[!] 捕获文件头! 原始: {orig_size} B | 压缩后: {comp_size} B")
            except Exception as e:
                print(f"\n[!] Header 解析失败: {e}")
            return False

        # EOF 结束标记与解压写入
        if res == b"EOF:END":
            elapsed = time.time() - start_time if start_time else 1
            full_compressed_data = b"".join(compressed_data_chunks)

            try:
                # 解压恢复原始数据
                decompressed_data = zlib.decompress(full_compressed_data)
                save_path = f"{output_dir}/received_{file_name}"

                with open(save_path, "wb") as f:
                    f.write(decompressed_data)

                speed = len(decompressed_data) / elapsed if elapsed > 0 else 0
                print(f"\n\n[✓] 文件接收并成功解压！")
                print(f"    - 保存路径: {save_path}")
                print(f"    - 传输总用时: {elapsed:.1f} 秒")
                print(f"    - **等效实际速度: {speed:.1f} Bytes/s**")
                return True
            except Exception as e:
                print(f"\n[!] 解压数据失败，可能传输存在丢包: {e}")
                return True

        # DAT 模块收集
        if res.startswith(b"DAT:"):
            raw_chunk = res[4:]
            compressed_data_chunks.append(raw_chunk)

            curr_comp_bytes = sum(len(c) for c in compressed_data_chunks)
            elapsed = time.time() - start_time if start_time else 1
            progress = (curr_comp_bytes / comp_size * 100) if comp_size > 0 else 0

            print(f"\r[<] 接收进度: {progress:.1f}% [{curr_comp_bytes}/{comp_size} B]", end="")

        return False

    if mode == "mic":
        print("[+] 极速接收: [麦克风模式]")
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, input=True, frames_per_buffer=frames_per_buffer)
        print("[+] 等待声波信号...\n")
        try:
            while True:
                data = stream.read(frames_per_buffer, exception_on_overflow=False)
                res = ggwave.decode(instance, data)
                if process_decoded_res(res):
                    break
        except KeyboardInterrupt:
            print("\n[!] 中断。")
        finally:
            ggwave.free(instance)
            stream.stop_stream()
            stream.close()
            p.terminate()

    elif mode == "file":
        if not os.path.exists(input_wav):
            print(f"[!] 文件不存在: {input_wav}")
            return
        with wave.open(input_wav, "rb") as wf:
            start_time = time.time()
            while True:
                data = wf.readframes(frames_per_buffer)
                if not data:
                    break
                res = ggwave.decode(instance, data)
                if process_decoded_res(res):
                    break
        ggwave.free(instance)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", choices=["mic", "file"], default="mic")
    parser.add_argument("-i", "--input", default="ultra_output.wav")
    parser.add_argument("-o", "--outdir", default=".")

    args = parser.parse_args()
    receive_file_ultra(args.mode, args.input, args.outdir)
