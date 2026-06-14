#!/bin/bash

mkdir -p src
mkdir -p obj
mkdir -p bin
echo "[DEnv C# Default] Created 3 directories: src, obj, bin"

touch src/Program.cs
touch src/MyProject.csproj
touch run.sh

cat > src/Program.cs << EOF
using System;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
EOF

cat > src/MyProject.csproj << EOF
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

</Project>
EOF



echo "[DEnv C# Default] Created 2 files: src/Program.cs, src/MyProject.csproj"
