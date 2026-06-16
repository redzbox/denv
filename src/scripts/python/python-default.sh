#!/bin/bash

mkdir -p src
echo "[DEnv Python Default] Created 1 directory: src"

touch src/main.py
touch run.sh
touch .gitignore
touch README.md


cat > src/main.py << EOF
print("Hello, World!")
EOF

cat > run.sh << EOF
#!/bin/bash

python3 src/main.py

EOF

cat > .gitignore << EOF

# Byte-compiled files

**pycache**/
*.py[cod]

# Virtual environments

.venv/
venv/
env/

# Distribution

build/
dist/
*.egg-info/

# Environment variables

.env

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

echo "[DEnv Python Default] Created 4 files: src/main.py, run.sh, .gitignore, README.md"
