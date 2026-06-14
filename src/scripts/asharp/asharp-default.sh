#!/bin/bash

touch src/main.adb
touch src/project.gpr
touch run.sh

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

echo "[DEnv A# Default] Created 2 files: src/main.adb, src/project.gpr"
