"""Generate a template file (pot) for message translation.

For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
import build_nv_tlview as build_plugin
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import pgettext

APP = 'nv_tlview'
POT_DIR = '../i18n'
POT_FILE = f'{POT_DIR}/messages.pot'


def make_pot(version='unknown'):
    os.makedirs(POT_DIR, exist_ok=True)

    # Generate a complete plugin.
    build_plugin.main()

    # Generate a pot file from the script.
    if os.path.isfile(POT_FILE):
        os.replace(POT_FILE, f'{POT_FILE}.bak')
        backedUp = True
    else:
        backedUp = False
    try:
        pot = pgettext.PotFile(POT_FILE, app=APP, appVersion=version)
        pot.scan_file(build_plugin.TARGET_FILE)
        print(f'Writing "{pot.filePath}"...\n')
        pot.write_pot()

    except:
        if backedUp:
            os.replace(f'{POT_FILE}.bak', POT_FILE)
        print('WARNING: Cannot write pot file.')
        return False

    return True


if __name__ == '__main__':
    try:
        success = make_pot(sys.argv[1])
    except:
        success = make_pot()
    if not success:
        sys.exit(1)
