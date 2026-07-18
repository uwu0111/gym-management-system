import os
from models import Member, MemberVIP, Trainer

class GymManager:
    def __init__(self):
        self.data_list = []
        self.load_data()

    # Đọc dữ liệu từ file manager_data.txt
    def load_data(self):
        if not os.path.exists("manager_data.txt"):
            return
        with open("manager_data.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 6:
                    continue
                role, code, name, email, phone, extra = parts[:6]
                
                if role == "Member":
                    self.data_list.append(Member(code, name, email, phone, extra))
                elif role == "MemberVIP":
                    self.data_list.append(MemberVIP(code, name, email, phone, extra))
                elif role == "Trainer":
                    self.data_list.append(Trainer(code, name, email, phone, extra))

    # Ghi dữ liệu xuống file manager_data.txt
    def save_data(self):
        with open("manager_data.txt", "w", encoding="utf-8") as f:
            for p in self.data_list:
                role = p.__class__.__name__
                extra = p.month if isinstance(p, Member) else p.experience
                f.write(f"{role}|{p.code}|{p.name}|{p.email}|{p.phone}|{extra}\n")

    def find_by_code(self, code):
        for p in self.data_list:
            if p.code == code:
                return p
        return None

    # Tự động tính mã Code tiếp theo dựa trên dữ liệu hiện tại
    def generate_next_code(self, prefix):
        count = 0
        for p in self.data_list:
            if p.code.startswith(prefix):
                count += 1
        next_num = count + 1
        return f"{prefix}{next_num:02d}"

    # Hệ thống tự tạo hồ sơ khi Admin phê duyệt tài khoản thành công
    def create_profile_from_approved_account(self, role, code, name, email, phone):
        if role == "Member":
            new_p = Member(code, name, email, phone, month=1) # Mặc định đăng ký trước 1 tháng
        elif role == "Trainer":
            new_p = Trainer(code, name, email, phone, experience=1) # Mặc định kinh nghiệm 1 năm
        else:
            return

        self.data_list.append(new_p)
        self.save_data()
        print(f"✨ Đã tự động tạo hồ sơ Gym cho {name} (Mã: {code})")

    # Admin nâng cấp Member thường lên VIP
    def upgrade_member_to_vip(self, old_code):
        p = self.find_by_code(old_code)
        if p and isinstance(p, Member) and not isinstance(p, MemberVIP):
            new_code = self.generate_next_code("MV")
            vip_p = MemberVIP(new_code, p.name, p.email, p.phone, p.month)
            
            self.data_list.remove(p)
            self.data_list.append(vip_p)
            self.save_data()
            print(f"👑 Đã nâng cấp lên VIP! Mã mới: {new_code}")
            return new_code
        
        print("❌ Không tìm thấy Member thường hợp lệ để nâng cấp!")
        return None

    def list_members(self):
        print("\n--- DANH SÁCH HỒ SƠ TRONG HỆ THỐNG ---")
        if not self.data_list:
            print("Danh sách trống!")
            return
        for p in self.data_list:
            role = "VIP" if isinstance(p, MemberVIP) else p.__class__.__name__
            print(f"[{role}] Mã: {p.code} | Tên: {p.name} | Email: {p.email} | SĐT: {p.phone}")