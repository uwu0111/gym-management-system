# main.py
from manager import GymManager
from register import RegisterService

class Main:
    def __init__(self):
        self.manager = GymManager()
        self.register = RegisterService(self.manager)
        self.run()

    def admin_menu(self):
        while True:
            print("\n=== TRANG QUẢN TRỊ (ADMIN) ===")
            print("1. Phê duyệt tài khoản đăng ký")
            print("2. Xem toàn bộ hồ sơ phòng Gym")
            print("3. Nâng cấp Member lên VIP")
            print("4. Đăng xuất")
            choice = input("Lựa chọn: ").strip()

            if choice == "1":
                self.register.approve_accounts_menu()
            elif choice == "2":
                self.manager.list_members()
            elif choice == "3":
                old_code = input("Nhập mã Member thường (Ví dụ: M01): ").strip()
                new_code = self.manager.upgrade_member_to_vip(old_code)
                if new_code:
                    self.register.sync_upgrade(old_code, new_code)
            elif choice == "4":
                print("Đã đăng xuất quyền Admin.")
                break

    def member_menu(self, code):
        while True:
            profile = self.manager.find_by_code(code)
            if not profile:
                print("❌ Lỗi dữ liệu liên kết hồ sơ!")
                break

            role_name = "VIP MEMBER" if profile.__class__.__name__ == "MemberVIP" else "MEMBER THƯỜNG"
            print(f"\n=== TRANG CÁ NHÂN ({profile.name} - {profile.code}) ===")
            print(f"Hạng thẻ: {role_name}")
            print("1. Xem chi tiết hồ sơ tập luyện")
            print("2. Đăng xuất")
            choice = input("Lựa chọn: ").strip()

            if choice == "1":
                print(f"\n[HỒ SƠ CÁ NHÂN]")
                print(f"🔹 Mã số: {profile.code}")
                print(f"🔹 Họ tên: {profile.name}")
                print(f"🔹 Liên hệ: {profile.phone} | {profile.email}")
                print(f"🔹 Gói hạn: {profile.month} tháng")
            elif choice == "2":
                break

    def run(self):
        while True:
            print("\n=== HỆ THỐNG PHÒNG GYM CHUYÊN NGHIỆP ===")
            print("1. Đăng nhập")
            print("2. Đăng ký tài khoản (Tự cấp mã số)")
            print("3. Thoát chương trình")
            choice = input("Chọn chức năng: ").strip()

            if choice == "1":
                usr, role, code = self.register.login()
                if role == "Admin":
                    self.admin_menu()
                elif role in ["Member", "MemberVIP", "Trainer"]:
                    self.member_menu(code)
            elif choice == "2":
                self.register.register_account()
            elif choice == "3":
                print("Hệ thống đã đóng. Tạm biệt!")
                break

if __name__ == "__main__":
    Main()