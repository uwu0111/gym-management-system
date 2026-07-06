from models import Member, MemberVIP, Trainer
from services import GymService


class Main:
    def __init__(self):
        self.service = GymService()
        self.run()

    # ---------- Các hàm nhập liệu có kiểm tra hợp lệ ----------
    def inputInt(self, message):
        while True:
            value_str = input(message)
            try:
                return int(value_str)
            except ValueError:
                print(f"'{value_str}' không hợp lệ! Vui lòng nhập số nguyên.")

    def inputFloat(self, message):
        while True:
            value_str = input(message)
            try:
                return float(value_str)
            except ValueError:
                print(f"'{value_str}' không hợp lệ! Vui lòng nhập số.")

    # ---------- Nhập thông tin Member / MemberVIP / Trainer ----------
    def inputPerson(self):
        print("\nChọn loại đối tượng cần thêm:")
        print("1. Member")
        print("2. Member VIP")
        print("3. Trainer")
        loai = input("Lựa chọn: ")

        code = input("Code: ")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")

        if loai == "1":
            month = self.inputInt("Số tháng đăng ký: ")
            return Member(code, name, email, phone, month)
        elif loai == "2":
            month = self.inputInt("Số tháng đăng ký: ")
            return MemberVIP(code, name, email, phone, month)
        elif loai == "3":
            kinhnghiem = self.inputInt("Số năm kinh nghiệm: ")
            hours = self.inputInt("Số giờ dạy: ")
            return Trainer(code, name, email, phone, kinhnghiem, hours)
        else:
            print("Lựa chọn không hợp lệ!")
            return None

    def showAllPeople(self):
        if not self.service.people:
            print("Danh sách rỗng!")
            return
        print("\nDanh sách hội viên & huấn luyện viên:")
        for person in self.service.people.values():
            print(person)

    def updatePersonMenu(self):
        code = input("Nhập code cần cập nhật: ")
        if code not in self.service.people:
            print("❌ Không tìm thấy mã này!")
            return

        person = self.service.people[code]
        kwargs = {}

        name = input(f"Tên mới (Enter để giữ '{person.name}'): ")
        if name: kwargs["name"] = name
        email = input(f"Email mới (Enter để giữ '{person.email}'): ")
        if email: kwargs["email"] = email
        phone = input(f"Phone mới (Enter để giữ '{person.phone}'): ")
        if phone: kwargs["phone"] = phone

        if isinstance(person, (Member, MemberVIP)):
            month_str = input("Số tháng mới (Enter để bỏ qua): ")
            if month_str:
                kwargs["month"] = int(month_str)
        elif isinstance(person, Trainer):
            kn_str = input("Kinh nghiệm mới (Enter để bỏ qua): ")
            if kn_str:
                kwargs["kinhnghiem"] = int(kn_str)
            hours_str = input("Số giờ mới (Enter để bỏ qua): ")
            if hours_str:
                kwargs["hours"] = int(hours_str)

        self.service.update_person(code, **kwargs)

    def deletePersonMenu(self):
        code = input("Nhập code cần xóa: ")
        self.service.delete_person(code)

    def statusMenu(self):
        code = input("Nhập code hội viên cần kiểm tra: ")
        print("Trạng thái:", self.service.get_membership_status(code))

    def assignScheduleMenu(self):
        code = input("Nhập code hội viên: ")
        schedule_text = input("Nhập nội dung lịch tập: ")
        self.service.assign_schedule(code, schedule_text)

    def updateProgressMenu(self):
        code = input("Nhập code hội viên: ")
        progress = self.inputInt("Nhập tiến độ (0-100): ")
        self.service.update_progress(code, progress)

    def checkAttendanceMenu(self):
        code = input("Nhập code hội viên: ")
        date_str = input("Nhập ngày (YYYY-MM-DD, Enter để lấy ngày hôm nay): ")
        if date_str:
            self.service.check_attendance(code, date_str)
        else:
            self.service.check_attendance(code)

    def attendanceReportMenu(self):
        report = self.service.get_attendance_report()
        if not report:
            print("Chưa có dữ liệu điểm danh!")
            return
        print("\nBáo cáo điểm danh:")
        for date_str, codes in report.items():
            print(f"{date_str}: {codes}")

    def revenueMenu(self):
        total = self.service.calculate_total_revenue()
        print(f"Tổng doanh thu: {total:,.0f} VNĐ")

    def countStatusMenu(self):
        result = self.service.count_membership_status()
        print(f"Số hội viên Active: {result['Active']}")
        print(f"Số hội viên Expired: {result['Expired']}")

    def attendancePercentMenu(self):
        code = input("Nhập code hội viên: ")
        percent = self.service.calculate_member_attendance_percentage(code)
        print(f"Tỷ lệ đi tập của {code}: {percent}%")

    def topPerformingMenu(self):
        top_n = self.inputInt("Nhập số lượng top cần hiển thị: ")
        top_members = self.service.get_top_performing_members(top_n)
        if not top_members:
            print("Chưa có dữ liệu lịch tập!")
            return
        print("\nTop hội viên tiến độ cao nhất:")
        for item in top_members:
            print(f"{item['code']}  {item['name']}  Progress: {item['progress']}%")

    def exportCsvMenu(self):
        filename = input("Nhập tên file xuất (Enter để dùng mặc định 'attendance_report.csv'): ")
        if filename:
            self.service.export_attendance_report_to_csv(filename)
        else:
            self.service.export_attendance_report_to_csv()

    def run(self):
        while True:
            print("\n===== QUẢN LÝ PHÒNG GYM =====")
            print("1. Thêm hội viên / huấn luyện viên")
            print("2. Hiển thị danh sách")
            print("3. Cập nhật thông tin")
            print("4. Xóa hội viên / huấn luyện viên")
            print("5. Kiểm tra trạng thái hội viên (Active/Expired)")
            print("6. Gán lịch tập cho hội viên")
            print("7. Cập nhật tiến độ tập luyện")
            print("8. Điểm danh")
            print("9. Xem báo cáo điểm danh")
            print("10. Tính tổng doanh thu")
            print("11. Đếm số lượng hội viên Active/Expired")
            print("12. Tính tỷ lệ đi tập của 1 hội viên")
            print("13. Xem top hội viên có tiến độ cao nhất")
            print("14. Xuất báo cáo điểm danh ra CSV")
            print("0. Thoát chương trình")
            option = input("Chọn chức năng: ")

            match option:
                case "1":
                    person = self.inputPerson()
                    if person:
                        self.service.add_person(person)
                case "2":
                    self.showAllPeople()
                case "3":
                    self.updatePersonMenu()
                case "4":
                    self.deletePersonMenu()
                case "5":
                    self.statusMenu()
                case "6":
                    self.assignScheduleMenu()
                case "7":
                    self.updateProgressMenu()
                case "8":
                    self.checkAttendanceMenu()
                case "9":
                    self.attendanceReportMenu()
                case "10":
                    self.revenueMenu()
                case "11":
                    self.countStatusMenu()
                case "12":
                    self.attendancePercentMenu()
                case "13":
                    self.topPerformingMenu()
                case "14":
                    self.exportCsvMenu()
                case "0":
                    print("Thoát chương trình.")
                    break
                case _:
                    print("Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    Main()