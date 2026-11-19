#!/usr/bin/env python3
"""Apply the independently branded NovaBox layer to a pinned Winlator checkout."""
from __future__ import annotations
import re
import shutil
import sys
from pathlib import Path
from layout_overlay import apply_layouts

SPLASH_JAVA = r'''package com.winlator;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.graphics.Shader;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;

/** Original NovaBox splash artwork drawn natively; no network or bitmap is required. */
public final class SplashActivity extends Activity {
    private final Handler handler = new Handler(Looper.getMainLooper());
    private boolean launched;
    private final Runnable launchMain = () -> {
        if (launched || isFinishing()) return;
        launched = true;
        startActivity(new Intent(SplashActivity.this, MainActivity.class));
        finish();
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
    };

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(5, 7, 22));
        getWindow().setNavigationBarColor(Color.rgb(5, 7, 22));
        setContentView(new SplashArtView());
        handler.postDelayed(launchMain, 250L);
    }
    @Override protected void onDestroy() {
        handler.removeCallbacks(launchMain);
        super.onDestroy();
    }

    private final class SplashArtView extends View {
        private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Typeface heavy = Typeface.create("sans-serif-black", Typeface.BOLD);
        private final Typeface normal = Typeface.create("sans-serif", Typeface.NORMAL);
        SplashArtView() { super(SplashActivity.this); }

        @Override protected void onDraw(Canvas c) {
            super.onDraw(c);
            c.save();
            c.scale(getWidth()/720f, getHeight()/1280f);
            p.setStyle(Paint.Style.FILL);
            p.setShader(new LinearGradient(0,0,720,1280,
                new int[]{0xff050716,0xff0b1030,0xff080b1d},null,Shader.TileMode.CLAMP));
            c.drawRect(0,0,720,1280,p); p.setShader(null);

            for (int i=0;i<54;i++) {
                p.setColor(i%3==0?0xff22d3ee:0xff7775ff);
                p.setAlpha(70+(i*19%150));
                c.drawCircle((i*137%701)+9,(i*239%850)+20,i%5==0?2.2f:1.1f,p);
            }
            p.setAlpha(255); p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(2.2f);
            p.setColor(0xff5730c8); c.drawRoundRect(new RectF(22,22,698,1258),28,28,p);
            p.setStrokeWidth(5f);
            p.setShader(new LinearGradient(24,0,696,0,
                new int[]{0xffa020f0,0xff433cff,0xff00d9ff},null,Shader.TileMode.CLAMP));
            c.drawLine(28,1050,28,1240,p); c.drawLine(692,40,692,230,p);
            p.setShader(null); p.setStyle(Paint.Style.FILL);

            Path left=new Path(); left.moveTo(178,278); left.lineTo(270,278); left.lineTo(270,548); left.lineTo(178,548); left.close();
            p.setShader(new LinearGradient(178,278,270,548,0xfff05cff,0xff5d19e8,Shader.TileMode.CLAMP)); c.drawPath(left,p);
            Path bridge=new Path(); bridge.moveTo(210,278); bridge.lineTo(318,278); bridge.lineTo(535,485); bridge.lineTo(465,548); bridge.close();
            p.setShader(new LinearGradient(220,278,510,548,
                new int[]{0xffbf20ff,0xff5146ff,0xff00cfff},null,Shader.TileMode.CLAMP)); c.drawPath(bridge,p);
            Path right=new Path(); right.moveTo(450,278); right.lineTo(542,278); right.lineTo(542,548); right.lineTo(450,548); right.close();
            p.setShader(new LinearGradient(450,278,542,548,0xff00e5f5,0xff0878ff,Shader.TileMode.CLAMP)); c.drawPath(right,p);
            p.setShader(null); p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(3f); p.setColor(0xfff4f1ff);
            c.drawPath(left,p); c.drawPath(bridge,p); c.drawPath(right,p);
            p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f);
            p.setShader(new LinearGradient(90,570,620,350,0xffb51cff,0xff00dfff,Shader.TileMode.CLAMP));
            c.drawOval(new RectF(86,400,635,625),p); p.setShader(null);

            p.setStyle(Paint.Style.FILL); p.setTextAlign(Paint.Align.CENTER); p.setTypeface(heavy); p.setTextSize(76);
            p.setShader(new LinearGradient(130,0,590,0,
                new int[]{0xfff8f7ff,0xffa9aaff,0xff22d3ee},null,Shader.TileMode.CLAMP));
            c.drawText("NOVABOX",360,700,p); p.setShader(null);
            p.setTypeface(normal); p.setTextSize(23); p.setColor(0xffe8eaff);
            c.drawText("WINDOWS COMPATIBILITY",360,765,p);
            c.drawText("FOR ANDROID",360,805,p);

            p.setColor(0xff121d55);
            for (int i=0;i<18;i++) {
                float x=i*43, h=35+(i*47%95);
                c.drawRect(x,1040-h,x+25,1040,p);
            }
            p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f);
            p.setShader(new LinearGradient(0,1020,720,1020,0xffa31cff,0xff00dbff,Shader.TileMode.CLAMP));
            c.drawArc(new RectF(40,900,680,1110),190,160,false,p); p.setShader(null);
            p.setStyle(Paint.Style.FILL); p.setTypeface(heavy); p.setTextSize(20); p.setColor(0xff22d3ee);
            c.drawText("PLAY  •  RUN  •  ENJOY",360,1170,p);
            p.setTypeface(normal); p.setTextSize(16); p.setColor(0xffaab4df);
            c.drawText("NOVABOX BY CAOTHAINGUYEN",360,1210,p);
            c.restore();
        }
    }
}
'''

def read(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Required upstream file not found: {path}")
    return path.read_text(encoding="utf-8")

def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Patch anchor not found: {label}")
    return text.replace(old, new, 1)

def patch_gradle(root: Path) -> None:
    path=root/"app/app/build.gradle"
    text=read(path)
    text=re.sub(r"applicationId\s+['\"]com\.winlator['\"]",
                "applicationId 'com.novabox.emulator'",text,count=1)
    if "applicationId 'com.novabox.emulator'" not in text:
        raise RuntimeError("Could not set NovaBox applicationId")
    text=re.sub(r'versionName\s+["\'][^"\']+["\']',
                'versionName "1.0.0"',text,count=1)
    write(path,text)

def patch_manifest(root: Path) -> None:
    path=root/"app/app/src/main/AndroidManifest.xml"
    text=read(path)
    text=text.replace('android:authorities="com.winlator.FileProvider"',
                      'android:authorities="com.novabox.emulator.FileProvider"')
    if 'android:authorities="com.novabox.emulator.FileProvider"' not in text:
        raise RuntimeError("Could not update FileProvider authority")
    text=text.replace('android:icon="@mipmap/ic_launcher"',
                      'android:icon="@mipmap/novabox_icon"')
    if 'android:icon="@mipmap/novabox_icon"' not in text:
        raise RuntimeError("Could not set NovaBox app icon")
    if 'android:roundIcon=' not in text:
        text=text.replace('android:icon="@mipmap/novabox_icon"',
                          'android:icon="@mipmap/novabox_icon"\n        android:roundIcon="@mipmap/novabox_icon"',1)
    else:
        text=re.sub(r'android:roundIcon="[^"]+"',
                    'android:roundIcon="@mipmap/novabox_icon"',text,count=1)

    match=re.search(r'<activity\b(?=[^>]*android:name="com\.winlator\.MainActivity")[\s\S]*?</activity>',text)
    if not match:
        raise RuntimeError("Could not locate MainActivity")
    activity=match.group(0)
    activity=re.sub(
        r'\s*<intent-filter>\s*<action android:name="android\.intent\.action\.MAIN"\s*/>\s*<category android:name="android\.intent\.category\.LAUNCHER"\s*/>\s*</intent-filter>',
        "",activity,count=1)
    text=text[:match.start()]+activity+text[match.end():]
    if "com.winlator.SplashActivity" not in text:
        splash=('        <activity android:name="com.winlator.SplashActivity" android:exported="true" '
                'android:screenOrientation="portrait" android:theme="@style/NovaBoxSplashTheme">\n'
                '            <intent-filter>\n'
                '                <action android:name="android.intent.action.MAIN" />\n'
                '                <category android:name="android.intent.category.LAUNCHER" />\n'
                '            </intent-filter>\n'
                '        </activity>\n')
        text=text.replace("</application>",splash+"    </application>",1)
    write(path,text)
    java=root/"app/app/src/main/java/com/winlator/SplashActivity.java"
    if not java.exists():
        write(java,SPLASH_JAVA)

def patch_resources(root: Path) -> None:
    res=root/"app/app/src/main/res"
    values=res/"values/strings.xml"
    text=read(values)
    names={"app_name":"NovaBox","shortcuts":"Thư viện ứng dụng","containers":"Môi trường Windows",
           "input_controls":"Điều khiển","settings":"Cài đặt","about":"Giới thiệu NovaBox"}
    for key,val in names.items():
        pattern=rf'(<string\s+name="{re.escape(key)}"[^>]*>).*?(</string>)'
        text,count=re.subn(pattern,lambda m:m.group(1)+val+m.group(2),text,count=1,flags=re.S)
        if not count: raise RuntimeError(f"Missing string resource {key}")
    for key,val in (("driver_hub","Trung tâm đồ họa"),("steam_library","Thư viện Steam")):
        if f'name="{key}"' not in text:
            text=text.replace("</resources>",f'    <string name="{key}">{val}</string>\n</resources>')
    write(values,text)

    vi=res/"values-vi/strings.xml"
    write(vi,'''<?xml version="1.0" encoding="utf-8"?>
<resources>
<string name="app_name">NovaBox</string>
<string name="shortcuts">Thư viện ứng dụng</string>
<string name="containers">Môi trường Windows</string>
<string name="input_controls">Điều khiển</string>
<string name="settings">Cài đặt</string>
<string name="about">Giới thiệu NovaBox</string>
<string name="driver_hub">Trung tâm Driver</string>
<string name="steam_library">Thư viện Steam</string>
<string name="graphics_driver">Driver đồ họa</string>
<string name="audio_driver">Driver âm thanh</string>
<string name="new_container">Tạo môi trường mới</string>
<string name="edit_container">Chỉnh sửa môi trường</string>
<string name="no_items_to_display">Chưa có mục nào</string>
<string name="install_wine">Cài Wine</string>
<string name="wine_version">Phiên bản Wine</string>
<string name="box64_preset">Cấu hình Box64</string>
<string name="box64_version">Phiên bản Box64</string>
<string name="screen_size">Độ phân giải màn hình</string>
<string name="advanced">Nâng cao</string>
<string name="stability">Ổn định</string>
<string name="performance">Hiệu năng</string>
<string name="conservative">An toàn</string>
<string name="intermediate">Cân bằng</string>
<string name="loading">Đang tải…</string>
<string name="install_component">Cài component</string>
<string name="downloading_file">Đang tải tệp…</string>
<string name="a_network_error_occurred">Lỗi mạng hoặc không tải được component</string>
<string name="remove">Gỡ</string>
<string name="install">Cài đặt</string>
<string name="cancel">Hủy</string>
<string name="ok">Đồng ý</string>
</resources>
''')
    for locale in ("values-pt/strings.xml","values-ru/strings.xml"):
        path=res/locale
        if path.exists():
            t=read(path)
            t=re.sub(r'(<string\s+name="app_name"[^>]*>).*?(</string>)',
                     r'\1NovaBox\2',t,count=1,flags=re.S)
            write(path,t)

    icon_dir=res/"mipmap-anydpi-v26"
    write(icon_dir/"novabox_icon.xml",'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/novabox_icon_background" />
    <foreground android:drawable="@drawable/novabox_launcher_foreground" />
</adaptive-icon>
''')
    colors=res/"values/colors.xml"
    t=read(colors) if colors.exists() else "<resources>\n</resources>\n"
    if "novabox_icon_background" not in t:
        t=t.replace("</resources>",'    <color name="novabox_icon_background">#050716</color>\n</resources>')
    write(colors,t)
    foreground=Path(__file__).resolve().parents[1]/"branding/novabox_launcher_foreground.xml"
    (res/"drawable").mkdir(parents=True,exist_ok=True)
    shutil.copyfile(foreground,res/"drawable/novabox_launcher_foreground.xml")

    styles=res/"values/styles.xml"
    t=read(styles)
    for old,new in {"#0288d1":"#8B5CF6","#607d8b":"#28243F","#455a64":"#17152A",
                    "#505963":"#25213D","#3f474f":"#151326","#1b1e21":"#0B0E16",
                    "#2d3238":"#151A27","#56677a":"#8B5CF6","#37424f":"#24223A"}.items():
        t=t.replace(old,new)
    if "NovaBoxSplashTheme" not in t:
        t=t.replace("</resources>",'''    <style name="NovaBoxSplashTheme" parent="@style/Theme.AppCompat.Light.NoActionBar">
        <item name="android:windowBackground">#0B0E16</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:colorAccent">#8B5CF6</item>
        <item name="android:navigationBarColor">#050716</item>
        <item name="android:statusBarColor">#050716</item>
    </style>
</resources>''')
    write(styles,t)

def patch_locale(root: Path) -> None:
    path=root/"app/app/src/main/java/com/winlator/core/LocaleHelper.java"
    text=read(path)
    text=text.replace('private static final String[] supportedLocales = {"en_US", "pt_BR", "ru_RU"};',
                      'private static final String[] supportedLocales = {"en_US", "pt_BR", "ru_RU", "vi_VN"};')
    text=text.replace('int index = preferences.getInt("lc_index", -1);',
                      'int index = preferences.getInt("lc_index", 3);')
    write(path,text)

    manager=root/"app/app/src/main/java/com/winlator/container/ContainerManager.java"
    source=read(manager)
    old='''                    if (file.isDirectory()) {
                        if (file.getName().startsWith(RootFS.USER+"-")) {
                            Container container = new Container(Integer.parseInt(file.getName().replace(RootFS.USER+"-", "")));
                            container.setRootDir(new File(homeDir, RootFS.USER+"-"+container.id));
                            JSONObject data = new JSONObject(FileUtils.readString(container.getConfigFile()));
                            container.loadData(data);
                            containers.add(container);
                            maxContainerId = Math.max(maxContainerId, container.id);
                        }
                    }'''
    new='''                    if (!file.isDirectory() || !file.getName().startsWith(RootFS.USER+"-")) continue;
                    String idText = file.getName().substring((RootFS.USER+"-").length());
                    File config = new File(file, ".container");
                    if (!config.isFile()) continue;
                    try {
                        int id = Integer.parseInt(idText);
                        Container container = new Container(id);
                        container.setRootDir(file);
                        JSONObject data = new JSONObject(FileUtils.readString(config));
                        container.loadData(data);
                        containers.add(container);
                        maxContainerId = Math.max(maxContainerId, id);
                    }
                    catch (NumberFormatException | JSONException ignored) {}'''
    if old in source:
        source=source.replace(old,new,1)
    elif new not in source:
        raise RuntimeError("Could not locate container loading loop")
    source=source.replace("catch (JSONException e) {}", "catch (Exception ignored) {}", 1)
    write(manager,source)

def patch_rootfs_validation(root: Path) -> None:
    rootfs_path=root/"app/app/src/main/java/com/winlator/xenvironment/RootFS.java"
    source=read(rootfs_path)
    old="""    public boolean isValid() {
        return rootDir.isDirectory() && getRFSVersionFile().exists();
    }"""
    new="""    public boolean hasRequiredBinaries() {
        File box64 = new File(rootDir, "usr/local/bin/box64");
        File wine = new File(rootDir, "opt/wine/bin/wine");
        return box64.isFile() && box64.length() > 0 && box64.canExecute()
            && wine.isFile() && wine.length() > 0 && wine.canExecute();
    }

    public boolean isValid() {
        return rootDir.isDirectory() && getRFSVersionFile().exists() && hasRequiredBinaries();
    }"""
    if old in source:
        source=source.replace(old,new,1)
    elif new not in source:
        raise RuntimeError("Could not locate RootFS validity check")
    write(rootfs_path,source)

    installer_path=root/"app/app/src/main/java/com/winlator/xenvironment/RootFSInstaller.java"
    installer=read(installer_path)
    old="""            if (success) {
                rootFS.createRFSVersionFile(LATEST_VERSION);
                resetContainerRFSVersions(activity);
            }
            else AppUtils.showToast(activity, R.string.unable_to_install_system_files);"""
    new="""            if (success && rootFS.hasRequiredBinaries()) {
                rootFS.createRFSVersionFile(LATEST_VERSION);
                resetContainerRFSVersions(activity);
            }
            else {
                File versionFile = rootFS.getRFSVersionFile();
                if (versionFile.exists()) versionFile.delete();
                AppUtils.showToast(activity, R.string.unable_to_install_system_files);
            }"""
    if old in installer:
        installer=installer.replace(old,new,1)
    elif new not in installer:
        raise RuntimeError("Could not locate RootFS installation success handler")
    write(installer_path,installer)

def patch_startup_flow(root: Path) -> None:
    activity_path=root/"app/app/src/main/java/com/winlator/XServerDisplayActivity.java"
    source=read(activity_path)
    for imp in ("import android.util.Log;", "import android.os.Handler;", "import android.os.Looper;",
                "import androidx.appcompat.app.AlertDialog;"):
        if imp not in source:
            anchor="import android.app.Activity;"
            if imp.startswith("import androidx."):
                anchor="import androidx.appcompat.app.AppCompatActivity;"
            elif imp.startswith("import android.os."):
                anchor="import android.os.Bundle;"
            source=source.replace(anchor,anchor+"\n"+imp,1)

    field_anchor="    private String screenEffectProfile;"
    fields="""    private String screenEffectProfile;
    private final Handler novaBoxStartupHandler = new Handler(Looper.getMainLooper());
    private Runnable novaBoxStartupTimeout;
    private boolean novaBoxStartupWindowReady = false;
"""
    if "novaBoxStartupTimeout" not in source:
        source=replace_once(source,field_anchor,fields,"NovaBox startup diagnostic fields")

    flag_anchor='        final boolean[] flags = {false, shortcut != null || getIntent().hasExtra("exec_path")};'
    flag_replacement=flag_anchor+"""
        novaBoxStartupTimeout = () -> {
            if (!novaBoxStartupWindowReady && !isFinishing() && !isDestroyed()) {
                preloaderDialog.close();
                new AlertDialog.Builder(this)
                    .setTitle("NovaBox")
                    .setMessage("Wine chưa tạo được cửa sổ Windows sau 120 giây. Hãy kiểm tra tệp hệ thống, phiên bản Box64 và trình điều khiển đồ họa của môi trường. Nếu đây là lần chạy đầu tiên, hãy bảo đảm bộ dữ liệu Windows đã cài đặt đầy đủ.")
                    .setPositiveButton("Đóng", (dialog, which) -> finish())
                    .setCancelable(false)
                    .show();
            }
        };
        novaBoxStartupHandler.postDelayed(novaBoxStartupTimeout, 120000L);"""
    if "novaBoxStartupHandler.postDelayed" not in source:
        source=replace_once(source,flag_anchor,flag_replacement,"NovaBox startup timeout")

    # Close the overlay for any renderable X11 window. Some Wine desktop windows
    # do not report WM_CLASS, so requiring a non-empty class can leave loading forever.
    source=source.replace(
        "if (!flags[0] && window.isRenderable() && !window.getClassName().isEmpty()) {",
        "if (!flags[0] && window.isRenderable()) {", 1)

    map_anchor="""                    preloaderDialog.closeOnUiThread();
                    flags[0] = true;"""
    map_replacement="""                    novaBoxStartupWindowReady = true;
                    if (novaBoxStartupTimeout != null) novaBoxStartupHandler.removeCallbacks(novaBoxStartupTimeout);
                    preloaderDialog.closeOnUiThread();
                    flags[0] = true;"""
    if "novaBoxStartupWindowReady = true" not in source:
        source=replace_once(source,map_anchor,map_replacement,"first Wine window startup completion")

    thread_old="""        Executors.newSingleThreadExecutor().execute(() -> {
            if (!isGenerateWineprefix()) {
                setupWineSystemFiles();
                extractGraphicsDriverFiles();
                changeWineAudioDriver();
            }
            setupXEnvironment();
        });"""
    thread_new="""        Executors.newSingleThreadExecutor().execute(() -> {
            final String[] startupStage = {"Chuẩn bị tệp hệ thống Windows"};
            try {
                if (!isGenerateWineprefix()) {
                    startupStage[0] = "Chuẩn bị tệp hệ thống Windows";
                    setupWineSystemFiles();
                    startupStage[0] = "Nạp tệp trình điều khiển đồ họa";
                    extractGraphicsDriverFiles();
                    startupStage[0] = "Thiết lập âm thanh";
                    changeWineAudioDriver();
                }
                startupStage[0] = "Khởi chạy bộ máy Wine và Box64";
                setupXEnvironment();
            }
            catch (Throwable error) {
                final String failedStage = startupStage[0];
                final String reason = error.getClass().getSimpleName() +
                    (error.getMessage() != null ? ": " + error.getMessage() : "");
                Log.e("NovaBoxStartup", "Startup failed at " + failedStage, error);
                novaBoxStartupHandler.removeCallbacks(novaBoxStartupTimeout);
                runOnUiThread(() -> {
                    preloaderDialog.close();
                    if (!isFinishing() && !isDestroyed()) {
                        new AlertDialog.Builder(this)
                            .setTitle("Không thể khởi động NovaBox")
                            .setMessage("Bước gặp lỗi: " + failedStage + "\\n\\n" + reason +
                                "\\n\\nHãy kiểm tra môi trường Windows, dung lượng trống và cấu hình driver.")
                            .setPositiveButton("Đóng", (dialog, which) -> finish())
                            .setCancelable(false)
                            .show();
                    }
                });
            }
        });"""
    if "final String[] startupStage" not in source:
        source=replace_once(source,thread_old,thread_new,"guarded Windows startup worker")

    destroy_anchor="""    protected void onDestroy() {
        winHandler.stop();"""
    destroy_new="""    protected void onDestroy() {
        if (novaBoxStartupTimeout != null) novaBoxStartupHandler.removeCallbacks(novaBoxStartupTimeout);
        winHandler.stop();"""
    if "removeCallbacks(novaBoxStartupTimeout)" not in source[source.find("protected void onDestroy"):]:
        source=replace_once(source,destroy_anchor,destroy_new,"startup timeout cleanup")

    root_anchor="""            container = containerManager.getContainerById(getIntent().getIntExtra("container_id", 0));
            containerManager.activateContainer(container);"""
    root_new="""            container = containerManager.getContainerById(getIntent().getIntExtra("container_id", 0));
            if (container == null) {
                new AlertDialog.Builder(this).setTitle("NovaBox")
                    .setMessage("Không tìm thấy môi trường Windows đã chọn. Hãy quay lại thư viện và chọn lại môi trường.")
                    .setPositiveButton("Đóng", (dialog, which) -> finish()).show();
                return;
            }
            containerManager.activateContainer(container);"""
    if "Không tìm thấy môi trường Windows đã chọn" not in source:
        source=replace_once(source,root_anchor,root_new,"missing container guard")

    launch_anchor="        environment.startEnvironmentComponents();"
    launch_new=launch_anchor+"""
        if (container != null && guestProgramLauncherComponent.getProcessId() <= 0) {
            throw new IllegalStateException("Không tạo được tiến trình Box64/Wine. " + ProcessHelper.getLastExecError());
        }"""
    if "guestProgramLauncherComponent.getProcessId()" not in source:
        source=replace_once(source,launch_anchor,launch_new,"guest process launch validation")

    write(activity_path,source)

    guest_path=root/"app/app/src/main/java/com/winlator/xenvironment/components/GuestProgramLauncherComponent.java"
    guest=read(guest_path)
    if "public int getProcessId()" not in guest:
        anchor="""    public void setGuestExecutable(String guestExecutable) {
        this.guestExecutable = guestExecutable;
    }"""
        addition=anchor+"""

    public int getProcessId() {
        return pid;
    }"""
        guest=replace_once(guest,anchor,addition,"guest process id accessor")
    write(guest_path,guest)

    helper_path=root/"app/app/src/main/java/com/winlator/core/ProcessHelper.java"
    helper=read(helper_path)
    if "getLastExecError()" not in helper:
        helper=helper.replace("    private static final ArrayList<Callback<String>> debugCallbacks = new ArrayList<>();", '    private static final ArrayList<Callback<String>> debugCallbacks = new ArrayList<>();\n    private static volatile String lastExecError = "";', 1)
        helper=helper.replace("    public static void removeAllDebugCallbacks() {",
            "    public static String getLastExecError() { return lastExecError; }\n\n    public static void removeAllDebugCallbacks() {",1)
        old="""            if (terminationCallback != null) createWaitForThread(process, terminationCallback);
        }
        catch (Exception e) {}
        return pid;"""
        new="""            if (terminationCallback != null) createWaitForThread(process, terminationCallback);
            lastExecError = "";
        }
        catch (Exception e) {
            lastExecError = e.getClass().getSimpleName() + (e.getMessage() != null ? ": " + e.getMessage() : "");
            android.util.Log.e("NovaBoxProcess", "Failed to start guest process: " + command, e);
        }
        return pid;"""
        if old not in helper:
            raise RuntimeError("Could not locate ProcessHelper.exec error handler")
        helper=helper.replace(old,new,1)
        write(helper_path,helper)

    vi=root/"app/app/src/main/res/values-vi/strings.xml"
    # Existing strings are preserved; this message is also used in the native startup dialog.
    if not vi.exists():
        raise RuntimeError("Vietnamese resources were not created before startup patch")
def patch_navigation(root: Path) -> None:
    menu_path=root/"app/app/src/main/res/menu/main_menu.xml"
    menu=read(menu_path)
    if "menu_item_driver_hub" not in menu:
        menu=replace_once(menu,"</group>",
          '        <item android:icon="@drawable/icon_settings" android:id="@+id/menu_item_driver_hub" android:title="@string/driver_hub" />\n    </group>',
          "Driver Hub menu item")
    if "menu_item_steam_library" not in menu:
        menu=replace_once(menu,"</group>",
          '        <item android:icon="@drawable/icon_shortcut" android:id="@+id/menu_item_steam_library" android:title="@string/steam_library" />\n    </group>',
          "Steam Library menu item")
    write(menu_path,menu)

    activity_path=root/"app/app/src/main/java/com/winlator/MainActivity.java"
    activity=read(activity_path)
    if "new DriverHubFragment()" not in activity:
        case_start = activity.find("case R.id.menu_item_settings:")
        if case_start < 0:
            raise RuntimeError("Could not locate MainActivity settings navigation case")
        break_end = activity.find("break;", case_start)
        if break_end < 0:
            raise RuntimeError("Could not locate end of MainActivity settings navigation case")
        break_end += len("break;")
        addition = """case R.id.menu_item_driver_hub:
                showFragment(new DriverHubFragment());
                break;
            case R.id.menu_item_steam_library:
                showFragment(new SteamLibraryFragment());
                break;
            case R.id.menu_item_settings:
                showFragment(new SettingsFragment());
                break;"""
        activity = activity[:case_start] + addition + activity[break_end:]
    if "NovaBox modification" not in activity:
        activity=activity.replace("package com.winlator;","package com.winlator;\n\n/* NovaBox modification: Driver Hub and Steam Library navigation. */",1)
    write(activity_path,activity)
    overlay=Path(__file__).resolve().parents[1]/"overlay"
    for name in ("DriverHubFragment.java","SteamLibraryFragment.java"):
        dest=root/"app/app/src/main/java/com/winlator"/name
        if not dest.exists(): shutil.copyfile(overlay/name,dest)

def main() -> int:
    if len(sys.argv)!=2: raise SystemExit("Usage: apply_branding.py /path/to/winlator")
    root=Path(sys.argv[1]).resolve()
    if not (root/".git").exists(): raise SystemExit(f"Not a Git checkout: {root}")
    patch_gradle(root); patch_manifest(root); patch_resources(root); patch_locale(root); patch_rootfs_validation(root)
    apply_layouts(root); patch_startup_flow(root); patch_navigation(root)
    print(f"NovaBox overlay applied to {root}; upstream notices are retained.")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as error:
        print(f"NovaBox overlay failed: {error}",file=sys.stderr)
        raise SystemExit(1)
