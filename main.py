import matplotlib.pyplot as plt
import ctypes

# 加载共享库
lib1 = ctypes.CDLL("./huise.dll")  # Windows

# 定义函数参数和返回类型
lib1.get_array.restype = ctypes.POINTER(ctypes.c_int)
lib1.get_array_length.restype = ctypes.c_size_t

# 获取数组指针和长度
arr_ptr = lib1.get_array()
length = lib1.get_array_length()
print("length:", length,"arr_ptr:", arr_ptr)
# 将指针转换为 Python 列表
arr = [arr_ptr[i+1] for i in range(length)]

# 设置字体
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
# 绘制折线图
x = [i+1 for i in range(length)]
y = arr
plt.plot(x, y)

# 添加标题和坐标轴标签
plt.title('折线图示例')
plt.xlabel('X轴')
plt.ylabel('Y轴')

# 显示图形
plt.show()