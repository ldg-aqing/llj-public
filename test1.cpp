#include <iostream>
using namespace std;

// 计算斐波那契数列的第 n 项（递归）
int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int n;
    cout << "请输入一个正整数 n：";
    cin >> n;
    cout << "斐波那契第 " << n << " 项是：" << fibonacci(n) << endl;
    return 0;
}
