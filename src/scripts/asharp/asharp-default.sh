#!/bin/bash

touch src/main.adb
touch src/project.gpr
touch .gitignore
touch README.md

cat > src/main.adb << EOF
with Ada.Text_IO;
use Ada.Text_IO;
procedure Hello_Dotnet is
begin
 Put_Line(Item => "Hello, world!");
end Hello_Dotnet;
EOF

cat > src/project.gpr << EOF
project MyProject is
   for Main use ("main.adb");
end MyProject;
EOF

cat > .gitignore << EOF

# Build output

bin/
obj/

# User-specific files

*.user
*.suo

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

echo "[DEnv A# Default] Created 4 files: src/main.adb, src/project.gpr, .gitignore, README.md"
