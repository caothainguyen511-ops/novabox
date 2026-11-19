/*
 * NovaBox Steam Library integration.
 * Reads manifests from the user's local Steam installation inside a Wine container.
 * Steam passwords, cookies, and Steam Guard remain in Steam's own client.
 */
package com.winlator;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.winlator.container.Container;
import com.winlator.container.ContainerManager;
import com.winlator.core.WineUtils;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class SteamLibraryFragment extends Fragment {
    private static final int BG=Color.rgb(11,14,22), CARD=Color.rgb(21,26,39);
    private static final int TEXT=Color.rgb(244,246,255), MUTED=Color.rgb(166,177,201);
    private static final int ACCENT=Color.rgb(139,92,246);
    private final ArrayList<Container> containers=new ArrayList<>();
    private ContainerManager manager;
    private Container selected;
    private Spinner selector;
    private LinearLayout results;
    private TextView status, steamPath;
    private File steamExe;

    private static final class Game {
        final String id,name,folder;
        Game(String id,String name,String folder){this.id=id;this.name=name;this.folder=folder;}
    }

    @Override public void onCreate(@Nullable Bundle state){super.onCreate(state);setHasOptionsMenu(false);}
    @Override public void onViewCreated(@NonNull View view,@Nullable Bundle state){
        super.onViewCreated(view,state);
        if(getActivity() instanceof AppCompatActivity){
            AppCompatActivity a=(AppCompatActivity)getActivity();
            if(a.getSupportActionBar()!=null)a.getSupportActionBar().setTitle(R.string.steam_library);
        }
    }

    @Nullable @Override
    public View onCreateView(@NonNull android.view.LayoutInflater inflater,@Nullable ViewGroup parent,@Nullable Bundle state){
        Context c=requireContext();
        manager=new ContainerManager(c);
        ScrollView scroll=new ScrollView(c);scroll.setFillViewport(true);scroll.setBackgroundColor(BG);
        LinearLayout page=new LinearLayout(c);page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(c,16),dp(c,18),dp(c,16),dp(c,26));scroll.addView(page);

        page.addView(text(c,"THƯ VIỆN STEAM",23,TEXT,true));
        page.addView(text(c,"Quét trò chơi đã cài trong từng môi trường Windows NovaBox.",13,MUTED,false),params(c,-1,-2,0,6,0,12));

        LinearLayout top=card(c);page.addView(top,params(c,-1,-2,0,0,0,12));
        top.addView(text(c,"CHỌN MÔI TRƯỜNG WINDOWS",11,ACCENT,true));
        selector=new Spinner(c);top.addView(selector,params(c,-1,48,0,8,0,0));
        steamPath=text(c,"Chưa quét Steam",12,MUTED,false);top.addView(steamPath,params(c,-1,-2,0,8,0,0));
        LinearLayout actions=new LinearLayout(c);actions.setOrientation(LinearLayout.HORIZONTAL);
        top.addView(actions,params(c,-1,48,0,12,0,0));
        Button scan=button(c,"LÀM MỚI THƯ VIỆN",true);actions.addView(scan,new LinearLayout.LayoutParams(0,dp(c,44),1));
        scan.setOnClickListener(v->scan());
        Button open=button(c,"MỞ STEAM",false);LinearLayout.LayoutParams op=new LinearLayout.LayoutParams(0,dp(c,44),1);op.leftMargin=dp(c,8);actions.addView(open,op);
        open.setOnClickListener(v->launch(null));

        LinearLayout notice=card(c);page.addView(notice,params(c,-1,-2,0,0,0,12));
        notice.addView(text(c,"BẢO MẬT TÀI KHOẢN",11,ACCENT,true));
        notice.addView(text(c,"Đăng nhập và xác thực Steam Guard ngay trong ứng dụng Steam. NovaBox không yêu cầu mật khẩu, không lưu cookie và không cần khóa API.",13,MUTED,false),params(c,-1,-2,0,6,0,0));
        status=text(c,"Chọn môi trường rồi nhấn LÀM MỚI THƯ VIỆN.",13,MUTED,false);
        page.addView(status,params(c,-1,-2,0,4,0,10));
        results=new LinearLayout(c);results.setOrientation(LinearLayout.VERTICAL);page.addView(results);
        loadContainers(c);
        return scroll;
    }

    private void loadContainers(Context c){
        containers.clear();containers.addAll(manager.getContainers());
        ArrayList<String> names=new ArrayList<>();for(Container x:containers)names.add(x.getName());
        if(names.isEmpty())names.add("Chưa có môi trường Windows");
        selector.setAdapter(new ArrayAdapter<>(c,android.R.layout.simple_spinner_dropdown_item,names));
        selector.setEnabled(!containers.isEmpty());
        selected=containers.isEmpty()?null:containers.get(0);
        if(selected==null)status.setText("Hãy tạo môi trường Windows rồi cài Steam vào đó.");
        selector.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener(){
            @Override public void onItemSelected(android.widget.AdapterView<?> p,View v,int position,long id){
                selected=position>=0&&position<containers.size()?containers.get(position):null;
                steamExe=null;results.removeAllViews();
                steamPath.setText("Chưa quét Steam trong môi trường này.");
                status.setText("Nhấn LÀM MỚI THƯ VIỆN để tìm Steam và game đã cài.");
            }
            @Override public void onNothingSelected(android.widget.AdapterView<?> p){}
        });
    }

    private void scan(){
        results.removeAllViews();
        if(selected==null){status.setText("Chưa có môi trường Windows. Hãy tạo môi trường trước.");return;}
        ArrayList<File> libraries=findLibraries(selected);
        Map<String,Game> games=new LinkedHashMap<>();steamExe=null;
        for(File apps:libraries){
            File exe=new File(apps.getParentFile(),"steam.exe");
            if(exe.isFile()&&steamExe==null)steamExe=exe;
            File[] manifests=apps.listFiles((dir,name)->name.startsWith("appmanifest_")&&name.endsWith(".acf"));
            if(manifests==null)continue;
            for(File manifest:manifests){
                Game game=parseManifest(manifest,apps.getParentFile());
                if(game!=null)games.put(game.id,game);
            }
        }
        if(steamExe==null){
            status.setText("Không tìm thấy ứng dụng Steam trong môi trường này.");
            steamPath.setText("Cài Steam vào môi trường đang chọn, sau đó quét lại.");
            Button help=button(requireContext(),"Mở trang Steam chính thức",false);
            results.addView(help,params(requireContext(),-1,46,0,10,0,0));
            help.setOnClickListener(v->startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://store.steampowered.com/about/"))));
            return;
        }
        steamPath.setText("Steam: "+steamExe.getParent());
        status.setText("Đã tìm thấy "+games.size()+" trò chơi trong "+libraries.size()+" thư viện Steam.");
        if(games.isEmpty()){
            results.addView(text(requireContext(),"Chưa thấy game đã cài. MỞ STEAM để đăng nhập hoặc cài game vào container này.",13,MUTED,false));
            return;
        }
        ArrayList<Game> sorted=new ArrayList<>(games.values());sorted.sort((a,b)->a.name.compareToIgnoreCase(b.name));
        for(Game game:sorted)addGame(game);
    }

    private ArrayList<File> findLibraries(Container container){
        LinkedHashMap<String,File> libs=new LinkedHashMap<>();
        File cDrive=new File(container.getRootDir(),".wine/drive_c");
        addLibrary(libs,new File(cDrive,"Program Files (x86)/Steam/steamapps"));
        addLibrary(libs,new File(cDrive,"Program Files/Steam/steamapps"));
        addLibrary(libs,new File(cDrive,"Steam/steamapps"));
        ArrayList<File> initial=new ArrayList<>(libs.values());
        Pattern pathPattern=Pattern.compile("\"path\"\\s+\"([^\"]+)\"",Pattern.CASE_INSENSITIVE);
        for(File apps:initial){
            Matcher m=pathPattern.matcher(read(apps.toPath().resolve("libraryfolders.vdf").toFile()));
            while(m.find()){
                String windows=m.group(1).replace("\\\\","\\");
                String unix=WineUtils.dosToUnixPath(windows,container);
                if(!unix.isEmpty())addLibrary(libs,new File(unix,"steamapps"));
            }
        }
        return new ArrayList<>(libs.values());
    }

    private static void addLibrary(Map<String,File> libs,File apps){
        if(!apps.isDirectory())return;
        try{libs.put(apps.getCanonicalPath(),apps);}
        catch(IOException e){libs.put(apps.getAbsolutePath(),apps);}
    }

    private static Game parseManifest(File manifest,File libraryRoot){
        String body=read(manifest);
        String id=field(body,"appid"),name=field(body,"name"),folder=field(body,"installdir");
        if(id.isEmpty()||name.isEmpty()||!id.matches("[0-9]{1,12}"))return null;
        File install=new File(new File(libraryRoot,"steamapps/common"),folder);
        if(!install.isDirectory())return null;
        return new Game(id,name,folder);
    }

    private static String field(String text,String key){
        Matcher m=Pattern.compile("\""+Pattern.quote(key)+"\"\\s+\"([^\"]*)\"",Pattern.CASE_INSENSITIVE).matcher(text);
        return m.find()?m.group(1):"";
    }
    private static String read(File file){
        if(file==null||!file.isFile())return "";
        try{return new String(Files.readAllBytes(file.toPath()),StandardCharsets.UTF_8);}
        catch(IOException e){return "";}
    }

    private void addGame(Game game){
        Context c=requireContext();LinearLayout item=card(c);
        results.addView(item,params(c,-1,-2,0,0,0,10));
        item.addView(text(c,game.name,15,TEXT,true));
        item.addView(text(c,"Steam AppID: "+game.id+" · "+game.folder,11,MUTED,false),params(c,-1,-2,0,5,0,0));
        Button play=button(c,"CHẠY qua Steam",true);item.addView(play,params(c,-1,42,0,10,0,0));
        play.setOnClickListener(v->launch(game.id));
    }

    private void launch(@Nullable String appId){
        if(selected==null){status.setText("Chọn một môi trường Windows trước.");return;}
        if(steamExe==null||!steamExe.isFile()){status.setText("Chưa tìm thấy Steam.exe. Cài Steam vào container rồi quét lại.");return;}
        String target=steamExe.getPath();
        if(appId!=null&&appId.matches("[0-9]{1,12}"))target+=" -applaunch "+appId;
        Intent i=new Intent(requireActivity(),XServerDisplayActivity.class);
        i.putExtra("container_id",selected.id);i.putExtra("exec_path",target);
        startActivity(i);
    }

    private static LinearLayout card(Context c){
        LinearLayout l=new LinearLayout(c);l.setOrientation(LinearLayout.VERTICAL);
        l.setPadding(dp(c,14),dp(c,13),dp(c,14),dp(c,13));
        GradientDrawable bg=new GradientDrawable();bg.setColor(CARD);bg.setCornerRadius(dp(c,16));
        bg.setStroke(dp(c,1),Color.rgb(43,49,70));l.setBackground(bg);return l;
    }
    private static TextView text(Context c,String s,int size,int color,boolean bold){
        TextView t=new TextView(c);t.setText(s);t.setTextSize(size);t.setTextColor(color);
        t.setTypeface(Typeface.DEFAULT,bold?Typeface.BOLD:Typeface.NORMAL);t.setLineSpacing(dp(c,3),1f);return t;
    }
    private static Button button(Context c,String label,boolean primary){
        Button b=new Button(c);b.setText(label);b.setAllCaps(false);b.setTextSize(13);b.setTextColor(TEXT);
        GradientDrawable bg=new GradientDrawable();bg.setCornerRadius(dp(c,12));
        if(primary)bg.setColor(ACCENT);else{bg.setColor(Color.rgb(29,35,52));bg.setStroke(dp(c,1),Color.rgb(63,70,98));}
        b.setBackground(bg);return b;
    }
    private static LinearLayout.LayoutParams params(Context c,int w,int h,int l,int t,int r,int b){
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(w<0?w:dp(c,w),h<0?h:dp(c,h));
        p.setMargins(dp(c,l),dp(c,t),dp(c,r),dp(c,b));return p;
    }
    private static int dp(Context c,int v){return Math.round(v*c.getResources().getDisplayMetrics().density);}
}
