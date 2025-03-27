import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import ctypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# 加载共享库
lib1 = ctypes.CDLL("./huise.dll")
# 确认返回类型
lib1.load.restype = None
lib1.get_array.restype = ctypes.POINTER(ctypes.c_int)
lib1.get_array_length.restype = ctypes.c_size_t

# 初始化图表（增大画布尺寸）
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#f5f5f5')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'

# 设置图表样式
ax.set_facecolor('#fafafa')  # 绘图区背景色
ax.set_title('Real-time line chart', fontsize=16, pad=20, color='#2f2f2f')
ax.set_xlabel('X axis', fontsize=12, labelpad=10, color='#444444')
ax.set_ylabel('Y axis', fontsize=12, labelpad=10, color='#444444')

# 设置坐标轴样式
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#808080')
ax.spines['left'].set_color('#808080')
ax.tick_params(axis='both', colors='#666666', labelsize=10)

# 添加网格线
ax.grid(True, linestyle='--', linewidth=0.5, color='#c0c0c0', alpha=0.7)

# 创建线条（深蓝色带阴影效果）
line, = ax.plot([], [], lw=2.5, color='#1f77b4', 
               marker='o', markersize=4, markerfacecolor='#ffffff',
               markeredgewidth=1, markeredgecolor='#1f77b4',
               path_effects=[path_effects.withStroke(linewidth=3, foreground="#1f77b480")])

# 文件变动处理器
class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if "huise.txt" in event.src_path:
            time.sleep(1.5)
            update_plot()

# 更新图表函数（修复x/y长度问题）
def update_plot():
    lib1.load()
    arr = lib1.get_array()
    length = lib1.get_array_length()
    
    # 同时过滤x和y数据
    valid_indices = [i for i in range(length) if arr[i+1] > 0]
    x = [i+1 for i in valid_indices]
    y = [arr[i+1] for i in valid_indices]
    
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view()
    ax.set_xlim(left=0, right=max(x)+1 if x else 10)  # 确保空数据时正常显示
    plt.draw()

# 初始化数据
update_plot()

# 启动文件监听
observer = Observer()
observer.schedule(FileChangeHandler(), path=".", recursive=False)
observer.start()

try:
    plt.tight_layout(pad=3)  # 优化布局
    plt.show()
except KeyboardInterrupt:
    observer.stop()
observer.join()