This is a read me for how to run and analyze the code

The easiest way to run this code would be to download an IDE (Integrated Development Environment). I use Visual Studio Code, here's the link:
https://code.visualstudio.com/download

There are options to download for Mac or Windows. You then need to install the extension for python, at this link:
https://marketplace.visualstudio.com/items?itemName=ms-python.python

You then need to install a python interpreter. This is different for Windows and Mac.

Windows:
Install Python from python.org. You can typically use the Download Python button that appears first on the page to download the latest version.

Note: If you don't have admin access, an additional option for installing Python on Windows is to use the Microsoft Store. The Microsoft Store provides installs of Python 3.7 and Python 3.8. Be aware that you might have compatibility issues with some packages using this method.

For additional information about using Python on Windows, see Using Python on Windows at Python.org

macOS
The system install of Python on macOS is not supported. Instead, an installation through Homebrew is recommended. To install Python using Homebrew on macOS use brew install python3 at the Terminal prompt.

Note On macOS, make sure the location of your VS Code installation is included in your PATH environment variable. See these setup instructions for more information.

THIS TUTORIAL HAS MORE INSTRUCTIONS:
https://code.visualstudio.com/docs/python/python-tutorial

If you have questions regarding the tutorial, please reach out.

In order to run the code, you'll need to save the folder and open it in VS Code (File --> Open.... --> click on file)
Then, in the terminal, you'll need to enter the following to import the packages needed:

MAC:

brew install networkx
brew install matplotlib
brew install xlrd
brew install csv

WINDOWS:
1. download pip: https://pip.pypa.io/en/stable/installing/

then, run:

pip install networkx
pip install matplotlib
pip install xlrd
pip install csv

Finally, right click in the file and click on Run Python File in Terminal