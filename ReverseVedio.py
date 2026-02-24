import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys
import tempfile


# ========== 核心：自动下载/调用FFmpeg（无需手动装） ==========
def get_ffmpeg():
    """自动获取FFmpeg，优先用系统的，没有则用内置的"""
    if getattr(sys, 'frozen', False):
        # 打包后，FFmpeg在exe同目录
        ffmpeg_path = os.path.join(os.path.dirname(sys.executable), "ffmpeg.exe")
    else:
        # 开发模式，用同目录的ffmpeg.exe
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

    # 检查FFmpeg是否存在
    if not os.path.exists(ffmpeg_path):
        messagebox.showerror("错误", "请将ffmpeg.exe放在程序同目录！")
        sys.exit(1)
    return ffmpeg_path


def reverse_video():
    input_path = entry_video.get().strip()
    output_dir = entry_folder.get().strip()

    if not input_path or not output_dir:
        messagebox.showwarning("提示", "请选择视频和保存文件夹！")
        return

    # 生成输出文件名
    file_name = os.path.basename(input_path)
    name, _ = os.path.splitext(file_name)
    output_path = os.path.join(output_dir, f"{name}_倒放.mp4")

    # 禁用按钮
    btn_start.config(state=tk.DISABLED)
    root.update()

    try:
        # FFmpeg核心命令：音视频同步倒放（Python 3.13完全兼容）
        cmd = [
            get_ffmpeg(),
            "-i", input_path,
            "-vf", "reverse",  # 视频倒放
            "-af", "areverse",  # 音频倒放
            "-y",  # 覆盖已有文件
            "-c:v", "libx264",
            "-c:a", "aac",
            output_path
        ]

        # 执行命令（隐藏黑窗口）
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        messagebox.showinfo("成功", f"倒放完成！\n{output_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("失败", f"FFmpeg执行错误：{e.stderr.decode('gbk', errors='ignore')}")
    except Exception as e:
        messagebox.showerror("失败", f"未知错误：{str(e)}")
    finally:
        # 恢复按钮
        btn_start.config(state=tk.NORMAL)


# ========== UI界面 ==========
def select_video():
    path = filedialog.askopenfilename(
        title="选择视频",
        filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv")]
    )
    if path:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, path)


def select_folder():
    path = filedialog.askdirectory(title="选择保存文件夹")
    if path:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, path)


# 主窗口
if __name__ == "__main__":
    root = tk.Tk()
    root.title("视频倒放工具（Python3.13兼容版）")
    root.geometry("600x150")

    # 视频选择
    tk.Label(root, text="待倒放视频：").place(x=20, y=20)
    entry_video = tk.Entry(root, width=50)
    entry_video.place(x=100, y=20)
    tk.Button(root, text="选择", command=select_video).place(x=520, y=17)

    # 文件夹选择
    tk.Label(root, text="保存文件夹：").place(x=20, y=60)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.place(x=100, y=60)
    tk.Button(root, text="选择", command=select_folder).place(x=520, y=57)

    # 开始按钮
    btn_start = tk.Button(root, text="开始倒放（音视频同步）", command=reverse_video,
                          bg="green", fg="white", font=("微软雅黑", 12))
    btn_start.place(x=200, y=90)

    root.mainloop()