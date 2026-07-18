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
            print("1. Phê duyệt tài khoản đăng ký mới (Duyệt xong tự tạo hồ sơ)")
            print("2. Xem danh sách hồ sơ Gym")
            print("3. Nâng cấp Member thường lên VIP")
            print("4. Đăng xuất")
            choice = input("Chọn chức năng: ").strip()

            if choice == "1":
                self.register.approve_accounts_menu() # Duyệt tài khoản chờ
            elif choice == "2":
                self.manager.list_members() # Xem hồ sơ
            elif choice == "3":
                old_code = input("Nhập mã Member thường cần nâng cấp (VD: M01): ").strip()
                new_code = self.manager.upgrade_member_to_vip(old_code)
                if new_code:
                    self.register.sync_upgrade(old_code, new_code) # Đồng bộ đổi mã tài khoản
            elif choice == "4":
                break

    def member_menu(self, code):
        while True:
            profile = self.manager.find_by_code(code)
            if not profile:
                print("❌ Không tìm thấy hồ sơ liên kết!")
                break

            role_title = "VIP MEMBER" if profile.__class__.__name__ == "MemberVIP" else "MEMBER"
            print(f"\n=== TRANG HỘI VIÊN ({profile.name} - {profile.code}) ===")
            print(f"Hạng thẻ hiện tại: {role_title}")
            print("1. Xem thông tin chi tiết")
            print("2. Đăng xuất")
            choice = input("Chọn: ").strip()

            if choice == "1":
                print(f"\n📍 Mã số: {profile.code}")
                print(f"📍 Họ tên: {profile.name}")
                print(f"📍 Email: {profile.email} | SĐT: {profile.phone}")
                print(f"📍 Thời gian đăng ký: {profile.month} tháng")
            elif choice == "2":
                break

    def run(self):
        while True:
            print("\n=== HỆ THỐNG PHÒNG GYM ===")
            print("1. Đăng nhập")
            print("2. Đăng ký tài khoản mới (Tự cấp mã chờ duyệt)")
            print("3. Thoát")
            choice = input("Lựa chọn: ").strip()

            if choice == "1":
                usr, role, code = self.register.login()
                if role == "Admin":
                    self.admin_menu()
                elif role in ["Member", "MemberVIP"]:
                    self.member_menu(code)
            elif choice == "2":
                self.register.register_account()
            elif choice == "3":
                print("Tạm biệt!")
                break

if __name__ == "__main__":
    Main()