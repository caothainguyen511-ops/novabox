/*
 * NovaBox addition, 2026-11-19.
 * Vietnamese-first graphics driver and compatibility dashboard.
 * Keep upstream Winlator LGPL-2.1 notices intact.
 */
package com.winlator;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.winlator.core.DefaultVersion;
import com.winlator.core.GeneralComponents;
import com.winlator.core.GPUHelper;

import java.util.Locale;

public class DriverHubFragment extends Fragment {
    private static final int BG = Color.rgb(11, 14, 22);
    private static final int CARD = Color.rgb(21, 26, 39);
    private static final int TEXT = Color.rgb(244, 246, 255);
    private static final int MUTED = Color.rgb(166, 177, 200);
    private static final int ACCENT = Color.rgb(139, 92, 246);
    private static final int CYAN = Color.rgb(34, 211, 238);
    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private TextView gpuInfo;
    private TextView recommendation;

    @Override public void onCreate(@Nullable Bundle state) {
        super.onCreate(state);
        setHasOptionsMenu(false);
    }

    @Override public void onViewCreated(@NonNull View view, @Nullable Bundle state) {
        super.onViewCreated(view, state);
        if (getActivity() instanceof AppCompatActivity) {
            AppCompatActivity a=(AppCompatActivity)getActivity();
            if(a.getSupportActionBar()!=null) a.getSupportActionBar().setTitle(R.string.driver_hub);
        }
        detectGpuAsync();
    }

    @Nullable @Override
    public View onCreateView(@NonNull android.view.LayoutInflater inflater,
            @Nullable ViewGroup parent, @Nullable Bundle state) {
        Context c=requireContext();
        ScrollView scroll=new ScrollView(c);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(BG);
        LinearLayout page=new LinearLayout(c);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(c,18),dp(c,20),dp(c,18),dp(c,28));
        scroll.addView(page,new ScrollView.LayoutParams(-1,-2));

        page.addView(text(c,"NOVA  /  WINDOWS COMPATIBILITY",12,CYAN,true));
        page.addView(text(c,"Trung tâm Driver",28,TEXT,true),params(c,-1,-2,0,4,0,2));
        page.addView(text(c,"Nhận diện GPU, cài component và chọn cấu hình phù hợp cho từng môi trường.",14,MUTED,false));

        LinearLayout gpu=card(c);
        page.addView(gpu,params(c,-1,-2,0,18,0,0));
        gpu.addView(text(c,"THIẾT BỊ CỦA BẠN",11,CYAN,true));
        gpuInfo=text(c,"Đang nhận diện GPU…",15,TEXT,true);
        gpu.addView(gpuInfo,params(c,-1,-2,0,8,0,0));
        recommendation=text(c,"Đang kiểm tra cấu hình đề xuất…",13,MUTED,false);
        gpu.addView(recommendation,params(c,-1,-2,0,6,0,0));

        addSection(page,c,"1. Driver đồ họa","Turnip dành cho Adreno tương thích. Vortek là backend Vulkan được engine tích hợp cho một số GPU khác; Gladio, Zink và VirGL là các backend OpenGL. Không cài Turnip lên Mali.");
        addSection(page,c,"2. DirectX / DX Wrapper","DXVK dành cho Direct3D 9/10/11. VKD3D dành riêng cho Direct3D 12. WineD3D là lựa chọn dự phòng. D7VK và CNC DDraw phục vụ một số game DirectDraw cũ.");
        addSection(page,c,"3. Cài component","Nút tải bên dưới dùng catalog component của upstream Winlator. Sau đó chọn phiên bản trong cấu hình môi trường Windows; không cài tất cả phiên bản cùng lúc.");

        addInstaller(page,c,GeneralComponents.Type.TURNIP,"Turnip · Vulkan / Adreno","Mesa Vulkan driver cho GPU Adreno. Không dùng làm driver Mali.",DefaultVersion.TURNIP);
        addInstaller(page,c,GeneralComponents.Type.ADRENOTOOLS_DRIVER,"Driver Adreno bổ sung","Nhập gói AdrenoTools ZIP có manifest từ nguồn đáng tin cậy, đúng GPU và Android.", "System");
        addInstaller(page,c,GeneralComponents.Type.DXVK,"DXVK · Direct3D 9 / 10 / 11","Dịch Direct3D 9–11 sang Vulkan. Chỉ bật khi Vulkan driver tương thích.",DefaultVersion.MINOR_DXVK);
        addInstaller(page,c,GeneralComponents.Type.VKD3D,"VKD3D · Direct3D 12","Dành cho game Direct3D 12; độc lập với DXVK.",DefaultVersion.VKD3D);
        addInstaller(page,c,GeneralComponents.Type.WINED3D,"WineD3D · Fallback","Lựa chọn thay thế khi DXVK/Vulkan gặp lỗi tương thích.",DefaultVersion.WINED3D);
        addInstaller(page,c,GeneralComponents.Type.BOX64,"Box64 · Runtime x86_64","Lớp chạy ứng dụng Windows 64-bit trên Android ARM64.",DefaultVersion.BOX64);

        LinearLayout backends=card(c);
        page.addView(backends,params(c,-1,-2,0,12,0,0));
        backends.addView(text(c,"BACKEND ĐƯỢC TÍCH HỢP",11,CYAN,true));
        backends.addView(text(c,"Vulkan: Turnip · Vortek\nOpenGL: Gladio · Zink · VirGL\nLegacy: D7VK · CNC DDraw",14,TEXT,false),params(c,-1,-2,0,8,0,0));
        backends.addView(text(c,"Các backend trên được lấy từ engine và module upstream. Driver Mali độc quyền vẫn do nhà sản xuất thiết bị cung cấp.",12,MUTED,false),params(c,-1,-2,0,8,0,0));

        LinearLayout warning=card(c);
        page.addView(warning,params(c,-1,-2,0,12,0,0));
        warning.addView(text(c,"LƯU Ý ỔN ĐỊNH",11,Color.rgb(251,191,36),true));
        warning.addView(text(c,"• Mỗi game nên có môi trường riêng.\n• Chỉ đổi một thiết lập mỗi lần.\n• Nếu game không mở, thử WineD3D hoặc quay về cấu hình đã chạy ổn.\n• Theo dõi nhiệt độ và RAM.\n• Không thay driver hệ thống bằng gói không rõ nguồn.",13,MUTED,false),params(c,-1,-2,0,8,0,0));

        Button create=actionButton(c,"＋  Tạo môi trường Windows");
        page.addView(create,params(c,-1,50,0,18,0,0));
        create.setOnClickListener(v->openContainerCreator());
        Button environments=secondaryButton(c,"Mở môi trường đã tạo");
        page.addView(environments,params(c,-1,48,0,10,0,0));
        environments.setOnClickListener(v->{if(getActivity() instanceof MainActivity)((MainActivity)getActivity()).showFragment(new ContainersFragment());});
        Button library=secondaryButton(c,"Mở thư viện ứng dụng");
        page.addView(library,params(c,-1,48,0,10,0,0));
        library.setOnClickListener(v->{if(getActivity() instanceof MainActivity)((MainActivity)getActivity()).showFragment(new ShortcutsFragment());});
        return scroll;
    }

    private void addSection(LinearLayout page,Context c,String heading,String body){
        LinearLayout item=card(c);page.addView(item,params(c,-1,-2,0,12,0,0));
        item.addView(text(c,heading,16,TEXT,true));
        item.addView(text(c,body,13,MUTED,false),params(c,-1,-2,0,6,0,0));
    }

    private void addInstaller(LinearLayout page,Context c,GeneralComponents.Type type,String heading,String body,String defaultVersion){
        LinearLayout item=card(c);page.addView(item,params(c,-1,-2,0,10,0,0));
        item.addView(text(c,heading,15,TEXT,true));
        item.addView(text(c,body+" Gói đã tải sẽ xuất hiện trong bộ chọn component của môi trường Windows.",12,MUTED,false),params(c,-1,-2,0,5,0,0));
        Spinner versions=new Spinner(c);item.addView(versions,params(c,-1,44,0,8,0,0));
        LinearLayout controls=new LinearLayout(c);controls.setOrientation(LinearLayout.HORIZONTAL);
        controls.setGravity(Gravity.CENTER_VERTICAL);item.addView(controls,params(c,-1,44,0,8,0,0));
        Button install=smallButton(c,type==GeneralComponents.Type.ADRENOTOOLS_DRIVER?"Nhập driver ZIP":"Tải gói");
        install.setTag("install");controls.addView(install,new LinearLayout.LayoutParams(0,dp(c,42),1));
        Button remove=smallButton(c,"Gỡ bản đã tải");remove.setTag("remove");
        LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(0,dp(c,42),1);rp.leftMargin=dp(c,8);controls.addView(remove,rp);
        GeneralComponents.initViews(type,controls,versions,null,defaultVersion);
    }

    private void detectGpuAsync(){
        final Context c=getContext();if(c==null)return;
        Thread worker=new Thread(()->{
            String vendor="",renderer="",version="",failure=null;
            try{vendor=GPUHelper.glGetVendor(c);renderer=GPUHelper.glGetRenderer(c);version=GPUHelper.glGetVersion(c);}
            catch(Throwable e){failure=e.getClass().getSimpleName()+": "+String.valueOf(e.getMessage());}
            final String v=vendor,r=renderer,g=version,f=failure;
            mainHandler.post(()->{
                if(!isAdded()||gpuInfo==null||recommendation==null)return;
                if(f!=null){gpuInfo.setText("Chưa đọc được thông tin GPU");recommendation.setText("Giữ cấu hình tự động của engine. "+f);return;}
                String combined=(v+" "+r).toLowerCase(Locale.ROOT);
                gpuInfo.setText((v.isEmpty()?"GPU":v)+"\n"+(r.isEmpty()?"Renderer chưa xác định":r)+(g.isEmpty()?"":"\n"+g));
                if(combined.contains("adreno"))recommendation.setText("Đề xuất: Vulkan = Turnip · OpenGL = Gladio. Giữ driver hệ thống làm dự phòng.");
                else if(combined.contains("mali")||combined.contains("immortalis")||combined.contains("xclipse"))recommendation.setText("Đề xuất: thử Vortek và Gladio; không chọn Turnip. Giữ driver hệ thống làm dự phòng.");
                else recommendation.setText("GPU chưa có hồ sơ: giữ lựa chọn tự động và thử từng game với một thay đổi mỗi lần.");
            });
        },"NovaBox-GPU-Detect");worker.setDaemon(true);worker.start();
    }

    private void openContainerCreator(){
        if(!(getActivity() instanceof MainActivity))return;
        MainActivity a=(MainActivity)getActivity();
        a.getSupportFragmentManager().beginTransaction().addToBackStack(null)
            .replace(R.id.FLFragmentContainer,new ContainerDetailFragment()).commit();
    }
    private static LinearLayout card(Context c){
        LinearLayout l=new LinearLayout(c);l.setOrientation(LinearLayout.VERTICAL);
        l.setPadding(dp(c,16),dp(c,15),dp(c,16),dp(c,15));
        GradientDrawable b=new GradientDrawable();b.setColor(CARD);b.setCornerRadius(dp(c,18));b.setStroke(dp(c,1),Color.rgb(43,49,70));l.setBackground(b);return l;
    }
    private static TextView text(Context c,String value,int size,int color,boolean bold){
        TextView t=new TextView(c);t.setText(value);t.setTextSize(size);t.setTextColor(color);
        t.setTypeface(Typeface.DEFAULT,bold?Typeface.BOLD:Typeface.NORMAL);t.setLineSpacing(dp(c,3),1f);return t;
    }
    private static Button smallButton(Context c,String label){
        Button b=new Button(c);b.setText(label);b.setTextSize(12);b.setTextColor(TEXT);b.setAllCaps(false);
        b.setMinHeight(dp(c,40));b.setPadding(dp(c,8),0,dp(c,8),0);return b;
    }
    private static Button actionButton(Context c,String label){
        Button b=smallButton(c,label);b.setBackground(new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{ACCENT,Color.rgb(99,102,241)}));b.setTextSize(15);b.setTextColor(Color.WHITE);return b;
    }
    private static Button secondaryButton(Context c,String label){
        Button b=smallButton(c,label);GradientDrawable bg=new GradientDrawable();bg.setColor(Color.rgb(29,35,52));bg.setCornerRadius(dp(c,14));bg.setStroke(dp(c,1),Color.rgb(63,70,98));b.setBackground(bg);return b;
    }
    private static LinearLayout.LayoutParams params(Context c,int w,int h,int l,int t,int r,int b){
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(w<0?w:dp(c,w),h<0?h:dp(c,h));p.setMargins(dp(c,l),dp(c,t),dp(c,r),dp(c,b));return p;
    }
    private static int dp(Context c,int v){return Math.round(v*c.getResources().getDisplayMetrics().density);}
}
