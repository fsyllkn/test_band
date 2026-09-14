from pathlib import Path
import base64
import runpy

# Apply all v3.2 changes first: 135% default height, split 32dp lowercase / 29dp uppercase,
# candidate sizing, toolbar setting shortcut and generic voice IME support.
runpy.run_path('scripts/patch_google_pinyin_ui_v32.py', run_name='__main__')

ROOT = Path('decoded')

# iPhone-style press-preview background: wider rounded cap with a narrow tapered stem.
# This is an original UI asset generated for this patch; it is not copied from Apple/Gboard.
PNG_B64 = (
    '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'
)

drawable_dir = ROOT / 'res/drawable-nodpi'
drawable_dir.mkdir(parents=True, exist_ok=True)
(drawable_dir / 'bg_key_preview_ios.png').write_bytes(base64.b64decode(PNG_B64))

# Replace the v3 rectangular preview with a wider cap + narrow stem preview.
# Keep the same popup IDs so Google's existing MaterialPopupView handler still controls it.
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
        android:background="@drawable/bg_key_preview_ios"
        style="@style/MaterialPopupContent">
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
                android:visibility="gone"
                style="@style/MaterialPopupLabel" />
            <ImageView
                android:id="@id/popup_icon"
                android:layout_width="78.0dip"
                android:layout_height="70.0dip"
                android:layout_gravity="top|center_horizontal"
                android:visibility="gone"
                style="@style/MaterialPopupImage" />
            <TextView
                android:id="@id/popup_footer"
                android:visibility="gone"
                style="@style/MaterialPopupFooter" />
        </FrameLayout>
    </com.google.android.apps.inputmethod.libs.framework.keyboard.widget.BasicPopupView>
</com.google.android.apps.inputmethod.libs.framework.keyboard.widget.MaterialPopupView>
''', encoding='utf-8')

print('UI v3.3 patch applied: iPhone-style wide-cap/narrow-stem key preview bubble; all v3.2 changes retained.')
