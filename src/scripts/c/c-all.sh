#!/bin/bash

mkdir -p build
mkdir -p src
mkdir -p include

echo "[DEnv C All] Created 3 directories: build, src, include"

touch src/main.c
touch run.sh

cat > src/main.c << EOF
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}

EOF

cat > run.sh << EOF
#!/bin/bash

gcc -Wall -Wextra -Werror -std=c11 src/main.c -o build/main
./build/main

EOF

echo "[DEnv C All] Created 2 files: src/main.c, run.sh"
