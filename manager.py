# manager.py
import os
from models import Member, MemberVIP, Trainer

class GymManager:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_list = []
        self.load_all_files()

    def get_file_path(self, file_name):
        return os.path.join(self.current_dir, file_name)

    def load_all_files(self):
        self.data_list = []
        
        member_path = self.get_file_path("member_data.txt")
        if os.path.exists(member_path):
            with open(member_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        code, name, email, phone, month = parts
                        self.data_list.append(Member(code, name, email, phone, month))

        vip_path = self.get_file_path("member_vip_data.txt")
        if os.path.exists(vip_path):
            with open(vip_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        code, name, email, phone, month = parts
                        self.data_list.append(MemberVIP(code, name, email, phone, month))

        trainer_path = self.get_file_path("trainer_data.txt")
        if os.path.exists(trainer_path):
            with open(trainer_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        code, name, email, phone, experience = parts
                        self.data_list.append(Trainer(code, name, email, phone, experience))

    def save_all_files(self):
        with open(self.get_file_path("member_data.txt"), "w", encoding="utf-8") as f_member, \
             open(self.get_file_path("member_vip_data.txt"), "w", encoding="utf-8") as f_vip, \
             open(self.get_file_path("trainer_data.txt"), "w", encoding="utf-8") as f_trainer:

            for p in self.data_list:
                if isinstance(p, MemberVIP):
                    f_vip.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.month}\n")
                elif isinstance(p, Member):
                    f_member.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.month}\n")
                elif isinstance(p, Trainer):
                    f_trainer.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.experience}\n")

    def find_by_code(self, code):
        for p in self.data_list:
            if p.code == code:
                return p
        return None

    def find_by_contact(self, email, phone):
        for p in self.data_list:
            if p.email.lower() == email.lower() or p.phone == phone:
                return p
        return None

    def get_max_index(self, prefix, register_service_accounts):
        max_idx = 0
        
        # SỬA LỖI: Loại trừ mã MV khi tìm max index cho M
        for p in self.data_list:
            if prefix == "M" and p.code.startswith("MV"):
                continue
            if p.code.startswith(prefix):
                try:
                    idx = int(p.code[len(prefix):])
                    if idx > max_idx:
                        max_idx = idx
                except ValueError:
                    pass
                    
        for data in register_service_accounts.values():
            if prefix == "M" and data["code"].startswith("MV"):
                continue
            if data["code"].startswith(prefix):
                try:
                    idx = int(data["code"][len(prefix):])
                    if idx > max_idx:
                        max_idx = idx
                except ValueError:
                    pass
                    
        return max_idx

    def create_profile(self, role, code, name, email, phone):
        if role == "Member":
            new_p = Member(code, name, email, phone, month=1)
        elif role == "Trainer":
            new_p = Trainer(code, name, email, phone, experience=1)
        else:
            return

        self.data_list.append(new_p)
        self.save_all_files()
        print(f"✨ Hệ thống tự động thiết lập hồ sơ cho: {name} ({code})")

    # Danh sách các vai trò hợp lệ và tiền tố mã tương ứng trong hệ thống
    ROLE_PREFIX = {"Member": "M", "MemberVIP": "MV", "Trainer": "T"}

    def convert_role(self, old_code, target_role, register_service_accounts):
        """
        Hàm DUY NHẤT xử lý toàn bộ việc chuyển đổi vai trò (thay cho 6 hàm
        upgrade/downgrade riêng lẻ trước đây): Member <-> MemberVIP <-> Trainer.
        """
        if target_role not in self.ROLE_PREFIX:
            print("❌ Vai trò đích không hợp lệ!")
            return None

        p = self.find_by_code(old_code)
        if not p:
            print("❌ Không tìm thấy mã số này trong hệ thống!")
            return None

        current_role = p.__class__.__name__
        if current_role == target_role:
            print(f"❌ '{p.name}' đã ở vai trò {target_role} rồi, không cần chuyển đổi!")
            return None

        prefix = self.ROLE_PREFIX[target_role]
        max_idx = self.get_max_index(prefix, register_service_accounts)
        new_code = f"{prefix}{max_idx + 1:02d}"

        if target_role in ("Member", "MemberVIP"):
            month = p.month if hasattr(p, "month") else 1
            new_cls = MemberVIP if target_role == "MemberVIP" else Member
            new_p = new_cls(new_code, p.name, p.email, p.phone, month)
        else:  # target_role == "Trainer"
            experience = p.experience if hasattr(p, "experience") else 1
            new_p = Trainer(new_code, p.name, p.email, p.phone, experience)

        self.data_list.remove(p)
        self.data_list.append(new_p)
        self.save_all_files()
        print(f"🔄 Đã chuyển '{p.name}' từ [{current_role}] sang [{target_role}] thành công! Mã số mới: {new_code}")
        return new_code

    def list_members(self):
        print("\n--- CƠ SỞ DỮ LIỆU PHÒNG GYM ---")
        if not self.data_list:
            print("(Không có dữ liệu hiển thị)")
            return
        for p in self.data_list:
            role = "VIP" if isinstance(p, MemberVIP) else p.__class__.__name__
            print(f"[{role}] Mã: {p.code} | Tên: {p.name} | SĐT: {p.phone} | Email: {p.email}")