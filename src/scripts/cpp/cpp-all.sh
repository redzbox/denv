#!/bin/bash

mkdir -p build
mkdir -p src
mkdir -p include

echo "[DEnv C++ All] Created 3 directories: build, src, include"

touch src/main.cpp
touch run.sh

cat > src/main.cpp << EOF
#include <iostream>

using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}

EOF

cat > run.sh << EOF
#!/bin/bash

g++ -Wall -Wextra -Werror -std=c++11 src/main.cpp -o build/main
./build/main

EOF

echo "[DEnv C++ All] Created 2 files: src/main.cpp, run.sh"
