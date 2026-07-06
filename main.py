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

    # ================= ADMIN =================
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

    def addMember(self):
        person = self.inputPerson()
        if person:
            self.service.add_person(person)

    def updateMember(self):
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

    def deleteMember(self):
        code = input("Nhập code cần xóa: ")
        self.service.delete_person(code)

    def listMembers(self):
        if not self.service.people:
            print("Danh sách rỗng!")
            return
        print("\nDanh sách hội viên & huấn luyện viên:")
        for person in self.service.people.values():
            print(person)

    def viewRevenue(self):
        total = self.service.calculate_total_revenue()
        result = self.service.count_membership_status()
        print(f"Tổng doanh thu: {total:,.0f} VNĐ")
        print(f"Số hội viên Active: {result['Active']}  -  Số hội viên Expired: {result['Expired']}")

    def exportCSV(self):
        filename = input("Nhập tên file xuất (Enter để dùng mặc định 'attendance_report.csv'): ")
        if filename:
            self.service.export_attendance_report_to_csv(filename)
        else:
            self.service.export_attendance_report_to_csv()

    def adminMenu(self):
        while True:
            print("\nAdmin Menu:")
            print("1. Add Member")
            print("2. Update Member")
            print("3. Delete Member")
            print("4. List Members")
            print("5. View Revenue")
            print("6. Export Data to CSV")
            print("7. Exit")
            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    self.addMember()
                case "2":
                    self.updateMember()
                case "3":
                    self.deleteMember()
                case "4":
                    self.listMembers()
                case "5":
                    self.viewRevenue()
                case "6":
                    self.exportCSV()
                case "7":
                    break
                case _:
                    print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

    # ================= TRAINER =================
    def trackAttendance(self):
        code = input("Nhập code hội viên: ")
        date_str = input("Nhập ngày (YYYY-MM-DD, Enter để lấy ngày hôm nay): ")
        if date_str:
            self.service.check_attendance(code, date_str)
        else:
            self.service.check_attendance(code)

    def updateMemberProgress(self):
        code = input("Nhập code hội viên: ")
        if code not in self.service.people or isinstance(self.service.people[code], Trainer):
            print("❌ Mã hội viên không hợp lệ!")
            return

        # Nếu hội viên chưa có lịch tập thì gán lịch tập mới trước
        if code not in self.service.schedules:
            schedule_text = input("Hội viên chưa có lịch tập, nhập nội dung lịch tập mới: ")
            self.service.assign_schedule(code, schedule_text)

        progress = self.inputInt("Nhập tiến độ mới (0-100): ")
        self.service.update_progress(code, progress)

    def trainerMenu(self):
        while True:
            print("\nTrainer Menu:")
            print("1. Track Attendance")
            print("2. Update Member Progress")
            print("3. Exit")
            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    self.trackAttendance()
                case "2":
                    self.updateMemberProgress()
                case "3":
                    break
                case _:
                    print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

    # ================= MEMBER =================
    def memberMenu(self):
        code = input("Nhập mã hội viên của bạn: ")
        person = self.service.people.get(code)
        if not person or isinstance(person, Trainer):
            print("❌ Không tìm thấy hội viên với mã này!")
            return

        while True:
            print(f"\nMember Menu ({person.name}):")
            print("1. View My Info")
            print("2. Check-in (Điểm danh)")
            print("3. View My Progress")
            print("4. View My Attendance Percentage")
            print("5. Exit")
            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    print(person)
                    print("Trạng thái:", self.service.get_membership_status(code))
                case "2":
                    self.service.check_attendance(code)
                case "3":
                    info = self.service.schedules.get(code)
                    if info:
                        print(f"Lịch tập: {info['schedule']}  -  Tiến độ: {info['progress']}%")
                    else:
                        print("Bạn chưa được gán lịch tập.")
                case "4":
                    percent = self.service.calculate_member_attendance_percentage(code)
                    print(f"Tỷ lệ đi tập của bạn: {percent}%")
                case "5":
                    break
                case _:
                    print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

    # ================= MAIN MENU =================
    def run(self):
        while True:
            print("\nGym Management System")
            print("1. Login as Admin")
            print("2. Login as Trainer")
            print("3. Login as Member")
            print("4. Exit")
            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    self.adminMenu()
                case "2":
                    self.trainerMenu()
                case "3":
                    self.memberMenu()
                case "4":
                    print("Thoát chương trình.")
                    break
                case _:
                    print("Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    Main()