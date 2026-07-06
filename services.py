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
    def export_to_csv(self, filename="attendance_report.csv"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("Mã Hội Viên,Tên Hội Viên,Ngày Đi Tập\n")
                for p in self.data_list:
                    if isinstance(p, (Member, MemberVIP)):
                        for date in p.attendance:
                            f.write(f"{p.code},{p.name},{date}\n")
            print(f"📊 Đã xuất file CSV thành công: {filename}")
        except Exception as e:
            print("Lỗi khi ghi file CSV:", e)

    # ------------------ HÀM LOAD FILE TXT GIỐNG BÀI ĐÃ HỌC ------------------
    def load_from_txt(self, filename="gym_data.txt"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line: # Bỏ qua dòng trống
                        continue
                    parts = line.split("|") # Tách chuỗi bằng dấu |
                    loai = parts[0]
                    
                    if loai == "Member":
                        m = Member(parts[1], parts[2], parts[3], parts[4], parts[5])
                        m.progress = int(parts[6])
                        if parts[7]: # Nếu chuỗi lưu danh sách ngày không trống
                            m.attendance = parts[7].split(",") # Tách các ngày bằng dấu phẩy
                        self.data_list.append(m)
                        
                    elif loai == "MemberVIP":
                        mv = MemberVIP(parts[1], parts[2], parts[3], parts[4], parts[5])
                        mv.progress = int(parts[6])
                        if parts[7]:
                            mv.attendance = parts[7].split(",")
                        self.data_list.append(mv)
                        
                    elif loai == "Trainer":
                        t = Trainer(parts[1], parts[2], parts[3], parts[4], parts[5], parts[6])
                        self.data_list.append(t)
        except FileNotFoundError:
            # Nếu chạy phần mềm lần đầu chưa có file gym_data.txt thì bỏ qua không lỗi
            pass

    # ------------------ HÀM LƯU FILE TXT TỰ ĐỘNG BÊN NGOÀI ------------------
    def save_to_txt(self, filename="gym_data.txt"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for p in self.data_list:
                    loai = p.__class__.__name__ # Lấy ra tên Class (Member/MemberVIP/Trainer)
                    if isinstance(p, (Member, MemberVIP)):
                        # Nối danh sách các ngày đi tập thành 1 chuỗi bằng dấu phẩy (VD: "2026-07-07,2026-07-08")
                        dates_str = ",".join(p.attendance) 
                        f.write(f"{loai}|{p.code}|{p.name}|{p.email}|{p.phone}|{p.month}|{p.progress}|{dates_str}\n")
                    elif isinstance(p, Trainer):
                        f.write(f"{loai}|{p.code}|{p.name}|{p.email}|{p.phone}|{p.kinhnghiem}|{p.hours}\n")
        except Exception as e:
            print("Lỗi lưu file txt:", e)