from pathlib import Path
import re
import runpy

# Apply the existing UI v3 patch first.
runpy.run_path('scripts/patch_google_pinyin_ui_v3.py', run_name='__main__')

ROOT = Path('decoded')

# The original "Tall/高" value is 1.10 and is defined as our 100% baseline.
# Therefore 135% = 1.10 * 1.35 = 1.485.
# Google Pinyin's keyboard settings XML reads its default from
# @string/pref_def_value_keyboard_height_ratio, so patch that resource directly.
pattern = re.compile(
    r'(<string name="pref_def_value_keyboard_height_ratio">)[^<]*(</string>)'
)
patched = 0
for strings_xml in ROOT.glob('res/values*/strings.xml'):
    text = strings_xml.read_text(encoding='utf-8')
    new_text, count = pattern.subn(r'\g<1>1.485\g<2>', text, count=1)
    if count:
        strings_xml.write_text(new_text, encoding='utf-8')
        patched += count

if patched == 0:
    raise SystemExit('Could not locate pref_def_value_keyboard_height_ratio')

print(f'UI v3.1 patch applied; keyboard default height = 135% (1.485), patched resources={patched}.')
