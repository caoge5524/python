#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

int main() {
    // 初始化随机数种子
    std::srand(std::time(nullptr));

    // 打开文件 "huise.txt" 以写入数据
    std::ofstream file("huise.txt");
    if (!file.is_open()) {
        std::cerr << "无法打开文件 huise.txt" << std::endl;
        return 1;
    }

    // 写入 120 行随机整数数据
    for (int i = 0; i < 120; ++i) {
        int random_number = std::rand() % 300 + 200; 
        file << random_number << std::endl;
    }

    file.close();
    std::cout << "已成功向 huise.txt 写入 120 行数据。" << std::endl;

    return 0;
}