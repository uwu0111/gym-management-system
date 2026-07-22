# register.py
import os
import re

class RegisterService:
    def __init__(self, gym_manager):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.accounts = {}
        self.admin_accounts = {}
        self.gym_manager = gym_manager
        self.load_all_accounts()

    def get_file_path(self, file_name):
        return os.path.join(self.current_dir, file_name)

    def load_all_accounts(self):
        self.admin_accounts = {}
        self.accounts = {}

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

    def is_phone_duplicate(self, phone):
        for adm in self.admin_accounts.values():
            if adm["phone"] == phone:
                return True
        for acc in self.accounts.values():
            if acc["phone"] == phone:
                return True
        for p in self.gym_manager.data_list:
            if p.phone == phone:
                return True
        return False

    def register_account(self):
        print("\n--- ĐĂNG KÝ TÀI KHOẢN MỚI ---")
        
        while True:
            username = input("Nhập Username: ").strip()
            if not username:
                print("❌ Không được để trống Username!")
                continue
            if username in self.accounts or username in self.admin_accounts:
                print("❌ Tên đăng nhập này đã tồn tại! Vui lòng nhập tên khác.")
                continue
            break

        password = input("Nhập Password: ").strip()
        name = input("Nhập Họ và Tên: ").strip()

        # VÒNG LẶP KIỂM TRA EMAIL
        while True:
            email = input("Nhập Email (Bắt buộc định dạng @gmail.com): ").strip()
            
            if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
                print("❌ Email không hợp lệ! Vui lòng nhập đúng định dạng (Ví dụ: abc@gmail.com).")
                continue
            
            is_email_dup = False
            for adm in self.admin_accounts.values():
                if adm["email"].lower() == email.lower():
                    is_email_dup = True
            for acc in self.accounts.values():
                if acc["email"].lower() == email.lower():
                    is_email_dup = True
            for p in self.gym_manager.data_list:
                if p.email.lower() == email.lower():
                    is_email_dup = True
                    
            if is_email_dup:
                print("❌ Email này đã được sử dụng bởi một tài khoản khác! Vui lòng nhập Email khác.")
                continue
            break

        # VÒNG LẶP KIỂM TRA SĐT
        while True:
            phone = input("Nhập Số điện thoại (Gồm 10 số, bắt đầu bằng số 0): ").strip()
            if not re.match(r"^0\d{9}$", phone):
                print("❌ Số điện thoại không hợp lệ! SĐT phải có đúng 10 chữ số và bắt đầu bằng số 0.")
                continue
            
            if self.is_phone_duplicate(phone):
                print("❌ Số điện thoại này đã được sử dụng! Vui lòng nhập số khác.")
                continue
            break

        print("\nBạn muốn đăng ký vai trò nào?")
        print("1. Member (Hội viên thường)")
        print("2. Trainer (Huấn luyện viên)")
        choice = input("Lựa chọn (1 hoặc 2): ").strip()

        if choice == "1":
            role = "Member"
            max_m = self.gym_manager.get_max_index("M", self.accounts)
            code = f"M{max_m + 1:02d}"
        elif choice == "2":
            role = "Trainer"
            max_t = self.gym_manager.get_max_index("T", self.accounts)
            code = f"T{max_t + 1:02d}"
        else:
            print("❌ Lựa chọn sai!")
            return

        self.accounts[username] = {
            "password": password, "role": role, "status": "Pending",
            "code": code, "name": name, "email": email, "phone": phone
        }
        self.save_accounts()
        print(f"🎉 Đăng ký thành công! Mã số định danh của bạn là: {code}. Xin vui lòng đợi Admin phê duyệt.")

    def login(self):
        print("\n--- ĐĂNG NHẬP HỆ THỐNG ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in self.admin_accounts and self.admin_accounts[username]["password"] == password:
            return username, "Admin", "ADMIN"

        if username in self.accounts and self.accounts[username]["password"] == password:
            acc = self.accounts[username]
            if acc["status"] == "Pending":
                print("❌ Tài khoản của bạn đang được xét duyệt, hãy liên hệ lại với Admin!")
                return None, None, None
            elif acc["status"] == "Rejected":
                print("❌ Tài khoản của bạn đã bị từ chối phê duyệt.")
                return None, None, None
            return username, acc["role"], acc["code"]
        
        print("❌ Thông tin đăng nhập không chính xác!")
        return None, None, None

    def approve_accounts_menu(self):
        while True:
            pending_list = [usr for usr, data in self.accounts.items() if data["status"] == "Pending"]
            if not pending_list:
                print("\nℹ️ Không có yêu cầu nào đang chờ phê duyệt.")
                break

            print("\n--- DANH SÁCH TÀI KHOẢN CHỜ DUYỆT ---")
            for idx, usr in enumerate(pending_list, 1):
                acc = self.accounts[usr]
                print(f"{idx}. Tài khoản: {usr} | Tên: {acc['name']} | Vai trò: {acc['role']} | Mã: {acc['code']}")

            choice = input("\nChọn số thứ tự để xử lý (Gõ '0' để quay lại): ").strip()
            if choice == "0":
                break

            try:
                sel_idx = int(choice) - 1
                if 0 <= sel_idx < len(pending_list):
                    target_user = pending_list[sel_idx]
                    acc = self.accounts[target_user]
                    
                    action = input(f"Phê duyệt (Y) / Từ chối (N) tài khoản '{target_user}'? (Y/N): ").strip().upper()
                    if action == "Y":
                        acc["status"] = "Approved"
                        self.save_accounts()
                        self.gym_manager.create_profile(
                            acc["role"], acc["code"], acc["name"], acc["email"], acc["phone"]
                        )
                        print(f"✅ Đã kích hoạt tài khoản '{target_user}' thành công!")
                    elif action == "N":
                        acc["status"] = "Rejected"
                        self.save_accounts()
                        print(f"🚫 Đã từ chối tài khoản '{target_user}'.")
                else:
                    print("❌ Số thứ tự không nằm trong danh sách!")
            except ValueError:
                print("❌ Vui lòng nhập ký tự số hợp lệ!")

    def sync_upgrade(self, old_code, new_code, new_role):
        for data in self.accounts.values():
            if data["code"] == old_code:
                data["code"] = new_code
                data["role"] = new_role
                self.save_accounts()
                print(f"🔄 Hệ thống đã đồng bộ mã đăng nhập mới: {new_code}")
                return