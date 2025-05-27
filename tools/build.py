"""Build the nv_tlview novelibre plugin package.
        
Note: VERSION must be updated manually before starting this script.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copy2
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder
import inliner

VERSION = '5.6.2'

TEMP_FILE = '../test/temp.py'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_tlview'
    LOCAL_LIB = 'nvtlview'
    GERMAN_TRANSLATION = True

    def add_extras(self):
        self.add_icons()

    def add_icons(self):
        super().add_icons()
        copy2('../icons/tLogo32.png', f'{self.buildDir}/icons')

    def inline_modules(self, source, target):
        """Inline all non-standard library modules."""
        inliner.run(
            source,
            TEMP_FILE,
            'tlviewer',
            '../../nv_tlview/src/'
            )
        inliner.run(
            TEMP_FILE,
            TEMP_FILE,
            'nvlib',
            '../../novelibre/src/'
            )
        inliner.run(
            TEMP_FILE,
            target,
            'tlv',
            '../../nv_tlview/src/'
            )
        os.remove(TEMP_FILE)


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
