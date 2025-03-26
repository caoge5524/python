import matplotlib.pyplot as plt
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

# 初始化图表
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
line, = ax.plot([], [], lw=2)
ax.set_title('Real time line chart')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')

# 文件变动处理器
class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if "huise.txt" in event.src_path:
            time.sleep(1.5)
            # 等待文件更新完成
            update_plot()

# 更新图表函数
def update_plot():
    lib1.load()
    arr = lib1.get_array()
    length = lib1.get_array_length()
    y = [arr[i + 1] for i in range(length) if arr[i + 1] > 0]
    x = [i+1 for i in range(length)]
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view()
    plt.draw()

# 初始化数据
update_plot()

# 启动文件监听
observer = Observer()
observer.schedule(FileChangeHandler(), path=".", recursive=False)
observer.start()

try:
    plt.show()
except KeyboardInterrupt:
    observer.stop()
observer.join()