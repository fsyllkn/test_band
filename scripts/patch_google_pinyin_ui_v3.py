from pathlib import Path

ROOT = Path('decoded')


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)


# 1) Preserve extended keyboard-height presets.
arrays = ROOT / 'res/values/arrays.xml'
s = arrays.read_text(encoding='utf-8')
entries = '''    <string-array name="entries_keyboard_height_ratio">
        <item>@string/kb_height_short</item>
        <item>@string/kb_height_midshort</item>
        <item>@string/kb_height_normal</item>
        <item>@string/kb_height_midtall</item>
        <item>@string/kb_height_tall</item>
        <item>120%</item>
        <item>125%</item>
        <item>130%</item>
        <item>135%</item>
        <item>140%</item>
        <item>145%</item>
        <item>150%</item>
        <item>155%</item>
    </string-array>'''
values = '''    <string-array name="entryvalues_keyboard_height_ratio">
        <item>0.9</item>
        <item>0.95</item>
        <item>1.0</item>
        <item>1.05</item>
        <item>1.1</item>
        <item>1.32</item>
        <item>1.375</item>
        <item>1.43</item>
        <item>1.485</item>
        <item>1.54</item>
        <item>1.595</item>
        <item>1.65</item>
        <item>1.705</item>
    </string-array>'''


def repl_array(text, name, replacement):
    a = text.index(f'    <string-array name="{name}">')
    b = text.index('    </string-array>', a) + len('    </string-array>')
    return text[:a] + replacement + text[b:]


s = repl_array(s, 'entries_keyboard_height_ratio', entries)
s = repl_array(s, 'entryvalues_keyboard_height_ratio', values)
arrays.write_text(s, encoding='utf-8')

zh_strings = ROOT / 'res/values-zh/strings.xml'
if zh_strings.exists():
    x = zh_strings.read_text(encoding='utf-8')
    x = x.replace('<string name="kb_height_tall">高</string>', '<string name="kb_height_tall">高（100%）</string>')
    zh_strings.write_text(x, encoding='utf-8')

# 2) QWERTY primary label layout: 29dp portrait / 25dp landscape.
# English uses one template for lower+upper case. Chinese has separate templates,
# so both Chinese templates are explicitly routed to the same enlarged layout.
src = ROOT / 'res/layout/softkey_qwerty_label_character_label_footer.xml'
dst = ROOT / 'res/layout/softkey_qwerty_label_character_label_footer_uiv3.xml'
x = src.read_text(encoding='utf-8')
x = once(
    x,
    'android:id="@id/label" enable_relayout="false" style="@style/Label.Qwerty"',
    'android:id="@id/label" android:textSize="29.0dip" enable_relayout="false" style="@style/Label.Qwerty"',
    'portrait qwerty label')
dst.write_text(x, encoding='utf-8')

src_land = ROOT / 'res/layout-land/softkey_qwerty_label_character_label_footer.xml'
dst_land = ROOT / 'res/layout-land/softkey_qwerty_label_character_label_footer_uiv3.xml'
x = src_land.read_text(encoding='utf-8')
x = once(
    x,
    'android:id="@id/label" style="@style/Label.QwertyLand"',
    'android:id="@id/label" android:textSize="25.0dip" style="@style/Label.QwertyLand"',
    'landscape qwerty label')
dst_land.write_text(x, encoding='utf-8')

# English template covers lowercase and uppercase.
en = ROOT / 'res/xml/softkeys_input_en_qwerty.xml'
x = en.read_text(encoding='utf-8')
x = once(
    x,
    'id="@id/softkey_template_en_qwerty" layout="@layout/softkey_qwerty_label_character_label_footer"',
    'id="@id/softkey_template_en_qwerty" layout="@layout/softkey_qwerty_label_character_label_footer_uiv3"',
    'English QWERTY template')
en.write_text(x, encoding='utf-8')

# Chinese lowercase and uppercase are separate templates. Route BOTH to 29dp.
zh = ROOT / 'res/xml/softkeys_input_zh_pinyin_qwerty.xml'
x = zh.read_text(encoding='utf-8')
for template in ['softkey_template_pinyin_qwerty', 'softkey_template_pinyin_qwerty_up']:
    x = once(
        x,
        f'id="@id/{template}" layout="@layout/softkey_qwerty_label_character_label_footer"',
        f'id="@id/{template}" layout="@layout/softkey_qwerty_label_character_label_footer_uiv3"',
        f'Chinese template {template}')
zh.write_text(x, encoding='utf-8')

# 3) Candidate words: 21dp -> 25dp.
dims = ROOT / 'res/values/dimens.xml'
x = dims.read_text(encoding='utf-8')
x = once(
    x,
    '<dimen name="text_size_candidate">21.0dip</dimen>',
    '<dimen name="text_size_candidate">25.0dip</dimen>',
    'candidate size')
dims.write_text(x, encoding='utf-8')

# 4) Dedicated QWERTY press preview: +30% text, wider Apple-like cap.
popup = ROOT / 'res/layout/popup_bubble_keypreview_material.xml'
x = (ROOT / 'res/layout/popup_bubble_material.xml').read_text(encoding='utf-8')
x = once(
    x,
    '<FrameLayout android:id="@id/popup_layout" style="@style/MaterialPopupView">',
    '<FrameLayout android:id="@id/popup_layout" android:minWidth="56.0dip" style="@style/MaterialPopupView">',
    'preview width')
x = once(
    x,
    '<com.google.android.apps.inputmethod.libs.framework.keyboard.widget.AutoCenteredLabelView android:id="@id/popup_label" android:visibility="gone" style="@style/MaterialPopupLabel" />',
    '<com.google.android.apps.inputmethod.libs.framework.keyboard.widget.AutoCenteredLabelView android:id="@id/popup_label" android:textSize="36.5dip" android:minWidth="56.0dip" android:visibility="gone" style="@style/MaterialPopupLabel" />',
    'preview label')
popup.write_text(x, encoding='utf-8')

for rel in ['softkeys_input_zh_pinyin_qwerty.xml', 'softkeys_input_en_qwerty.xml']:
    f = ROOT / 'res/xml' / rel
    x = f.read_text(encoding='utf-8')
    needle = 'intention="DECODE" popup_label="$press_data$" />'
    repl = 'intention="DECODE" popup_label="$press_data$" popup_layout="@layout/popup_bubble_keypreview_material" />'
    n = x.count(needle)
    if n not in (1, 2):
        raise SystemExit(f'{rel}: preview PRESS count={n}')
    f.write_text(x.replace(needle, repl), encoding='utf-8')

# 5) Toolbar: keep Settings shortcut, remove the v2 pseudo-clipboard shortcut.
# A real Gboard-like clipboard history needs its own listener + persistent history UI.
ids = ROOT / 'res/values/ids.xml'
x = ids.read_text(encoding='utf-8')
if 'name="key_pos_header_settings"' not in x:
    x = x.replace('</resources>', '    <item type="id" name="key_pos_header_settings" />\n</resources>', 1)
ids.write_text(x, encoding='utf-8')

header = ROOT / 'res/layout/keyboard_prime_header_inner.xml'
x = header.read_text(encoding='utf-8')
old = '''    <LinearLayout android:gravity="right" android:paddingRight="?KeyboardInnerPadding" style="@style/PrimeHeaderInnerLinear">
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_voice" style="@style/HeaderTab.PrimeIcon" />
    </LinearLayout>'''
new = '''    <LinearLayout android:gravity="right" android:paddingRight="?KeyboardInnerPadding" style="@style/PrimeHeaderInnerLinear">
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_settings" style="@style/HeaderTab.PrimeIcon" />
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_voice" style="@style/HeaderTab.PrimeIcon" />
    </LinearLayout>'''
x = once(x, old, new, 'toolbar layout')
header.write_text(x, encoding='utf-8')

for rel in ['keymapping_header_zh_cn_prime.xml', 'keymapping_header_en_prime.xml']:
    f = ROOT / 'res/xml' / rel
    x = f.read_text(encoding='utf-8')
    marker = '        <mapping view_id="@id/key_pos_header_voice" key_id="@id/softkey_voice" />'
    add = '        <mapping view_id="@id/key_pos_header_settings" key_id="@id/softkey_settings_key" />\n'
    x = once(x, marker, add + marker, f'{rel} settings mapping')
    f.write_text(x, encoding='utf-8')

# 6) Voice input compatibility.
# Stock Google Pinyin only accepts voice-IME packages whose package name starts
# with "com.google.android". This method already checks subtype mode == "voice".
# Make the package-prefix test neutral so any enabled voice IME can be selected,
# including FUTO Voice Input (org.futo.voiceinput).
gc = ROOT / 'smali/gc.smali'
x = gc.read_text(encoding='utf-8')
x = once(
    x,
    '    const-string v3, "com.google.android"',
    '    const-string v3, ""',
    'voice IME package restriction')
gc.write_text(x, encoding='utf-8')

print('UI v3 patch applied: uppercase parity, candidates/preview retained, settings retained, generic voice IME enabled.')
