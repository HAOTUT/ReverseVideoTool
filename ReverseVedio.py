import os
import cv2
import numpy as np

# ===================== 1. 核心参数修复 =====================
# 输入路径：统一用双反斜杠，确保路径正确
input_video_path = "A:\\MyPythonProject\\pythonProject\\data\\Vedio\\test1.mp4"
# 输出路径：补充文件名+后缀（.mp4），统一双反斜杠
output_video_path = "A:\\MyPythonProject\\pythonProject\\data\\ReversedVedio\\reversed_test1.mp4"

# ===================== 2. 前置检查 =====================
# 检查输入文件是否存在
if not os.path.exists(input_video_path):
    print(f"错误：输入文件不存在！路径：{input_video_path}")
    exit()

# 检查输出文件夹是否存在，不存在则创建（避免路径不存在报错）
output_dir = os.path.dirname(output_video_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"提示：自动创建输出文件夹：{output_dir}")

# ===================== 3. 打开视频并获取属性 =====================
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    print("错误：无法打开输入视频文件！")
    exit()

# 获取视频属性（保留原始值，避免类型转换导致的问题）
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率不转int，用原始浮点值更兼容
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

print(f"输入视频信息：")
print(f"  总帧数：{frame_count}")
print(f"  帧率：{fps}")
print(f"  分辨率：{width}x{height}")

# ===================== 4. 编码器和VideoWriter修复 =====================
# 强制指定MP4编码器（避免适配逻辑失效）
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4v是MP4最兼容的编码器
# 创建VideoWriter：分辨率严格用(width, height)，和帧一致
out = cv2.VideoWriter(
    output_video_path,
    fourcc,
    fps,
    (width, height),  # 修复：用原始宽高，不交换
    isColor=True
)

# 检查Writer是否创建成功
if not out.isOpened():
    print("错误：无法创建视频写入对象！尝试以下方案：")
    print(f"  1. 更换输出格式为AVI：{output_video_path.replace('.mp4', '.avi')}")
    print(f"  2. 检查输出路径权限：{output_dir}")
    cap.release()
    exit()

# ===================== 5. 读取并倒序写入帧 =====================
frames_list = []
print("正在读取原视频帧...")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames_list.append(frame)

print("正在写入倒放视频...")
for idx in range(len(frames_list) - 1, -1, -1):
    frame = frames_list[idx]
    # 帧分辨率校验：确保和Writer一致
    if frame.shape[1] != width or frame.shape[0] != height:
        frame = cv2.resize(frame, (width, height))
    out.write(frame)

    # 打印进度
    if idx % 10 == 0:  # 你的视频只有135帧，改每10帧打印一次
        print(f"  剩余待写入帧数：{idx}")

    # 实时预览（按ESC退出）
    cv2.imshow("Reversed Video", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# ===================== 6. 释放资源 =====================
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"\n✅ 倒放视频保存成功！路径：{output_video_path}")