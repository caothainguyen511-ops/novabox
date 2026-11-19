from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PATCHER = ROOT / "scripts" / "apply_branding.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    fixtures = {
        "app/app/build.gradle": """android { namespace 'com.winlator' defaultConfig { applicationId 'com.winlator' versionName "11.2" } }""",
        "app/app/src/main/AndroidManifest.xml": """<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.winlator">
<application android:icon="@mipmap/ic_launcher">
<activity android:name="com.winlator.MainActivity" android:exported="true">
<intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter>
</activity>
<provider android:authorities="com.winlator.FileProvider" />
</application></manifest>""",
        "app/app/src/main/res/values/strings.xml": '<resources><string name="app_name">Winlator</string><string name="shortcuts">Shortcuts</string><string name="containers">Containers</string><string name="input_controls">Input Controls</string><string name="settings">Settings</string><string name="about">About</string></resources>',
        "app/app/src/main/res/values/styles.xml": '<resources><style name="AppThemeDark"><item name="colorAccent">#0288d1</item><item name="colorPrimarySurface">#1b1e21</item></style></resources>',
        "app/app/src/main/res/menu/main_menu.xml": '<menu xmlns:android="http://schemas.android.com/apk/res/android"><group android:checkableBehavior="single"><item android:id="@+id/menu_item_about" /></group></menu>',
        "app/app/src/main/res/layout/main_menu_header.xml": "<FrameLayout />",
        "app/app/src/main/res/layout/container_list_item.xml": '<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" android:orientation="horizontal" android:paddingLeft="16dp" android:paddingRight="16dp" android:gravity="center_vertical" />',
        "app/app/src/main/java/com/winlator/XServerDisplayActivity.java": """package com.winlator;
import android.app.Activity;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
class XServerDisplayActivity extends AppCompatActivity {
    private String screenEffectProfile;
    void onCreate() {
        final boolean[] flags = {false, shortcut != null || getIntent().hasExtra("exec_path")};
        xServer.windowManager.addOnWindowModificationListener(new WindowManager.OnWindowModificationListener() {
            public void onMapWindow(Window window) {
                if (!flags[0] && window.isRenderable() && !window.getClassName().isEmpty()) {
                    preloaderDialog.closeOnUiThread();
                    flags[0] = true;
                }
            }
        });
        Executors.newSingleThreadExecutor().execute(() -> {
            if (!isGenerateWineprefix()) {
                setupWineSystemFiles();
                extractGraphicsDriverFiles();
                changeWineAudioDriver();
            }
            setupXEnvironment();
        });
    }
    protected void onDestroy() {
        winHandler.stop();
    }
    void openContainer() {
            container = containerManager.getContainerById(getIntent().getIntExtra("container_id", 0));
            containerManager.activateContainer(container);
    }
    void setupXEnvironment() {
        environment.startEnvironmentComponents();
    }
}""",
        "app/app/src/main/java/com/winlator/xenvironment/components/GuestProgramLauncherComponent.java": """package com.winlator.xenvironment.components;
class GuestProgramLauncherComponent {
    public void setGuestExecutable(String guestExecutable) {
        this.guestExecutable = guestExecutable;
    }
}""",
        "app/app/src/main/java/com/winlator/core/ProcessHelper.java": """package com.winlator.core;
import java.util.ArrayList;
class ProcessHelper {
    private static final ArrayList<Callback<String>> debugCallbacks = new ArrayList<>();
    public static void removeAllDebugCallbacks() {
    }
    static int exec(String command, Callback<Integer> terminationCallback) {
        try {
            if (terminationCallback != null) createWaitForThread(process, terminationCallback);
        }
        catch (Exception e) {}
        return pid;
    }
}""",
        "app/app/src/main/java/com/winlator/core/LocaleHelper.java": 'package com.winlator.core; public class LocaleHelper { private static final String[] supportedLocales = {"en_US", "pt_BR", "ru_RU"}; void f(SharedPreferences preferences) { int index = preferences.getInt("lc_index", -1); } }',
        "app/app/src/main/java/com/winlator/xenvironment/RootFS.java": """package com.winlator.xenvironment;
class RootFS {
    private File rootDir;
    public boolean isValid() {
        return rootDir.isDirectory() && getRFSVersionFile().exists();
    }
}""",
        "app/app/src/main/java/com/winlator/xenvironment/RootFSInstaller.java": """package com.winlator.xenvironment;
class RootFSInstaller {
    void install() {
            if (success) {
                rootFS.createRFSVersionFile(LATEST_VERSION);
                resetContainerRFSVersions(activity);
            }
            else AppUtils.showToast(activity, R.string.unable_to_install_system_files);
    }
}""",
        "app/app/src/main/java/com/winlator/container/ContainerManager.java": """package com.winlator.container;
class ContainerManager { void loadContainers() {
                    if (file.isDirectory()) {
                        if (file.getName().startsWith(RootFS.USER+"-")) {
                            Container container = new Container(Integer.parseInt(file.getName().replace(RootFS.USER+"-", "")));
                            container.setRootDir(new File(homeDir, RootFS.USER+"-"+container.id));
                            JSONObject data = new JSONObject(FileUtils.readString(container.getConfigFile()));
                            container.loadData(data);
                            containers.add(container);
                            maxContainerId = Math.max(maxContainerId, container.id);
                        }
                    }
} }""",
        "app/app/src/main/java/com/winlator/contentdialog/AboutDialog.java": """package com.winlator.contentdialog;
class AboutDialog {
    void show() {
        tvWebpage.setText(Html.fromHtml("<a href="https://www.winlator.org">winlator.org</a>", Html.FROM_HTML_MODE_LEGACY));
        String creditsAndThirdPartyAppsHTML = String.join("<br />",
            "GLIBC Patches by (<a href="https://github.com/termux-pacman/glibc-packages">Termux Pacman</a>)",
            "Wine (<a href="https://www.winehq.org">winehq.org</a>)",
            "Box86/Box64 by <a href="https://github.com/ptitSeb">ptitseb</a>"
        );
    }
}""",
        "app/app/src/main/res/layout/about_dialog.xml": """<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
<TextView android:id="@+id/TVWebpage" />
<ImageView android:src="@mipmap/ic_launcher" />
<TextView android:text="@string/credits_and_third_party_apps" />
</LinearLayout>""",
        "app/app/src/main/java/com/winlator/MainActivity.java": """package com.winlator;
public class MainActivity { public boolean onNavigationItemSelected(MenuItem item) { switch (item.getItemId()) {
case R.id.menu_item_settings:
showFragment(new SettingsFragment());
break;
} return true; } }""",
        "app/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml": '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><foreground android:drawable="@mipmap/ic_launcher_foreground" /></adaptive-icon>',
    }
    for relative, source in fixtures.items():
        file = root / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(source, encoding="utf-8")
    (root / ".git").mkdir()
    brand = root / "branding" / "novabox_launcher_foreground.xml"
    brand.parent.mkdir(parents=True, exist_ok=True)
    brand.write_text('''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108"><path android:fillColor="#8B5CF6" android:pathData="M20,23 L43,23 L69,55 L69,23 L88,23 L88,85 L65,85 L39,53 L39,85 L20,85 Z" /></vector>''', encoding="utf-8")

    subprocess.run([sys.executable, str(PATCHER), str(root)], check=True)
    subprocess.run([sys.executable, str(PATCHER), str(root)], check=True)

    gradle = (root / "app/app/build.gradle").read_text()
    assert "com.novabox.emulator" in gradle
    assert "NovaBox" in (root / "app/app/src/main/res/values-vi/strings.xml").read_text()
    locale = (root / "app/app/src/main/java/com/winlator/core/LocaleHelper.java").read_text()
    assert "vi_VN" in locale and 'getInt("lc_index", 3)' in locale
    rootfs = (root / "app/app/src/main/java/com/winlator/xenvironment/RootFS.java").read_text()
    assert "usr/local/bin/box64" in rootfs and "hasRequiredBinaries()" in rootfs
    assert "box64.canExecute()" in rootfs and "wine.canExecute()" in rootfs
    installer = (root / "app/app/src/main/java/com/winlator/xenvironment/RootFSInstaller.java").read_text()
    assert "success && rootFS.hasRequiredBinaries()" in installer
    assert "versionFile.delete()" in installer
    manager = (root / "app/app/src/main/java/com/winlator/container/ContainerManager.java").read_text()
    assert "if (!file.isDirectory() || !file.getName().startsWith" in manager

    about = (root / "app/app/src/main/java/com/winlator/contentdialog/AboutDialog.java").read_text()
    assert "github.com/caothainguyen511-ops/novabox" in about
    assert "winlator.org" not in about
    about_layout = (root / "app/app/src/main/res/layout/about_dialog.xml").read_text()
    assert "@mipmap/novabox_icon" in about_layout and "BỘ TƯƠNG THÍCH WINDOWS CHO ANDROID" in about_layout
    vi_strings = (root / "app/app/src/main/res/values-vi/strings.xml").read_text()
    assert "Giới thiệu NovaBox" in vi_strings and "Trình quản lý tác vụ" in vi_strings
    manifest = root / "app/app/src/main/AndroidManifest.xml"
    ET.parse(manifest)
    manifest_text = manifest.read_text()
    assert 'android:icon="@mipmap/novabox_icon"' in manifest_text
    assert manifest_text.count("android.intent.category.LAUNCHER") == 1

    ET.parse(root / "app/app/src/main/res/mipmap-anydpi-v26/novabox_icon.xml")
    ET.parse(root / "app/app/src/main/res/values/styles.xml")
    activity = (root / "app/app/src/main/java/com/winlator/MainActivity.java").read_text()
    assert "new DriverHubFragment()" in activity
    assert "new SteamLibraryFragment()" in activity
    assert (root / "app/app/src/main/java/com/winlator/SplashActivity.java").is_file()
    splash = (root / "app/app/src/main/java/com/winlator/SplashActivity.java").read_text()
    assert "NOVABOX BY CAOTHAINGUYEN" in splash
    assert (root / "app/app/src/main/java/com/winlator/DriverHubFragment.java").is_file()
    assert (root / "app/app/src/main/java/com/winlator/SteamLibraryFragment.java").is_file()

    menu = (root / "app/app/src/main/res/menu/main_menu.xml").read_text()
    assert menu.count("menu_item_driver_hub") == 1
    assert menu.count("menu_item_steam_library") == 1
    assert "CHƠI GAME WINDOWS TRÊN ANDROID" in (root / "app/app/src/main/res/layout/main_menu_header.xml").read_text()
    startup = (root / "app/app/src/main/java/com/winlator/XServerDisplayActivity.java").read_text()
    assert "novaBoxStartupHandler.postDelayed" in startup
    assert "window.isRenderable() && !window.getClassName().isEmpty()" not in startup
    assert "if (!flags[0] && window.isRenderable())" in startup
    assert "Startup failed at" in startup
    assert "guestProgramLauncherComponent.getProcessId()" in startup
    guest = (root / "app/app/src/main/java/com/winlator/xenvironment/components/GuestProgramLauncherComponent.java").read_text()
    assert "public int getProcessId()" in guest
    helper = (root / "app/app/src/main/java/com/winlator/core/ProcessHelper.java").read_text()
    assert "getLastExecError()" in helper and "NovaBoxProcess" in helper

print("NovaBox overlay fixture test passed")
