from distutils.core import setup
import py2exe
name = raw_input("Enter name")
setup(console = [name])