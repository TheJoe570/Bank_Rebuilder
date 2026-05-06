
# SC2 Replay Bank Rebuilder

A Windows desktop Python tool for extracting player/bank information from StarCraft II `.SC2Replay` files and rebuilding SC2 bank files using `s2repdump`.

## Overview

SC2 Replay Bank Rebuilder lets you drag and drop a replay file into a GUI, view detected player/bank information, and export rebuilt bank files to a folder you choose.

The main script is:

```text
bank_recovery.py
Features
Drag and drop .SC2Replay files into the app
Display extracted player information
Display detected bank information
Rebuild bank files using s2repdump
Choose a custom output directory
Manual Save Banks button
Requirements

You need:

Windows
Python 3.x
s2repdump
Python packages from requirements.txt

Python dependencies may include:

tkinter
tkinterdnd2
s2protocol
mpyq
argparse

Important: s2repdump must be available in your Windows System Variables PATH.
If Windows cannot find s2repdump, the app may open, but replay processing will fail.

Step 1 — Install Python

Install Python 3 from:

https://www.python.org/downloads/

During installation, check:

Add Python to PATH

After installing, open PowerShell or Command Prompt and run:

py --version

You should see a Python 3.x version.

Step 2 — Download or clone this project

Place the project somewhere easy to access, for example:

C:\Users\YOUR_NAME\Desktop\Projects\Bank_Rebuilder

The folder should contain files like:

bank_recovery.py
requirements.txt
tools\
Step 3 — Open a terminal in the project folder

Open the Bank_Rebuilder folder in File Explorer.

Click the folder path bar at the top, type:

cmd

Then press Enter.

This opens Command Prompt directly inside the project folder.

You can also use PowerShell:

cd C:\Users\YOUR_NAME\Desktop\Projects\Bank_Rebuilder
Step 4 — Create a virtual environment

From inside the Bank_Rebuilder folder, run:

py -m venv venv

This creates a local Python environment in a folder named:

venv
Step 5 — Activate the virtual environment
PowerShell
.\venv\Scripts\Activate.ps1

If PowerShell blocks activation, run this once:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Then activate again:

.\venv\Scripts\Activate.ps1
Command Prompt
venv\Scripts\activate.bat

When activated, your terminal should show:

(venv)
Step 6 — Install dependencies

With the virtual environment activated, run:

python -m pip install --upgrade pip
pip install -r requirements.txt
Step 7 — Install or locate s2repdump

This project requires s2repdump.

Check if Windows can already find it:

where s2repdump

If it returns a path, you are good.

Example:

C:\SomeFolder\s2repdump.exe

If it says no files were found, you need to add the folder containing s2repdump.exe to your Windows PATH.

Step 8 — Add s2repdump to Windows PATH
Find the folder that contains s2repdump.exe.
Copy the folder path.
Press the Windows key.
Search for:
Environment Variables
Open:
Edit the system environment variables
Click:
Environment Variables
Under System variables, find:
Path
Click Edit.
Click New.
Paste the folder path containing s2repdump.exe.
Click OK on all windows.
Close and reopen your terminal.

Then test again:

where s2repdump
Step 9 — Run the app

With the virtual environment activated, run:

python .\bank_recovery.py

A GUI window should open titled:

SC2 Replay Bank Rebuilder
Step 10 — Use the app
Drag a .SC2Replay file onto the black drop area.
The app will process the replay.
Player and bank information should appear in the window.
Choose an output folder when prompted.
The app will rebuild/export bank files.
You can also use the Save Banks button after a replay has been loaded.
Quick Start

After everything is installed once, normal startup is:

cd C:\Users\YOUR_NAME\Desktop\Projects\Bank_Rebuilder
.\venv\Scripts\Activate.ps1
python .\bank_recovery.py

For Command Prompt:

cd C:\Users\YOUR_NAME\Desktop\Projects\Bank_Rebuilder
venv\Scripts\activate.bat
python bank_recovery.py
Troubleshooting
The app opens but replay processing fails

Check that s2repdump works:

where s2repdump

If Windows cannot find it, add s2repdump.exe to PATH.

ModuleNotFoundError

Example:

ModuleNotFoundError: No module named 'tkinterdnd2'

Fix:

pip install -r requirements.txt

Or manually:

pip install tkinterdnd2
PowerShell will not activate the virtual environment

Run:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Then:

.\venv\Scripts\Activate.ps1
Drag and drop does not work

Try:

Dragging the file directly onto the large black drop area
Making sure the replay file ends in .SC2Replay
Restarting the app
Running from a normal user terminal, not Administrator
s2repdump works in one terminal but not another

Close and reopen the terminal after editing PATH.

Windows does not always refresh PATH in terminals that were already open.

Developer Notes

The app uses:

tkinter for the GUI
tkinterdnd2 for drag and drop
subprocess to run s2repdump
threading to avoid freezing the GUI during processing

Main s2repdump commands used by the project:

s2repdump -d players -d banks <replay_file>
s2repdump --bank-rebuild --out <output_folder> <replay_file>
Author

Created by TheJoe570 / Joe.

S2Repdump credit: Talv.

License

This project is licensed under the MIT License. See License.txt for details.