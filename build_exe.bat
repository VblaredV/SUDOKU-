@echo off
chcp 65001 >nul
title Сборка Sudoku BV
color 0A

echo ========================================
echo    СБОРКА SUDOKU BV - ФИНАЛЬНАЯ ВЕРСИЯ
echo ========================================
echo.

cd /d C:\Users\52\Desktop\sudoku_project

echo [1/5] Очистка старых файлов...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul
echo ✅ Готово
echo.

echo [2/5] Проверка шрифта...
if exist "assets\fonts\segoe-ui-emoji_0.ttf" (
    echo ✅ Шрифт найден: assets\fonts\segoe-ui-emoji_0.ttf
) else (
    echo ❌ Шрифт не найден! Положи шрифт в assets\fonts\
    pause
    exit /b
)
echo.

echo [3/5] Установка PyInstaller...
pip install pyinstaller --quiet
echo ✅ Готово
echo.

echo [4/5] Сборка EXE...
pyinstaller --onefile --windowed --name "SudokuBV" ^
  --add-data "assets;assets" ^
  --hidden-import pygame ^
  --hidden-import json ^
  --hidden-import os ^
  --hidden-import time ^
  --hidden-import datetime ^
  --hidden-import pathlib ^
  --collect-all pygame ^
  main.py
echo ✅ Готово
echo.

echo [5/5] Создание тестовой папки...
mkdir test_game 2>nul
copy dist\SudokuBV.exe test_game\ /y >nul
xcopy assets test_game\assets\ /e /i /q >nul
echo ✅ Готово
echo.

echo ========================================
echo    ✅ СБОРКА ЗАВЕРШЕНА!
echo ========================================
echo.
echo 📁 EXE файл: dist\SudokuBV.exe
echo 📁 Тестовая папка: test_game\
echo.
echo 🎮 Чтобы запустить тестовую версию:
echo    1. Открой папку test_game\
echo    2. Запусти SudokuBV.exe
echo.
pause