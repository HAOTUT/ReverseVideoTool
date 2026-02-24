<<<<<<< HEAD
import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

def reverse_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        messagebox.showerror("错误", "无法打开视频！")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in reversed(frames):
        out.write(frame)
    out.release()
    messagebox.showinfo("完成", f"视频已保存：\n{output_path}")

def select_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv"), ("所有文件", "*.*")]
    )
    if not filepath:
        return

    name, ext = os.path.splitext(filepath)
    output_path = f"{name}_倒放{ext}"
    reverse_video(filepath, output_path)

# ------------------- GUI 主界面 -------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("视频倒放工具")
    root.geometry("400x180")

    tk.Label(root, text="视频倒放工具", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="选择视频并开始倒放", command=select_file, width=25, height=2).pack(pady=10)

    root.mainloop()
=======
import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

def reverse_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        messagebox.showerror("错误", "无法打开视频！")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in reversed(frames):
        out.write(frame)
    out.release()
    messagebox.showinfo("完成", f"视频已保存：\n{output_path}")

def select_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv"), ("所有文件", "*.*")]
    )
    if not filepath:
        return

    name, ext = os.path.splitext(filepath)
    output_path = f"{name}_倒放{ext}"
    reverse_video(filepath, output_path)

# ------------------- GUI 主界面 -------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("视频倒放工具")
    root.geometry("400x180")

    tk.Label(root, text="视频倒放工具", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="选择视频并开始倒放", command=select_file, width=25, height=2).pack(pady=10)

    root.mainloop()
>>>>>>> e67513580f1214f9a7897522ec04a8004c426c5d
