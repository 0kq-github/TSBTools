:pyinstaller TSBTools.py --noconsole --onefile --icon=tsb.ico
:pyarmor pack -e " --noconsole --onefile --icon=tsb.ico" TSBTools.py
python -m PyInstaller TSBTools.py --noconsole --onefile --icon=tsb.ico