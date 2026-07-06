import os
from datetime import datetime
from models import Member, MemberVIP, Trainer

class GymService:
    def __init__(self):
        self.data_list = [] 
        # Tự động nạp dữ liệu từ file txt lên khi phần mềm khởi chạy
        self.load_from_txt()

    # 1. Thêm thành viên
    def add_person(self, person_obj):
        for p in self.data_list:
            if p.code == person_obj.code:
                print(f"❌ Mã {person_obj.code} đã tồn tại!")
                return
        self.data_list.append(person_obj)
        print(f"✅ Đã thêm thành công: {person_obj.name}")

    # 2. Sửa thành viên
    def update_person(self, code, new_name, new_email, new_phone):
        found = False
        for p in self.data_list:
            if p.code == code:
                found = True
                if new_name: p.name = new_name
                if new_email: p.email = new_email
                if new_phone: p.phone = new_phone
                print("✅ Cập nhật thông tin thành công!")
        if not found:
            print("❌ Không tìm thấy mã cần cập nhật!")

    # 3. Xóa thành viên
    def delete_person(self, code):
        found = False
        for p in self.data_list:
            if p.code == code:
                self.data_list.remove(p)
                found = True
                print(f"✅ Đã xóa thành công mã {code}.")
                break
        if not found:
            print("❌ Không tìm thấy mã cần xóa!")

    # 5. Xem doanh thu
    def calculate_revenue(self):
        total = 0
        for p in self.data_list:
            if isinstance(p, Member):
                total += p.getSalary()
        return total

    # Trainer - Điểm danh
    def track_attendance(self, code, date_str):
        found = False
        for p in self.data_list:
            if p.code == code and isinstance(p, Member):
                found = True
                if date_str in p.attendance:
                    print(f"ℹ️ Hội viên {code} đã điểm danh ngày này rồi.")
                else:
                    p.attendance.append(date_str)
                    print(f"✅ Điểm danh thành công ngày {date_str}.")
        if not found:
            print("❌ Không tìm thấy hội viên phù hợp!")

    # Trainer - Cập nhật tiến độ
    def update_progress(self, code, progress_value):
        found = False
        for p in self.data_list:
            if p.code == code and isinstance(p, Member):
                found = True
                p.progress = progress_value
                print(f"✅ Cập nhật tiến độ: {progress_value}%")
        if not found:
            print("❌ Không tìm thấy hội viên phù hợp!")

    # ---------- ĐỌC/GHI FILE TXT ----------
    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            f.write("[PEOPLE]\n")
            for person in self.people.values():
                t = person.__class__.__name__
                if isinstance(person, (Member, MemberVIP)):
                    f.write(f"{t}|{person.code}|{person.name}|{person.email}|{person.phone}|{person.month}\n")
                elif isinstance(person, Trainer):
                    f.write(f"{t}|{person.code}|{person.name}|{person.email}|{person.phone}|{person.kinhnghiem}|{person.hours}\n")
            
            f.write("[SCHEDULES]\n")
            for code, info in self.schedules.items():
                f.write(f"{code}|{info['schedule']}|{info['progress']}\n")
                
            f.write("[ATTENDANCE]\n")
            for date_str, codes in self.attendance.items():
                codes_str = ",".join(codes)
                f.write(f"{date_str}|{codes_str}\n")

    def load_data(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                current_section = None
                for line in f:
                    line = line.strip()
                    if not line: continue
                    if line in ["[PEOPLE]", "[SCHEDULES]", "[ATTENDANCE]"]:
                        current_section = line
                        continue
                        
                    parts = line.split("|")
                    if current_section == "[PEOPLE]":
                        p_type = parts[0]
                        if p_type in ["Member", "MemberVIP"]:
                            cls = Member if p_type == "Member" else MemberVIP
                            self.people[parts[1]] = cls(parts[1], parts[2], parts[3], parts[4], int(parts[5]))
                        elif p_type == "Trainer":
                            self.people[parts[1]] = Trainer(parts[1], parts[2], parts[3], parts[4], int(parts[5]), int(parts[6]))
                    elif current_section == "[SCHEDULES]":
                        self.schedules[parts[0]] = {"schedule": parts[1], "progress": int(parts[2])}
                    elif current_section == "[ATTENDANCE]":
                        self.attendance[parts[0]] = parts[1].split(",") if parts[1] else []
        except Exception as e:
            print("Lỗi đọc file text:", e)

    def export_attendance_report_to_txt(self, filename="attendance_report.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{'Ngày':<12} {'Mã Hội Viên':<12} {'Tên Hội Viên':<22}\n")
            f.write("-" * 50 + "\n")
            for date_str, member_list in self.attendance.items():
                for m_code in member_list:
                    person = self.people.get(m_code)
                    name = person.name if person else "Chưa đồng bộ"
                    f.write(f"{date_str:<12} {m_code:<12} {name:<22}\n")
        print(f"📊 Đã xuất dữ liệu lịch sử thành công ra file: {filename}")