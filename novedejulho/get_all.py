import os
import sys

IGNORE_LIST = ['__init__.py','get_all.py', 'generate_db.py']

def get_all():
  files = os.listdir('.')
  files = [ file for file in files if '.py' in file and file not in IGNORE_LIST ]

  for file in sorted(files):
    print(file.replace('.py', ''))
    os.system('python3 {}'.format(file))

if __name__ == '__main__':
  get_all()