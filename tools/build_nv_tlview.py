"""Build a nv_tlview plugin.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the nvoxlib package.

The novxlib library (see https://github.com/peter88213/novxlib)
must be located on the same directory level as the nv_tlview project. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}nv_tlview.py'
TARGET_FILE = f'{BUILD}nv_tlview.py'

os.makedirs(BUILD, exist_ok=True)


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'nvpluginlib', '../../nv_tlview/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'nvlib', '../../novelibre/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'novxlib', '../../novxlib/src/')
    print('Done.')


if __name__ == '__main__':
    main()
