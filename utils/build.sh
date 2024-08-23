#!/usr/bin/env bash
pyinstaller --onefile --icon=icon.ico .\infoedukascrape.py
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.png;." .\infoedukascrape_gui.py