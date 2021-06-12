#include <nowide/iostream.hpp>
#include <iostream>

int main() {
    nowide::cout << "Basic letters: \xd7\xa9-\xd0\xbc-\xce\xbd\n";
    nowide::cout << "East Asian Letters: \xe5\x92\x8c\xe5\xb9\xb3\n";
    nowide::cout << "Non-BMP letters: \xf0\x9d\x84\x9e" << std::endl;
}
