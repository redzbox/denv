#!/bin/bash

mkdir -p build
mkdir -p src
mkdir -p include

echo "[DEnv C++ Default] Created 3 directories: build, src, include"

touch src/main.cpp
touch run.sh
touch .gitignore

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

g++ src/main.cpp -o build/main
./build/main

EOF

cat > .gitignore << EOF

# Build output

*.o
*.obj
*.out
*.exe
*.a
*.so
*.dll

# CMake

build/
CMakeFiles/
CMakeCache.txt
cmake_install.cmake
Makefile
compile_commands.json

# Editor files

.vscode/
.idea/

# OS files

.DS_Store
Thumbs.db

EOF

echo "[DEnv C++ Default] Created 3 files: src/main.cpp, run.sh, .gitignore"
