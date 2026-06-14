#!/bin/bash

mkdir -p src
echo "[DEnv Python Default] Created 1 directory: src"

touch src/main.py
touch run.sh

cat > src/main.py << EOF
print("Hello, World!")
EOF

cat > run.sh << EOF
#!/bin/bash

python3 src/main.py

EOF

echo "[DEnv Python Default] Created 2 files: src/main.py, run.sh"
