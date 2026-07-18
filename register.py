import os

class RegisterService:
    def __init__(self, gym_manager):
        self.accounts = {}      # Lưu tài khoản Member, Trainer
        self.admin_accounts = {} # Lưu tài khoản Admin riêng biệt
        self.gym_manager = gym_manager
        self.load_all_accounts()

    # ĐỌC SONG SONG CẢ FILE ADMIN VÀ FILE HỘI VIÊN
    def load_all_accounts(self):
        # 1. Đọc file admin_data.txt
        if os.path.exists("admin_data.txt"):
            with open("admin_data.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        usr, pwd, name, email, phone = parts
                        self.admin_accounts[usr] = {
                            "password": pwd, "role": "Admin", "code": "ADMIN",
                            "name": name, "email": email, "phone": phone
                        }
        else:
            # Nếu chưa có file admin, tạo sẵn một tài khoản mặc định
            self.admin_accounts["admin"] = {
                "password": "admin", "role": "Admin", "code": "ADMIN",
                "name": "Admin", "email": "admin@gym.com", "phone": "000"
            }
            with open("admin_data.txt", "w", encoding="utf-8") as f:
                f.write("admin|admin|Admin Tối Cao|admin@gym.com|000\n")

        # 2. Đọc file register_data.txt (Member và Trainer)
        self.accounts = {}
        if os.path.exists("register_data.txt"):
            with open("register_data.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 8:
                        usr, pwd, role, status, code, name, email, phone = parts
                        self.accounts[usr] = {
                            "password": pwd, "role": role, "status": status, 
                            "code": code, "name": name, "email": email, "phone": phone
                        }

    def save_accounts(self):
        with open("register_data.txt", "w", encoding="utf-8") as f:
            for usr, data in self.accounts.items():
                f.write(f"{usr}|{data['password']}|{data['role']}|{data['status']}|{data['code']}|{data['name']}|{data['email']}|{data['phone']}\n")

    # ĐĂNG KÝ (Chỉ cho đăng ký Member thường hoặc Trainer)
    def register_account(self):
        print("\n--- ĐĂNG KÝ TÀI KHOẢN MỚI ---")
        username = input("Nhập Username: ").strip()
        
        # Kiểm tra trùng tên ở cả danh sách admin lẫn hội viên
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
        print(f"🎉 Đăng ký thành công! Mã số cấp tạm thời: {code}. Đang chờ Admin phê duyệt.")

    # ĐĂNG NHẬP (Kiểm tra file Admin trước, nếu không có thì kiểm tra file Register)
    def login(self):
        print("\n--- ĐĂNG NHẬP HỆ THỐNG ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Kiểm tra xem có phải Admin không
        if username in self.admin_accounts and self.admin_accounts[username]["password"] == password:
            print(f"🎉 Đăng nhập thành công quyền ADMIN!")
            return username, "Admin", "ADMIN"

        # Kiểm tra tài khoản người dùng thường
        if username in self.accounts and self.accounts[username]["password"] == password:
            acc = self.accounts[username]
            if acc["status"] == "Pending":
                print("❌ Tài khoản đang chờ duyệt, vui lòng quay lại sau!")
                return None, None, None
            print(f"🎉 Đăng nhập thành công! Chào mừng {acc['name']}.")
            return username, acc["role"], acc["code"]
        
        print("❌ Sai tài khoản hoặc mật khẩu!")
        return None, None, None

    # ADMIN PHÊ DUYỆT TÀI KHOẢN
    def approve_accounts_menu(self):
        while True:
            pending_list = [usr for usr, data in self.accounts.items() if data["status"] == "Pending"]
            if not pending_list:
                print("\nℹ️ Không có tài khoản nào đang chờ phê duyệt.")
                break

            print("\n--- DANH SÁCH CHỜ PHÊ DUYỆT ---")
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
                        
                        # Gọi quản lý Gym ghi thông tin vào file chức năng tương ứng
                        self.gym_manager.create_profile(
                            acc["role"], acc["code"], acc["name"], acc["email"], acc["phone"]
                        )
                        print(f"✅ Đã duyệt tài khoản '{target_user}' thành công!")
            except:
                print("❌ Lựa chọn không hợp lệ!")

    # ĐỒNG BỘ MÃ MỚI KHI NÂNG CẤP VIP
    def sync_upgrade(self, old_code, new_code):
        for usr, data in self.accounts.items():
            if data["code"] == old_code:
                data["code"] = new_code
                data["role"] = "MemberVIP"
                self.save_accounts()
                print(f"🔄 Đã đồng bộ tài khoản '{usr}' sang mã VIP mới: {new_code}")
                return