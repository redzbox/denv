#!/bin/bash

mkdir -p build
mkdir -p src
mkdir -p include

echo "[DEnv C All] Created 3 directories: build, src, include"

touch src/main.c
touch run.sh
touch .gitignore
touch README.md

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

cat > .gitignore << EOF

# Build Output

*.o
*.out
*.exe
*.a
*.so

# Debug symbols

*.dSYM/

# Editor files

.vscode/
.idea/

# OS files

.DS_Store
Thumbs.db

EOF

PROJECT_NAME=$(basename "$PWD")

cat > README.md << EOF
# $PROJECT_NAME

Project Setup from DEnv
EOF

echo "[DEnv C All] Created 4 files: src/main.c, run.sh, .gitignore, README.md"
