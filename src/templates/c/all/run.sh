#!/bin/bash

gcc -Wall -Wextra -Werror -std=c11 src/main.c -o build/main
./build/main
