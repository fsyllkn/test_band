from pathlib import Path
import runpy

# Apply all UI v3.3 changes first, including the iPhone-style preview bubble.
runpy.run_path('scripts/patch_google_pinyin_ui_v33.py', run_name='__main__')

ROOT = Path('decoded')
preview = ROOT / 'res/layout/popup_bubble_keypreview_material.xml'
x = preview.read_text(encoding='utf-8')

# The stock key-preview label is about 28dp. Set the preview to 150% of that
# baseline: 28 * 1.5 = 42dp. This replaces the previous 36.5dp (+30%) test.
needle = 'android:textSize="36.5dip"'
if x.count(needle) != 1:
    raise SystemExit(f'Expected one 36.5dp preview label, found {x.count(needle)}')
x = x.replace(needle, 'android:textSize="42.0dip"', 1)
preview.write_text(x, encoding='utf-8')

print('UI v3.4 patch applied: key-preview label is 42dp (150% of the 28dp stock preview baseline).')
