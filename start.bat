@echo off
python -m venv myguiapp
call myguiapp/Scripts/activate.bat
pip install -r req/req.txt
python gui.py
