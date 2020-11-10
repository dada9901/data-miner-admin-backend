import os
import platform
import sys
import subprocess
project_root = os.path.dirname(os.path.realpath(__file__))
# project_root = os.path.realpath(__file__)
if platform.system() == 'Linux':
    command = sys.executable + ' -m pip freeze > ' + project_root + '/requirements.txt'
if platform.system() == 'Windows':
    command = '"' + sys.executable + '"' + ' -m pip freeze > "' + project_root + '\\requirements.txt"'
print(command)
os.popen(command)   #路径有空格，可用
