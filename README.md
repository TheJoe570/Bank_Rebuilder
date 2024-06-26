# Bank_Rebuilder
GUI tool for extracting UAC (sc2) Bank information from .SC2Replay file
# SC2 Replay Bank Rebuilder

##
##
pip install -r requirements.txt     (You must be in the Bank_Rebuilder directory.)
First and foremost.
Second, s2repdump MUST be in your System Variables PATH. click edit and add a new path. It will open Edit environment variables tab.


## Overview
SC2 Replay Bank Rebuilder is a Python application designed to extract players and banks information from StarCraft II replay files (.SC2Replay) and rebuild bank files from the extracted data.

## Features
- Drag and drop functionality to easily process replay files.
- Display extracted player and bank information.
- Rebuild bank files with user-selected output directory.
- Manual "Save Banks" button to allow users to save banks without rebuilding.

## Requirements
- Python 3.x
- tkinter
- tkinterdnd2
- s2protocol
- s2repdump    *******
- Mpyq
- Argparse
***** By adding the directory containing s2repdump to the Open Environment Variables (PATH variable), you ensure that it can be executed from any location in the Command Prompt or any other application without specifying its full path.

## Installation
1. Clone or download the repository to your local machine.
2. Install the required dependencies: 
***** To install the dependencies open the Bank_Rebuilder folder and click the path field and type CMD. This will open a terminal in this directory. You can then do the pip install command:
pip install -r requirements.txt

## Usage
1. Run the `Test bank app.py` script.
2. Drag and drop a .SC2Replay file onto the application window.
3. The application will process the file and display extracted information.
4. Optionally, rebuild banks by selecting an output directory.
5. Alternatively, use the "Save Banks" button to manually save banks.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/my-feature`).
6. Create a new Pull Request.

## Author
- TheJoe570  "Joe"
 *S2Repdump -Talv

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
