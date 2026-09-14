from pathlib import Path
import runpy

# Apply all v3.2 changes first.
runpy.run_path('scripts/patch_google_pinyin_ui_v32.py', run_name='__main__')

ROOT = Path('decoded')

# Use a vector drawable instead of an embedded binary PNG. This keeps the patch
# text-only and avoids base64 corruption in CI. Android 16 will use this resource.
vector_dir = ROOT / 'res/drawable-v21'
vector_dir.mkdir(parents=True, exist_ok=True)
(vector_dir / 'bg_key_preview_ios.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="78dp"
    android:height="104dp"
    android:viewportWidth="78"
    android:viewportHeight="104">
    <path
        android:fillColor="#FFFFFFFF"
        android:strokeColor="#FFD8D8D8"
        android:strokeWidth="1"
        android:pathData="M17,1 C10,1 5,6 5,13 L5,60 C5,67 10,72 17,72 L24,72 L29,96 C30,101 34,103 39,103 C44,103 48,101 49,96 L54,72 L61,72 C68,72 73,67 73,60 L73,13 C73,6 68,1 61,1 Z" />
</vector>
''', encoding='utf-8')

# Fallback for pre-v21 devices. Not used on the user's Android 16 device, but
# keeps the resource reference resolvable across the APK's minSdk range.
fallback_dir = ROOT / 'res/drawable'
fallback_dir.mkdir(parents=True, exist_ok=True)
(fallback_dir / 'bg_key_preview_ios.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#FFFFFFFF" />
    <stroke android:width="1dp" android:color="#FFD8D8D8" />
    <corners android:radius="12dp" />
</shape>
''', encoding='utf-8')

# Replace the previous rectangular preview with a wide cap + narrow stem layout.
# CoversSoftKey=true makes the lower part overlap/attach to the pressed key.
preview = ROOT / 'res/layout/popup_bubble_keypreview_material.xml'
preview.write_text('''<?xml version="1.0" encoding="utf-8"?>
<com.google.android.apps.inputmethod.libs.framework.keyboard.widget.MaterialPopupView
    android:id="@id/popup_bubble"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    app:CoversSoftKey="true"
    app:PopupDistance="0.0dip"
    app:SoftKeyInsetBottom="@dimen/softkey_bg_inset_bottom"
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">
    <com.google.android.apps.inputmethod.libs.framework.keyboard.widget.BasicPopupView
        android:id="@id/popup_content"
        android:layout_width="78.0dip"
        android:layout_height="104.0dip"
        android:layout_margin="0.0dip"
        android:paddingLeft="0.0dip"
        android:paddingRight="0.0dip"
        android:background="@drawable/bg_key_preview_ios">
        <FrameLayout
            android:id="@id/popup_layout"
            android:layout_width="78.0dip"
            android:layout_height="104.0dip">
            <com.google.android.apps.inputmethod.libs.framework.keyboard.widget.AutoCenteredLabelView
                android:id="@id/popup_label"
                android:layout_width="78.0dip"
                android:layout_height="70.0dip"
                android:layout_gravity="top|center_horizontal"
                android:gravity="center"
                android:textSize="36.5dip"
                android:textColor="?ColorLabelPopup"
                android:visibility="gone" />
            <ImageView
                android:id="@id/popup_icon"
                android:layout_width="78.0dip"
                android:layout_height="70.0dip"
                android:layout_gravity="top|center_horizontal"
                android:scaleType="center"
                android:visibility="gone" />
            <TextView
                android:id="@id/popup_footer"
                android:visibility="gone" />
        </FrameLayout>
    </com.google.android.apps.inputmethod.libs.framework.keyboard.widget.BasicPopupView>
</com.google.android.apps.inputmethod.libs.framework.keyboard.widget.MaterialPopupView>
''', encoding='utf-8')

print('UI v3.3 patch applied: iPhone-style wide-cap/narrow-stem key preview bubble; all v3.2 changes retained.')
