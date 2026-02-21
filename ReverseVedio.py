import os
import sys
import cv2
import numpy as np
from tkinter import Tk, filedialog

# ===================== 打包适配：获取资源路径 =====================
def resource_path(relative_path):
    """获取打包后文件的真实路径（解决PyInstaller路径问题）"""
    try:
        base_path = sys._MEIPASS  # 打包后的临时目录
    except Exception:
        base_path = os.path.abspath(".")  # 未打包时的当前目录
    return os.path.join(base_path, relative_path)

# ===================== 选择输入视频文件 =====================
def select_video_file():
    """弹出文件选择框，选择视频文件"""
    root = Tk()
    root.withdraw()  # 隐藏tkinter主窗口
    root.attributes('-topmost', True)  # 窗口置顶
    file_path = filedialog.askopenfilename(
        title="选择要倒放的视频文件",
        filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv"), ("所有文件", "*.*")]
    )
    if not file_path:
        print("未选择视频文件，程序退出！")
        sys.exit()
    return file_path

# ===================== 主逻辑 =====================
if __name__ == "__main__":
    # 1. 选择输入视频
    input_video_path = select_video_file()
    # 2. 生成输出路径（和原视频同目录，后缀加_reversed）
    video_dir = os.path.dirname(input_video_path)
    video_name = os.path.basename(input_video_path)
    name, ext = os.path.splitext(video_name)
    output_video_path = os.path.join(video_dir, f"{name}_reversed{ext}")

    # 3. 检查输入文件
    if not os.path.exists(input_video_path):
        print(f"错误：输入文件不存在！路径：{input_video_path}")
        input("按回车键退出...")
        sys.exit()

    # 4. 打开视频
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("错误：无法打开输入视频文件！")
        input("按回车键退出...")
        sys.exit()

    # 5. 获取视频属性
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    print(f"\n输入视频信息：")
    print(f"  路径：{input_video_path}")
    print(f"  总帧数：{frame_count}")
    print(f"  帧率：{fps}")
    print(f"  分辨率：{width}x{height}")

    # 6. 设置编码器（适配不同格式）
    fourcc = None
    if ext.lower() == ".mp4":
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    elif ext.lower() == ".avi":
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 默认MP4

    # 7. 创建VideoWriter
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=True)
    if not out.isOpened():
        print("错误：无法创建视频写入对象！")
        cap.release()
        input("按回车键退出...")
        sys.exit()

    # 8. 读取并倒序写入
    print("\n正在读取视频帧...")
    frames_list = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames_list.append(frame)

    print("正在写入倒放视频...")
    for idx in range(len(frames_list)-1, -1, -1):
        frame = frames_list[idx]
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, (width, height))
        out.write(frame)
        if idx % max(1, frame_count//10) == 0:  # 按10等分打印进度
            progress = (len(frames_list)-idx)/len(frames_list)*100
            print(f"  进度：{progress:.1f}% (剩余帧数：{idx})")
        # 预览（可选）
        cv2.imshow("视频倒放中（按ESC退出）", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 9. 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"\n✅ 倒放视频已保存至：")
    print(f"  {output_video_path}")
    input("按回车键退出...")  # 防止程序运行完直接关闭