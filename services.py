import json
import csv
from datetime import datetime
from models import Member, MemberVIP, Trainer
class GymService:
    def __init__(self, data_file="gym_data.json"):
        self.data_file = data_file
        self.people = {}       
        self.schedules = {}    
        self.attendance = {}   
        
        # Tự động nạp dữ liệu cũ lên khi khởi động dịch vụ
        self.load_data()

    # 1. MEMBERSHIP MANAGEMENT (Quản lý Hội viên & Trainer)
    def add_person(self, person_obj):
        if person_obj.code in self.people:
            print(f"❌ Mã {person_obj.code} đã tồn tại!")
            return False
        self.people[person_obj.code] = person_obj
        self.save_data()
        print(f"✅ Đã thêm thành công: {person_obj.name}")
        return True

    def update_person(self, code, **kwargs):
        if code not in self.people:
            print("❌ Không tìm thấy người dùng cần cập nhật!")
            return False
        
        person = self.people[code]
        # Cập nhật các thuộc tính chung
        if "name" in kwargs: person.name = kwargs["name"]
        if "email" in kwargs: person.email = kwargs["email"]
        if "phone" in kwargs: person.phone = kwargs["phone"]
        
        # Cập nhật thuộc tính riêng dựa theo loại Class
        if isinstance(person, (Member, MemberVIP)) and "month" in kwargs:
            person.month = kwargs["month"]
        elif isinstance(person, Trainer):
            if "kinhnghiem" in kwargs: person.kinhnghiem = kwargs["kinhnghiem"]
            if "hours" in kwargs: person.hours = kwargs["hours"]
            
        self.save_data()
        print(f"✅ Đập nhật thông tin mã {code} thành công!")
        return True

    def delete_person(self, code):
        if code in self.people:
            del self.people[code]
            # Xóa các dữ liệu liên quan để tránh rác dữ liệu
            if code in self.schedules: del self.schedules[code]
            self.save_data()
            print(f"✅ Đã xóa thành công mã {code} khỏi hệ thống.")
            return True
        print("❌ Không tìm thấy mã cần xóa!")
        return False

    def get_membership_status(self, member_code):
        """Kiểm tra hội viên còn hạn hay hết hạn (Giả lập: nếu số tháng ký gửi > 0 là Active)"""
        person = self.people.get(member_code)
        if not person or isinstance(person, Trainer):
            return "Unknown"
        return "Active" if person.month > 0 else "Expired"

    # 2. WORKOUT SCHEDULE MANAGEMENT (Quản lý Lịch tập & Tiến độ)
    def assign_schedule(self, member_code, schedule_text):
        if member_code not in self.people or isinstance(self.people[member_code], Trainer):
            print("❌ Mã hội viên không hợp lệ!")
            return False
        self.schedules[member_code] = {
            "schedule": schedule_text,
            "progress": 0  # Tiến độ ban đầu là 0%
        }
        self.save_data()
        print(f"✅ Đã gán lịch tập cho hội viên {member_code}")
        return True

    def update_progress(self, member_code, progress_percentage):
        if member_code not in self.schedules:
            print("❌ Hội viên này chưa được gán lịch tập!")
            return False
        
        # Ép tiến độ trong khoảng từ 0 đến 100
        progress_percentage = max(0, min(100, progress_percentage))
        self.schedules[member_code]["progress"] = progress_percentage
        self.save_data()
        print(f"✅ Đã cập nhật tiến độ tập luyện của {member_code}: {progress_percentage}%")
        return True

    # 3. ATTENDANCE TRACKING (Điểm danh hàng ngày)
    def check_attendance(self, member_code, date_str=None):
        """Điểm danh. Nếu không truyền ngày, hệ thống lấy ngày hôm nay làm chuẩn"""
        if member_code not in self.people or isinstance(self.people[member_code], Trainer):
            print("❌ Mã hội viên không tồn tại để điểm danh!")
            return False
        
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
            
        if date_str not in self.attendance:
            self.attendance[date_str] = []
            
        if member_code in self.attendance[date_str]:
            print(f"ℹ️ Hội viên {member_code} đã điểm danh ngày {date_str} trước đó rồi.")
            return True
            
        self.attendance[date_str].append(member_code)
        self.save_data()
        print(f"✅ Điểm danh thành công cho {member_code} ngày {date_str}")
        return True

    def get_attendance_report(self):
        """Trả về báo cáo chi tiết ngày nào có những ai đi tập"""
        return self.attendance

    # 4. CALCULATE & STATISTICS (Tính toán số liệu)
    def calculate_total_revenue(self):
        """Tổng doanh thu = Tổng số tiền học phí thu từ Member và MemberVIP"""
        total = 0
        for person in self.people.values():
            if isinstance(person, (Member, MemberVIP)):
                total += person.getSalary()  # Học phí thu được
        return total

    def count_membership_status(self):
        """Đếm số lượng hội viên Active và Expired"""
        active_count = 0
        expired_count = 0
        for code, person in self.people.items():
            if isinstance(person, (Member, MemberVIP)):
                if self.get_membership_status(code) == "Active":
                    active_count += 1
                else:
                    expired_count += 1
        return {"Active": active_count, "Expired": expired_count}

    def calculate_member_attendance_percentage(self, member_code):
        """Tính tỷ lệ đi tập = (Số ngày đi tập / Tổng số ngày phòng gym mở cửa) * 100"""
        if not self.attendance:
            return 0.0
        total_days = len(self.attendance)
        attended_days = sum(1 for days in self.attendance.values() if member_code in days)
        return round((attended_days / total_days) * 100, 2)

    def get_top_performing_members(self, top_n=3):
        """Lấy danh sách các hội viên có tiến độ tập luyện (progress) cao nhất"""
        sorted_schedules = sorted(self.schedules.items(), key=lambda x: x[1]["progress"], reverse=True)
        top_members = []
        for code, info in sorted_schedules[:top_n]:
            person = self.people.get(code)
            if person:
                top_members.append({
                    "code": code,
                    "name": person.name,
                    "progress": info["progress"]
                })
        return top_members

    # 5. DATA PERSISTENCE (Lưu/Đọc JSON & Xuất CSV)
    def save_data(self):
        """Chuyển đổi toàn bộ đối tượng thành cấu trúc dữ liệu cơ bản để lưu vào file JSON"""
        serializable_people = {}
        for code, person in self.people.items():
            data = {
                "type": person.__class__.__name__,
                "code": person.code,
                "name": person.name,
                "email": person.email,
                "phone": person.phone
            }
            if isinstance(person, (Member, MemberVIP)):
                data["month"] = person.month
            elif isinstance(person, Trainer):
                data["kinhnghiem"] = person.kinhnghiem
                data["hours"] = person.hours
            serializable_people[code] = data

        master_data = {
            "people": serializable_people,
            "schedules": self.schedules,
            "attendance": self.attendance
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(master_data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """Nạp dữ liệu từ JSON lên và ép lại thành các đối tượng OOP ban đầu"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                master_data = json.load(f)
                
                # Khôi phục danh sách người (Objects)
                people_data = master_data.get("people", {})
                for code, item in people_data.items():
                    p_type = item["type"]
                    if p_type == "Member":
                        self.people[code] = Member(item["code"], item["name"], item["email"], item["phone"], item["month"])
                    elif p_type == "MemberVIP":
                        self.people[code] = MemberVIP(item["code"], item["name"], item["email"], item["phone"], item["month"])
                    elif p_type == "Trainer":
                        self.people[code] = Trainer(item["code"], item["name"], item["email"], item["phone"], item["kinhnghiem"], item["hours"])
                
                # Khôi phục lịch trình và điểm danh
                self.schedules = master_data.get("schedules", {})
                self.attendance = master_data.get("attendance", {})
        except FileNotFoundError:
            # Lần đầu tiên chạy chưa có file thì bỏ qua
            pass

    def export_attendance_report_to_csv(self, filename="attendance_report.csv"):
        """Xuất báo cáo điểm danh ra file CSV công khai để gửi cho Admin/Trainer"""
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Ngày", "Mã Hội Viên", "Tên Hội Viên", "Email"])
            
            for date_str, member_list in self.attendance.items():
                for m_code in member_list:
                    person = self.people.get(m_code)
                    p_name = person.name if person else "Nợ dữ liệu"
                    p_email = person.email if person else "Nợ dữ liệu"
                    writer.writerow([date_str, m_code, p_name, p_email])
        print(f"📊 Đã xuất file báo cáo điểm danh ra: {filename}")