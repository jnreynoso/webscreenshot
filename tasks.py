#!/usr/bin/python

from server import main as start_server
from sys import platform as _platform
from invoke import run, task
import os

def check_os():
    system = ''

    if _platform == "linux" or _platform == "linux2":
        system = 'Linux'
    elif _platform == "darwin":
        system = 'OSX'
    elif _platform == "win32":
        system = 'Agg'

    return system

def check_webkit2png():
    output = os.popen("echo $(which webkit2png)").read()

    if 'bin' in output:
        return True
    else:
        return False

def install_webkit2png(system="Linux"):
    if system == "Linux":
        run("sudo apt-get install python-qt4 libqt4-webkit xvfb")
        run("sudo apt-get install flashplugin-installer")
        run("sudo apt-get install git-core")
        run("mkdir python-webkit2png")
        run("git clone https://github.com/adamn/python-webkit2png.git python-webkit2png")
        run("cd python-webkit2png && sudo python setup.py install")
        run("rm -rf python-webkit2png/")
    elif system == "OSX":
        run('brew install webkit2png')
    elif system == "Agg":
        run(':D')

@task
def install():
    if check_webkit2png():
        print("webkit2png already installed")
    else:
        install_webkit2png(system=check_os())

@task
def runserver():
    run("mkdir -p screenshots")
    start_server()
