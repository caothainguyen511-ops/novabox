# Hướng dẫn NovaBox

## Chạy ứng dụng Windows

1. Mở **Môi trường Windows** và tạo một container riêng cho mỗi game hoặc ứng dụng.
2. Dùng trình quản lý tệp của container để mở tệp cài đặt Windows (.exe) mà bạn có quyền sử dụng.
3. Nhấn chạy trong môi trường đó. Game sẽ mở trong màn hình XServer của NovaBox.
4. Tạo shortcut sau khi cài đặt xong để lần sau chạy nhanh hơn.

## Chọn driver

- Adreno: bắt đầu với Turnip nếu thiết bị hỗ trợ Vulkan phù hợp.
- Mali / Immortalis / Xclipse: giữ driver hệ thống; thử Vortek hoặc backend được engine hỗ trợ. Không dùng Turnip như driver Mali.
- Game Direct3D 9/10/11: thử DXVK khi Vulkan hoạt động ổn.
- Game Direct3D 12: VKD3D, chỉ khi driver và GPU hỗ trợ các tính năng Vulkan cần thiết.
- Nếu game lỗi hình hoặc không mở: thử WineD3D, hạ độ phân giải hoặc quay về cấu hình container đã hoạt động.

Đổi từng thiết lập một để dễ xác định nguyên nhân. Điện thoại có thể giảm hiệu năng khi nóng hoặc thiếu RAM.

## Đồng bộ Steam

1. Tạo môi trường Windows, cài Steam vào chính môi trường đó và đăng nhập trong Steam.
2. Mở **Steam Library**, chọn môi trường vừa cài Steam và nhấn **Đồng bộ thư viện**.
3. Chọn game và nhấn **Chạy qua Steam**. Steam Guard tiếp tục hoạt động bên trong Steam.

NovaBox chỉ đọc thư viện cục bộ và AppID. Nó không lấy mật khẩu, cookie hay bỏ qua quyền sở hữu game.
