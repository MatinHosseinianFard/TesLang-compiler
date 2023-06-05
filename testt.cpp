#include <iostream>
#include <vector>

void test(std::vector<int> A) {
    std::cout << A[0] << std::endl;
}

int main() {
    std::vector<int> x;
    x.push_back(3);
    std::cout << x.at(1) << std::endl;
    std::cout << 5;
    // test(x);
    return 0;
}
