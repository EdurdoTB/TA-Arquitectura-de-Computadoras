#!/bin/bash

# Script para la ejecución directa de los archivos .py y .c 

#nasm -f elf64 Arqui.asm -o arq.o
gcc -shared libreria.c -o validacion.so
python3 Main.py


