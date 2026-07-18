# register.py
import os

class RegisterService:
    def __init__(self, gym_manager):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.accounts = {}
        self.admin_accounts = {}
        self.gym_manager = gym_manager
        self.load_all_accounts()

    def get_file_path(self, file_name):
        return os.path.join(self.current_dir, file_name)

    # ĐỌC SONG SONG FILE ADMIN VÀ FILE THÀNH VIÊN
    def load_all_accounts(self):
        self.admin_accounts = {}
        self.accounts = {}

        # 1. Đọc file admin_data.txt
        admin_path = self.get_file_path("admin_data.txt")
        if os.path.exists(admin_path):
            with open(admin_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        usr, pwd, name, email, phone = parts
                        self.admin_accounts[usr] = {
                            "password": pwd, "role": "Admin", "code": "ADMIN",
                            "name": name, "email": email, "phone": phone
                        }
        else:
            # Tạo sẵn nếu chưa có file admin
            self.admin_accounts["admin"] = {
                "password": "admin", "role": "Admin", "code": "ADMIN",
                "name": "Admin Tối Cao", "email": "admin@gym.com", "phone": "000"
            }
            with open(admin_path, "w", encoding="utf-8") as f:
                f.write("admin|admin|Admin Tối Cao|admin@gym.com|000\n")

        # 2. Đọc file register_data.txt
        reg_path = self.get_file_path("register_data.txt")
        if os.path.exists(reg_path):
            with open(reg_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 8:
                        usr, pwd, role, status, code, name, email, phone = parts
                        self.accounts[usr] = {
                            "password": pwd, "role": role, "status": status, 
                            "code": code, "name": name, "email": email, "phone": phone
                        }

    def save_accounts(self):
        with open(self.get_file_path("register_data.txt"), "w", encoding="utf-8") as f:
            for usr, data in self.accounts.items():
                f.write(f"{usr}|{data['password']}|{data['role']}|{data['status']}|{data['code']}|{data['name']}|{data['email']}|{data['phone']}\n")

    # NGƯỜI DÙNG TỰ ĐĂNG KÝ (TẠO CODE CHỜ DUYỆT)
    def register_account(self):
        print("\n--- ĐĂNG KÝ TÀI KHOẢN MỚI ---")
        username = input("Nhập Username: ").strip()
        
        if username in self.accounts or username in self.admin_accounts:
            print("❌ Tên đăng nhập này đã tồn tại!")
            return

        password = input("Nhập Password: ").strip()
        name = input("Nhập Họ và Tên: ").strip()
        email = input("Nhập Email: ").strip()
        phone = input("Nhập Số điện thoại: ").strip()

        print("\nBạn muốn đăng ký vai trò nào?")
        print("1. Member (Hội viên thường)")
        print("2. Trainer (Huấn luyện viên)")
        choice = input("Lựa chọn (1 hoặc 2): ").strip()

        if choice == "1":
            role = "Member"
            code = self.gym_manager.generate_next_code("M") 
        elif choice == "2":
            role = "Trainer"
            code = self.gym_manager.generate_next_code("T")
        else:
            print("❌ Lựa chọn sai!")
            return

        self.accounts[username] = {
            "password": password, "role": role, "status": "Pending",
            "code": code, "name": name, "email": email, "phone": phone
        }
        self.save_accounts()
        print(f"🎉 Đăng ký hoàn tất! Mã số của bạn: {code}. Vui lòng đợi Admin phê duyệt.")

    # ĐĂNG NHẬP KIỂM TRA ĐA TỆP
    def login(self):
        print("\n--- ĐĂNG NHẬP HỆ THỐNG ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Kiểm tra dữ liệu bộ nhớ Admin trước
        if username in self.admin_accounts and self.admin_accounts[username]["password"] == password:
            return username, "Admin", "ADMIN"

        # Kiểm tra dữ liệu bộ nhớ Hội viên/Trainer sau
        if username in self.accounts and self.accounts[username]["password"] == password:
            acc = self.accounts[username]
            if acc["status"] == "Pending":
                print("❌ Tài khoản này chưa được duyệt! Vui lòng liên hệ Admin.")
                return None, None, None
            return username, acc["role"], acc["code"]
        
        print("❌ Tài khoản hoặc mật khẩu không chính xác!")
        return None, None, None

    # ADMIN DUYỆT
    def approve_accounts_menu(self):
        while True:
            pending_list = [usr for usr, data in self.accounts.items() if data["status"] == "Pending"]
            if not pending_list:
                print("\nℹ️ Không có yêu cầu nào đang chờ duyệt.")
                break

            print("\n--- DANH SÁCH TÀI KHOẢN CHỜ DUYỆT ---")
            for idx, usr in enumerate(pending_list, 1):
                acc = self.accounts[usr]
                print(f"{idx}. Tài khoản: {usr} | Tên: {acc['name']} | Vai trò: {acc['role']} | Mã: {acc['code']}")

            choice = input("\nChọn số để duyệt (nhấn '0' để quay lại): ").strip()
            if choice == "0":
                break

            try:
                sel_idx = int(choice) - 1
                if 0 <= sel_idx < len(pending_list):
                    target_user = pending_list[sel_idx]
                    acc = self.accounts[target_user]
                    
                    confirm = input(f"Phê duyệt tài khoản '{target_user}'? (Y/N): ").strip().upper()
                    if confirm == "Y":
                        acc["status"] = "Approved"
                        self.save_accounts()
                        
                        # Đồng bộ sinh dữ liệu sang file quản lý tương ứng
                        self.gym_manager.create_profile(
                            acc["role"], acc["code"], acc["name"], acc["email"], acc["phone"]
                        )
                        print(f"✅ Đã kích hoạt tài khoản '{target_user}'!")
                else:
                    print("❌ Số thứ tự nằm ngoài danh sách!")
            except:
                print("❌ Vui lòng nhập một số hợp lệ!")

    # ĐỒNG BỘ MÃ KHI HỘI VIÊN ĐƯỢC LÊN VIP
    def sync_upgrade(self, old_code, new_code):
        for usr, data in self.accounts.items():
            if data["code"] == old_code:
                data["code"] = new_code
                data["role"] = "MemberVIP"
                self.save_accounts()
                print(f"🔄 Đã đồng bộ thông tin đăng nhập của '{usr}' sang mã VIP mới: {new_code}")
                return