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
                        code, name, email, phone, experience = parts  # Thay đổi tại đây
                        self.data_list.append(Trainer(code, name, email, phone, experience))

    def save_all_files(self):
        f_member = open(self.get_file_path("member_data.txt"), "w", encoding="utf-8")
        f_vip = open(self.get_file_path("member_vip_data.txt"), "w", encoding="utf-8")
        f_trainer = open(self.get_file_path("trainer_data.txt"), "w", encoding="utf-8")

        for p in self.data_list:
            if isinstance(p, MemberVIP):
                f_vip.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.month}\n")
            elif isinstance(p, Member):
                f_member.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.month}\n")
            elif isinstance(p, Trainer):
                f_trainer.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.experience}\n")  # Thay đổi tại đây

        f_member.close()
        f_vip.close()
        f_trainer.close()

    def find_by_code(self, code):
        for p in self.data_list:
            if p.code == code:
                return p
        return None

    def get_max_index(self, prefix, register_service_accounts):
        max_idx = 0
        for p in self.data_list:
            if p.code.startswith(prefix):
                try:
                    idx = int(p.code[len(prefix):])
                    if idx > max_idx:
                        max_idx = idx
                except ValueError:
                    pass
                    
        for data in register_service_accounts.values():
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
            new_p = Trainer(code, name, email, phone, experience=1)  # Khởi tạo mặc định 1 năm kinh nghiệm
        else:
            return

        self.data_list.append(new_p)
        self.save_all_files()
        print(f"✨ Hệ thống tự động thiết lập hồ sơ cho: {name} ({code})")

    def upgrade_member_to_vip(self, old_code, register_service_accounts):
        p = self.find_by_code(old_code)
        if p and isinstance(p, Member) and not isinstance(p, MemberVIP):
            max_vip = self.get_max_index("MV", register_service_accounts)
            new_code = f"MV{max_vip + 1:02d}"
            vip_p = MemberVIP(new_code, p.name, p.email, p.phone, p.month)
            
            self.data_list.remove(p)
            self.data_list.append(vip_p)
            self.save_all_files()
            print(f"👑 Nâng cấp VIP thành công! Mã số mới của bạn là: {new_code}")
            return new_code
        
        print("❌ Mã số này không hợp lệ hoặc đã là thành viên VIP!")
        return None

    def list_members(self):
        print("\n--- CƠ SỞ DỮ LIỆU PHÒNG GYM ---")
        if not self.data_list:
            print("(Không có dữ liệu hiển thị)")
            return
        for p in self.data_list:
            role = "VIP" if isinstance(p, MemberVIP) else p.__class__.__name__
            print(f"[{role}] Mã: {p.code} | Tên: {p.name} | SĐT: {p.phone} | Email: {p.email}")