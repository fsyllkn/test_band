from pathlib import Path
import runpy

# Apply v3.1 first: UI v3 + 135% default height.
runpy.run_path('scripts/patch_google_pinyin_ui_v31.py', run_name='__main__')

ROOT = Path('decoded')

# Build a dedicated lowercase layout: 32dp portrait, 28dp landscape.
# Keep the existing UI-v3 layout at 29dp/25dp for uppercase.
base = ROOT / 'res/layout/softkey_qwerty_label_character_label_footer_uiv3.xml'
lower = ROOT / 'res/layout/softkey_qwerty_label_character_label_footer_lower32.xml'
x = base.read_text(encoding='utf-8')
if 'android:textSize="29.0dip"' not in x:
    raise SystemExit('Expected 29dp portrait UI-v3 QWERTY layout')
x = x.replace('android:textSize="29.0dip"', 'android:textSize="32.0dip"', 1)
lower.write_text(x, encoding='utf-8')

base_land = ROOT / 'res/layout-land/softkey_qwerty_label_character_label_footer_uiv3.xml'
lower_land = ROOT / 'res/layout-land/softkey_qwerty_label_character_label_footer_lower32.xml'
x = base_land.read_text(encoding='utf-8')
if 'android:textSize="25.0dip"' not in x:
    raise SystemExit('Expected 25dp landscape UI-v3 QWERTY layout')
x = x.replace('android:textSize="25.0dip"', 'android:textSize="28.0dip"', 1)
lower_land.write_text(x, encoding='utf-8')

# Chinese already has separate lowercase/uppercase templates.
zh = ROOT / 'res/xml/softkeys_input_zh_pinyin_qwerty.xml'
x = zh.read_text(encoding='utf-8')
needle = 'id="@id/softkey_template_pinyin_qwerty" layout="@layout/softkey_qwerty_label_character_label_footer_uiv3"'
repl = 'id="@id/softkey_template_pinyin_qwerty" layout="@layout/softkey_qwerty_label_character_label_footer_lower32"'
if x.count(needle) != 1:
    raise SystemExit(f'Chinese lowercase template match count={x.count(needle)}')
x = x.replace(needle, repl, 1)
# Uppercase template intentionally remains on the 29dp UI-v3 layout.
zh.write_text(x, encoding='utf-8')

# English original uses one template for both lowercase and uppercase keys.
# Add a dedicated uppercase template, keep uppercase at 29dp, and split the key list.
en = ROOT / 'res/xml/softkeys_input_en_qwerty.xml'
x = en.read_text(encoding='utf-8')

# Existing template becomes lowercase 32dp.
needle = 'id="@id/softkey_template_en_qwerty" layout="@layout/softkey_qwerty_label_character_label_footer_uiv3"'
repl = 'id="@id/softkey_template_en_qwerty" layout="@layout/softkey_qwerty_label_character_label_footer_lower32"'
if x.count(needle) != 1:
    raise SystemExit(f'English base template match count={x.count(needle)}')
x = x.replace(needle, repl, 1)

# Clone the template for uppercase, restoring the 29dp layout.
template_start = x.index('        <softkey_template id="@id/softkey_template_en_qwerty"')
template_end = x.index('        </softkey_template>', template_start) + len('        </softkey_template>')
template = x[template_start:template_end]
upper_template = template.replace(
    'id="@id/softkey_template_en_qwerty"',
    'id="@id/softkey_template_en_qwerty_up"',
    1,
).replace(
    'layout="@layout/softkey_qwerty_label_character_label_footer_lower32"',
    'layout="@layout/softkey_qwerty_label_character_label_footer_uiv3"',
    1,
)
x = x[:template_end] + '\n' + upper_template + x[template_end:]

# Split the single English key list immediately before the first uppercase key.
first_upper = '            <softkey id="@id/softkey_en_qwerty_up_q"'
pos = x.index(first_upper)
insert = '''        </softkey_list>
        <softkey_list template_id="@id/softkey_template_en_qwerty_up" splitter=" ">
'''
x = x[:pos] + insert + x[pos:]

en.write_text(x, encoding='utf-8')

# Explicitly declare the new English uppercase template ID for legacy AAPT1.
ids = ROOT / 'res/values/ids.xml'
x = ids.read_text(encoding='utf-8')
if 'name="softkey_template_en_qwerty_up"' not in x:
    x = x.replace('</resources>', '    <item type="id" name="softkey_template_en_qwerty_up" />\n</resources>', 1)
ids.write_text(x, encoding='utf-8')

print('UI v3.2 patch applied: lowercase 32dp portrait / 28dp landscape; uppercase remains 29dp / 25dp; default height 135%.')
