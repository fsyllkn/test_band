from pathlib import Path

ROOT = Path('decoded')


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)


# Height presets.
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

# Lowercase QWERTY layout: 29dp portrait / 25dp landscape.
src = ROOT / 'res/layout/softkey_qwerty_label_character_label_footer.xml'
dst = ROOT / 'res/layout/softkey_qwerty_label_character_label_footer_lowercase.xml'
x = src.read_text(encoding='utf-8')
x = once(x,
    'android:id="@id/label" enable_relayout="false" style="@style/Label.Qwerty"',
    'android:id="@id/label" android:textSize="29.0dip" enable_relayout="false" style="@style/Label.Qwerty"',
    'portrait lowercase label')
dst.write_text(x, encoding='utf-8')

src = ROOT / 'res/layout-land/softkey_qwerty_label_character_label_footer.xml'
dst = ROOT / 'res/layout-land/softkey_qwerty_label_character_label_footer_lowercase.xml'
x = src.read_text(encoding='utf-8')
x = once(x,
    'android:id="@id/label" style="@style/Label.QwertyLand"',
    'android:id="@id/label" android:textSize="25.0dip" style="@style/Label.QwertyLand"',
    'landscape lowercase label')
dst.write_text(x, encoding='utf-8')

for rel, template in [
    ('softkeys_input_zh_pinyin_qwerty.xml', 'softkey_template_pinyin_qwerty'),
    ('softkeys_input_en_qwerty.xml', 'softkey_template_en_qwerty'),
]:
    f = ROOT / 'res/xml' / rel
    x = f.read_text(encoding='utf-8')
    x = once(x,
        f'id="@id/{template}" layout="@layout/softkey_qwerty_label_character_label_footer"',
        f'id="@id/{template}" layout="@layout/softkey_qwerty_label_character_label_footer_lowercase"',
        f'{rel} lowercase template')
    f.write_text(x, encoding='utf-8')

# Candidate words: 21 -> 25dp.
dims = ROOT / 'res/values/dimens.xml'
x = dims.read_text(encoding='utf-8')
x = once(x,
    '<dimen name="text_size_candidate">21.0dip</dimen>',
    '<dimen name="text_size_candidate">25.0dip</dimen>',
    'candidate size')
dims.write_text(x, encoding='utf-8')

# Dedicated QWERTY key preview: +30% text, wider top.
popup = ROOT / 'res/layout/popup_bubble_keypreview_material.xml'
x = (ROOT / 'res/layout/popup_bubble_material.xml').read_text(encoding='utf-8')
x = once(x,
    '<FrameLayout android:id="@id/popup_layout" style="@style/MaterialPopupView">',
    '<FrameLayout android:id="@id/popup_layout" android:minWidth="56.0dip" style="@style/MaterialPopupView">',
    'preview width')
x = once(x,
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

# Explicit IDs required by this legacy AAPT1 resource set.
ids = ROOT / 'res/values/ids.xml'
x = ids.read_text(encoding='utf-8')
for name in ['key_pos_header_clipboard', 'key_pos_header_settings', 'softkey_clipboard_edit']:
    if f'name="{name}"' not in x:
        x = x.replace('</resources>', f'    <item type="id" name="{name}" />\n</resources>', 1)
ids.write_text(x, encoding='utf-8')

# Toolbar: Clipboard/Edit, Settings, existing Voice/Hide button.
header = ROOT / 'res/layout/keyboard_prime_header_inner.xml'
x = header.read_text(encoding='utf-8')
old = '''    <LinearLayout android:gravity="right" android:paddingRight="?KeyboardInnerPadding" style="@style/PrimeHeaderInnerLinear">
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_voice" style="@style/HeaderTab.PrimeIcon" />
    </LinearLayout>'''
new = '''    <LinearLayout android:gravity="right" android:paddingRight="?KeyboardInnerPadding" style="@style/PrimeHeaderInnerLinear">
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_clipboard" style="@style/HeaderTab.PrimeIcon" />
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_settings" style="@style/HeaderTab.PrimeIcon" />
        <com.google.android.apps.inputmethod.libs.framework.keyboard.SoftKeyView android:id="@id/key_pos_header_voice" style="@style/HeaderTab.PrimeIcon" />
    </LinearLayout>'''
x = once(x, old, new, 'toolbar layout')
header.write_text(x, encoding='utf-8')

plain = ROOT / 'res/xml/softkeys_header_plain.xml'
x = plain.read_text(encoding='utf-8')
softkey = '''        <softkey id="@id/softkey_clipboard_edit" layout="@layout/softkey_icon" content_description="@string/text_editing_access_point_content_desc">
            <action type="PRESS" keycode="OPEN_EXTENSION" data="com.google.android.apps.inputmethod.libs.textediting.TextEditingExtension" />
            <icon location="@id/icon" value="@attr/IconAccessPointTextEditing" />
        </softkey>
'''
x = once(x, '    </softkeys>\n</framework>', softkey + '    </softkeys>\n</framework>', 'clipboard softkey')
plain.write_text(x, encoding='utf-8')

for rel in ['keymapping_header_zh_cn_prime.xml', 'keymapping_header_en_prime.xml']:
    f = ROOT / 'res/xml' / rel
    x = f.read_text(encoding='utf-8')
    marker = '        <mapping view_id="@id/key_pos_header_voice" key_id="@id/softkey_voice" />'
    add = '''        <mapping view_id="@id/key_pos_header_clipboard" key_id="@id/softkey_clipboard_edit" />
        <mapping view_id="@id/key_pos_header_settings" key_id="@id/softkey_settings_key" />
'''
    x = once(x, marker, add + marker, f'{rel} mappings')
    f.write_text(x, encoding='utf-8')

print('UI v2 patch applied successfully.')
