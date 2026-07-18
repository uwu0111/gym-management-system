# manager.py
import os
from models import Member, MemberVIP, Trainer

class GymManager:
    def __init__(self):
        # Ép buộc lấy đúng đường dẫn thư mục chứa file manager.py
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_list = []
        self.load_all_files()

    def get_file_path(self, file_name):
        return os.path.join(self.current_dir, file_name)

    # 1. ĐỌC 3 FILE DỮ LIỆU HỒ SƠ
    def load_all_files(self):
        self.data_list = []
        
        # Đọc Member thường
        member_path = self.get_file_path("member_data.txt")
        if os.path.exists(member_path):
            with open(member_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        code, name, email, phone, month = parts
                        self.data_list.append(Member(code, name, email, phone, month))

        # Đọc Member VIP
        vip_path = self.get_file_path("member_vip_data.txt")
        if os.path.exists(vip_path):
            with open(vip_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        code, name, email, phone, month = parts
                        self.data_list.append(MemberVIP(code, name, email, phone, month))

        # Đọc Trainer
        trainer_path = self.get_file_path("trainer_data.txt")
        if os.path.exists(trainer_path):
            with open(trainer_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        code, name, email, phone, exp = parts
                        self.data_list.append(Trainer(code, name, email, phone, exp))

    # 2. GHI CHIA TÁCH VÀO CHÍNH XÁC CÁC FILE
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
                f_trainer.write(f"{p.code}|{p.name}|{p.email}|{p.phone}|{p.experience}\n")

        f_member.close()
        f_vip.close()
        f_trainer.close()

    def find_by_code(self, code):
        for p in self.data_list:
            if p.code == code:
                return p
        return None

    # Tự động tính mã tịnh tiến tăng dần
    def generate_next_code(self, prefix):
        count = 0
        for p in self.data_list:
            if p.code.startswith(prefix):
                count += 1
        return f"{prefix}{count + 1:02d}"

    # Hệ thống tự ghi hồ sơ sau khi duyệt tài khoản
    def create_profile(self, role, code, name, email, phone):
        if role == "Member":
            new_p = Member(code, name, email, phone, month=1)
        elif role == "Trainer":
            new_p = Trainer(code, name, email, phone, experience=1)
        else:
            return

        self.data_list.append(new_p)
        self.save_all_files()
        print(f"✨ Đã tự động lập hồ sơ Gym cho: {name} ({code})")

    # Admin chuyển đổi hạng thẻ của Member -> VIP
    def upgrade_member_to_vip(self, old_code):
        p = self.find_by_code(old_code)
        if p and isinstance(p, Member) and not isinstance(p, MemberVIP):
            new_code = self.generate_next_code("MV")
            vip_p = MemberVIP(new_code, p.name, p.email, p.phone, p.month)
            
            self.data_list.remove(p)
            self.data_list.append(vip_p)
            self.save_all_files() # Tự cập nhật lại file member thường và file VIP
            print(f"👑 Đã nâng cấp lên VIP thành công! Mã mới: {new_code}")
            return new_code
        
        print("❌ Mã Member thường không tồn tại hoặc không hợp lệ!")
        return None

    def list_members(self):
        print("\n--- DANH SÁCH HỒ SƠ TOÀN HỆ THỐNG ---")
        if not self.data_list:
            print("(Trống)")
            return
        for p in self.data_list:
            role = "VIP" if isinstance(p, MemberVIP) else p.__class__.__name__
            print(f"[{role}] Mã: {p.code} | Tên: {p.name} | SĐT: {p.phone}")