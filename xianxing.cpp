#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int real_day = 14;
int count[] = {0,46,52,53,54,56,60,70,74,65,67,89,97,67,56};
// 假设我们有一个结构体存储样本数据
typedef struct {
    int x;
    int y;// 假设x是天数，y是包裹数量
} Sample;

// 计算均值
double calculate_mean(double* arr, int cnt) {
    double sum = 0.0;
    for (int i = 0; i < cnt; ++i) {
        sum += arr[i];
    }
    return sum / cnt;
}

// 计算线性回归系数
void linear_regression(Sample* samples, int sample_count, double* W, double* b) {
    int sum_x = 0, sum_y = 0, sum_xy = 0, sum_xx = 0;
    
    for (int i = 0; i < sample_count; ++i) {
        int xi = samples[i].x;
        int yi = samples[i].y;
        sum_x += xi;
        sum_y += yi;
        sum_xy += xi * yi;
        sum_xx += xi * xi;
    }
 
    *W = (double)(sample_count * sum_xy - sum_x * sum_y) / (sample_count * sum_xx - sum_x * sum_x);
    *b = (double)sum_y / sample_count - (*W * sum_x) / sample_count;
}

// 预测函数
double predict_y(double W, double b, int x) {
    return W * x + b;
}
int main(){
    Sample data[366];
    for (int i = 0; i < real_day; i++)
    {
        data[i] = { i + 1, count[i+1] } ;
    }
    // 数据点数量
    double W, b;

    // 计算线性回归系数
    linear_regression(data, real_day, &W, &b);
    
    // printf("Slope (W): %.2f\n", W);
    // printf("Intercept (b): %.2f\n", b);
    
    // 预测
    int new_x = real_day + 1; // 预测下一天的包裹数量
    double predicted_y = predict_y(W, b, new_x);
    printf("The estimated number of packages is:%.2f",predicted_y);
    // printf("Predicted  for x = %.1f: %.2f\n", new_x, predicted_y);
}