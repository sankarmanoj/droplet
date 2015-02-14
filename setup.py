from distutils.core import setup
import py2exe
import sys
#setup(console=["install.py"])
#setup(console=["sender.py"])
#setup(console=["run.py"])
name = raw_input("Enter file name")
setup(console=[name])