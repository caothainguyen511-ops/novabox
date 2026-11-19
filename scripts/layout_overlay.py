"""Apply a compact Vietnamese-first NovaBox layout theme to Winlator resources."""
from pathlib import Path

STRINGS = {
    "run": "Chạy", "edit": "Sửa", "add": "Thêm",
    "controls_editor": "Chỉnh điều khiển",
    "external_controllers": "Tay cầm ngoài",
    "wine_configuration": "Cấu hình Wine",
    "win_components": "Thành phần Windows",
    "environment_variables": "Biến môi trường",
    "drives": "Ổ đĩa", "hud_mode": "HUD / FPS",
    "profile": "Hồ sơ", "profile_name": "Tên hồ sơ",
    "processor_affinity": "Phân bổ lõi CPU",
    "video_memory_size": "Bộ nhớ đồ họa",
    "storage_info": "Thông tin lưu trữ",
    "force_fullscreen": "Buộc toàn màn hình",
    "task_manager": "Trình quản lý tác vụ",
    "open_file": "Mở tệp", "download_file": "Tải gói",
}

def apply_layouts(root: Path) -> None:
    resources = root / "app/app/src/main/res"
    vi = resources / "values-vi/strings.xml"
    vi.parent.mkdir(parents=True, exist_ok=True)
    text = vi.read_text(encoding="utf-8") if vi.exists() else "<resources>\n</resources>\n"
    additions = [f'<string name="{k}">{v}</string>' for k, v in STRINGS.items() if f'name="{k}"' not in text]
    if additions:
        text = text.replace("</resources>", "\n".join(additions) + "\n</resources>")
    vi.write_text(text, encoding="utf-8", newline="\n")

    header = resources / "layout/main_menu_header.xml"
    header.write_text('''<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="142dp"
    android:background="@drawable/novabox_header_background"
    android:paddingLeft="18dp" android:paddingRight="18dp" android:paddingBottom="20dp">
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content"
        android:layout_gravity="bottom" android:orientation="vertical">
        <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
            android:text="NOVABOX" android:textColor="#FFFFFF" android:textSize="26sp"
            android:textStyle="bold" android:letterSpacing="0.08" />
        <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
            android:layout_marginTop="4dp" android:text="WINDOWS COMPATIBILITY FOR ANDROID"
            android:textColor="#B8C4DC" android:textSize="10sp" android:letterSpacing="0.08" />
    </LinearLayout>
</FrameLayout>''', encoding="utf-8", newline="\n")

    list_item = resources / "layout/container_list_item.xml"
    content = list_item.read_text(encoding="utf-8")
    if "@drawable/novabox_container_card" not in content:
        content = content.replace('android:orientation="horizontal"',
            'android:orientation="horizontal"\n    android:layout_marginLeft="12dp"\n'
            '    android:layout_marginRight="12dp"\n    android:layout_marginTop="5dp"\n'
            '    android:layout_marginBottom="5dp"\n    android:background="@drawable/novabox_container_card"', 1)
        content = content.replace('android:paddingLeft="16dp"', 'android:paddingLeft="14dp"', 1)
        content = content.replace('android:paddingRight="16dp"', 'android:paddingRight="14dp"', 1)
        list_item.write_text(content, encoding="utf-8", newline="\n")

    drawables = resources / "drawable"
    drawables.mkdir(parents=True, exist_ok=True)
    (drawables / "novabox_header_background.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="0" android:startColor="#17152A" android:endColor="#27204A" />
</shape>''', encoding="utf-8", newline="\n")
    (drawables / "novabox_container_card.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#151A27" /><corners android:radius="16dp" />
    <stroke android:width="1dp" android:color="#2B3146" />
</shape>''', encoding="utf-8", newline="\n")
