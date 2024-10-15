from paver.easy import *
import paver
import os
import glob
import shutil
import sys
import platform
import subprocess

sys.path.append(os.path.dirname(__file__))

@task
def setup():
    sh('python -m pip install -U coverage parameterized radon')

@task
def check_tkinter():
    """Check if tkinter is installed and install it if missing."""
    try:
        import tkinter 
        print("Tkinter is already installed.")
    except ImportError:
        print("Tkinter is not installed. Installing...")
        install_tkinter()

def install_tkinter():
    """Install tkinter based on the operating system."""
    os_type = platform.system()
    
    if os_type == "Darwin": 
        print("Installing tkinter on macOS...")
        try:
            subprocess.check_call(['brew', 'install', 'python-tk'])
        except subprocess.CalledProcessError:
            print("Error: brew failed to install tkinter. Ensure Homebrew is installed.")
    
    elif os_type == "Linux":
        print("Installing tkinter on Linux...")
        try:
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'python3-tk'])
        except subprocess.CalledProcessError:
            print("Error: apt-get failed to install tkinter. Please check your system configuration.")
    
    elif os_type == "Windows":
        print("On Windows, tkinter is typically included with Python. If missing, please reinstall Python.")
      
@task
def test():
    sh('python -m coverage run --source src --omit src/master_display.py -m unittest discover -s test')
    sh('python -m coverage html')
    sh('python -m coverage report --show-missing')

@task
def clean():
    for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
    for pycache in glob.glob("*/__pycache__"): os.removedirs(pycache)
    for pycache in glob.glob("*/__pycache__"): shutil.rmtree(pycache)
    try:
        shutil.rmtree(os.getcwd() + "/cover")
    except:
        pass

@task
def radon():
    sh('radon cc src -a -nb')
    sh('radon cc src -a -nb > radon.report')
    if os.stat("radon.report").st_size != 0:
        raise Exception('radon found complex code')

@task
def run():
    setup()
    check_tkinter() 
    sh('python -m src.master_display')
    
@task

@needs(['setup', 'clean', 'test', 'radon'])
def default():
    pass
