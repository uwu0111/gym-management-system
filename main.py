# main.py
from manager import GymManager
from register import RegisterService

class Main:
    def __init__(self):
        self.manager = GymManager()
        self.register = RegisterService(self.manager)
        self.run()

    def convert_role_menu(self):
        """Chức năng gộp: chuyển đổi vai trò Member / MemberVIP / Trainer theo bất kỳ chiều nào."""
        old_code = input("\nNhập mã cần chuyển đổi vai trò (Ví dụ: M01, MV01, T01): ").strip()
        profile = self.manager.find_by_code(old_code)
        if not profile:
            print("❌ Không tìm thấy mã số này trong hệ thống!")
            return

        current_role = profile.__class__.__name__
        role_labels = {"Member": "Member thường", "MemberVIP": "VIP", "Trainer": "Trainer"}
        all_roles = ["Member", "MemberVIP", "Trainer"]
        options = [r for r in all_roles if r != current_role]

        print(f"\nVai trò hiện tại của '{profile.name}' ({old_code}): {role_labels[current_role]}")
        print("Chọn vai trò muốn chuyển sang:")
        for idx, r in enumerate(options, 1):
            print(f"{idx}. {role_labels[r]}")
        print("0. Hủy / Quay lại")

        sub_choice = input("Lựa chọn: ").strip()
        if sub_choice == "0":
            return

        try:
            target_role = options[int(sub_choice) - 1]
        except (ValueError, IndexError):
            print("❌ Lựa chọn không hợp lệ!")
            return

        new_code = self.manager.convert_role(old_code, target_role, self.register.accounts)
        if new_code:
            self.register.sync_upgrade(old_code, new_code, target_role)

    def admin_menu(self):
        while True:
            print("\n=== TRANG QUẢN TRỊ (ADMIN) ===")
            print("1. Phê duyệt tài khoản đăng ký")
            print("2. Xem toàn bộ hồ sơ phòng Gym")
            print("3. Chuyển đổi vai trò (Member / VIP / Trainer)")
            print("4. Đăng xuất")
            choice = input("Lựa chọn: ").strip()

            if choice == "1":
                self.register.approve_accounts_menu()
            elif choice == "2":
                self.manager.list_members()
            elif choice == "3":
                self.convert_role_menu()
            elif choice == "4":
                print("Đã đăng xuất tài khoản Admin.")
                break

    def member_menu(self, code):
        while True:
            profile = self.manager.find_by_code(code)
            if not profile:
                print("❌ Lỗi dữ liệu liên kết hồ sơ phòng tập!")
                break

            role_name = "VIP MEMBER" if profile.__class__.__name__ == "MemberVIP" else "MEMBER THƯỜNG"
            if profile.__class__.__name__ == "Trainer":
                role_name = "TRAINER (HLV)"

            print(f"\n=== TRANG CÁ NHÂN ({profile.name} - {profile.code}) ===")
            print(f"Hạng thành viên: {role_name}")
            print("1. Xem chi tiết hồ sơ tập luyện")
            print("2. Đăng xuất")
            choice = input("Lựa chọn: ").strip()

            if choice == "1":
                print(f"\n[THÔNG TIN HỒ SƠ]")
                print(f"🔹 Mã định danh: {profile.code}")
                print(f"🔹 Họ và tên: {profile.name}")
                print(f"🔹 Số điện thoại: {profile.phone}")
                print(f"🔹 Email liên hệ: {profile.email}")
                if hasattr(profile, "month"):
                    print(f"🔹 Gói đăng ký: {profile.month} tháng")
                elif hasattr(profile, "experience"):
                    print(f"🔹 Kinh nghiệm: {profile.experience} năm")
            elif choice == "2":
                break

    def run(self):
        while True:
            print("\n=== HỆ THỐNG PHÒNG GYM CHUYÊN NGHIỆP ===")
            print("1. Đăng nhập hệ thống")
            print("2. Đăng ký tài khoản mới")
            print("3. Thoát chương trình")
            choice = input("Chọn chức năng: ").strip()

            if choice == "1":
                usr, role, code = self.register.login()
                if role == "Admin":
                    self.admin_menu()
                elif role in ["Member", "MemberVIP", "Trainer"]:
                    profile = self.manager.find_by_code(code)

                    if not profile:
                        # Mã trong tài khoản bị lệch so với hồ sơ Gym (thường do lỗi
                        # xảy ra giữa chừng khi chuyển đổi vai trò trước đó).
                        # Thử tự khôi phục liên kết bằng email/SĐT đã đăng ký.
                        acc = self.register.accounts.get(usr)
                        if acc:
                            profile = self.manager.find_by_contact(acc["email"], acc["phone"])
                            if profile:
                                old_code = code
                                code = profile.code
                                acc["code"] = code
                                acc["role"] = profile.__class__.__name__
                                self.register.save_accounts()
                                print(f"🔧 Đã tự động khôi phục liên kết tài khoản (mã cũ: {old_code} → mã đúng: {code}).")

                    if profile:
                        self.member_menu(code)
                    else:
                        print("❌ Không tìm thấy hồ sơ phòng tập liên kết với tài khoản này. Vui lòng liên hệ Admin để kiểm tra lại.")
            elif choice == "2":
                self.register.register_account()
            elif choice == "3":
                print("Chương trình kết thúc an toàn. Tạm biệt!")
                break

if __name__ == "__main__":
    Main()