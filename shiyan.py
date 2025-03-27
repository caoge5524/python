import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import ctypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import panel as pn
import numpy as np
from threading import Lock

pn.extension()

# 加载共享库
lib1 = ctypes.CDLL("./huise.dll")
lib1.load.restype = None
lib1.get_array.restype = ctypes.POINTER(ctypes.c_int)
lib1.get_array_length.restype = ctypes.c_size_t

# 创建线程锁
lock = Lock()

class Dashboard:
    def __init__(self):
        # 初始化数据
        self.x = []
        self.y = []
        self.fig, self.ax = self.create_figure()
        self.stats = pn.widgets.StaticText(value='Statistics: Waiting for data...')
        self.alert = pn.pane.Alert(object='Threshold exceeded!', alert_type='danger', visible=False)

        # 创建控制面板
        self.refresh_rate = pn.widgets.IntSlider(name='Refresh Rate (ms)', value=1000, start=500, end=5000)
        self.alert_threshold = pn.widgets.FloatInput(name='Alert Threshold', value=1000, step=10)

        # 仪表盘布局
        self.template = pn.template.FastListTemplate(
            title='Real-Time Monitoring Dashboard',
            sidebar=[pn.Column("## Controls", self.refresh_rate, self.alert_threshold)],
            main=[
                pn.Row(
                    pn.Column(self.stats, self.create_plot_pane()),
                    self.create_status_indicator()
                ),
                self.alert
            ],
            accent="#9acd32",
            header_background="#1f77b4"
        )
        
    def create_figure(self):
        """创建matplotlib图表"""
        fig, ax = plt.subplots(figsize=(12, 6), facecolor='#f5f5f5')
        plt.rcParams['font.family'] = 'Times New Roman, SimSun'
        ax.set_facecolor('#808080')
        ax.set_title('Real-time Data Stream', fontsize=16, pad=20, color='#9acd32')
        ax.set_xlabel('X axis', fontsize=12, labelpad=10, color='#9acd32')
        ax.set_ylabel('Y axis', fontsize=12, labelpad=10, color='#9acd32')
        ax.grid(True, linestyle='--', linewidth=0.5, color='#c0c0c0', alpha=0.7)
        self.line, = ax.plot([], [], lw=2.5, color='#fafafa', 
                           marker='o', markersize=4, markerfacecolor='#ffffff',
                           path_effects=[path_effects.withStroke(linewidth=3, foreground="#1f77b480")])
        return fig, ax

    def create_plot_pane(self):
        """将matplotlib图表转换为Panel组件"""
        return pn.pane.Matplotlib(self.fig, dpi=144, height=500)

    def create_status_indicator(self):
        """创建状态指示灯"""
        return pn.indicators.BooleanStatus(name='Data Status', value=False, color='danger', height=100, width=100)

    def update_data(self):
        """更新数据并刷新图表"""
        with lock:
            lib1.load()
            arr = lib1.get_array()
            length = lib1.get_array_length()
            
            valid_indices = [i for i in range(length) if arr[i+1] > 0]
            self.x = [i+1 for i in valid_indices]
            self.y = [arr[i+1] for i in valid_indices]
            
            # 更新图表
            self.line.set_data(self.x, self.y)
            self.ax.relim()
            self.ax.autoscale_view()
            self.ax.set_xlim(left=0, right=max(self.x)+1 if self.x else 10)
            
            # 更新统计信息
            average_value = np.mean(self.y) if self.y else 0
            stats_text = f"""
            Data Statistics:
            - Predicted Value: {self.y[-1] if self.y else 'N/A'}
            - Average: {average_value:.2f}
            - Max Value: {max(self.y) if self.y else 0}
            """
            self.stats.value = stats_text
            
            # 触发警报
            if self.y and max(self.y) > self.alert_threshold.value:
                self.alert.visible = True
                
    def start_watcher(self):
        """启动文件监听"""
        class FileHandler(FileSystemEventHandler):
            def __init__(self, dashboard):
                self.dashboard = dashboard

            def on_modified(self, event):
                if "huise.txt" in event.src_path:
                    time.sleep(1)
                    # 更新数据时间阻塞
                    self.dashboard.update_data()

        observer = Observer()
        observer.schedule(FileHandler(self), path=".", recursive=False)
        observer.start()
        return observer

# 初始化仪表盘
dashboard = Dashboard()
observer = dashboard.start_watcher()

# 添加定时刷新
def periodic_update():
    while True:
        dashboard.update_data()
        time.sleep(dashboard.refresh_rate.value / 1000)  # 动态读取刷新间隔

from threading import Thread
Thread(target=periodic_update, daemon=True).start()

# 启动仪表盘
dashboard.template.servable()

# 启动 Panel 服务器
pn.serve(dashboard.template, start=True, show=True)