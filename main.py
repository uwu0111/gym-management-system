from models import Member, MemberVIP, Trainer
from services import GymService

class Main:
    def __init__(self):
        # Service khi khởi tạo sẽ tự động gọi hàm load_from_txt() để lấy toàn bộ dữ liệu từ bên ngoài
        self.service = GymService()
        self.run()

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
                    print("\n--- Add Member ---")
                    loai = input("Chọn loại (1: Thường, 2: VIP, 3: Trainer): ")
                    code = input("Code: ")
                    name = input("Name: ")
                    email = input("Email: ")
                    phone = input("Phone: ")
                    if loai == "1":
                        month = int(input("Số tháng đăng ký: "))
                        new_member = Member(code, name, email, phone, month)
                        # services.py cần 2 thuộc tính này để track_attendance / update_progress / export_to_csv hoạt động
                        new_member.progress = 0
                        new_member.attendance = []
                        self.service.add_person(new_member)
                        self.service.save_to_txt()
                    elif loai == "2":
                        month = int(input("Số tháng đăng ký VIP: "))
                        new_member = MemberVIP(code, name, email, phone, month)
                        new_member.progress = 0
                        new_member.attendance = []
                        self.service.add_person(new_member)
                        self.service.save_to_txt()
                    elif loai == "3":
                        kn = int(input("Số năm kinh nghiệm: "))
                        hours = int(input("Số giờ dạy: "))
                        self.service.add_person(Trainer(code, name, email, phone, kn, hours))
                        self.service.save_to_txt()
                case "2":
                    code = input("Code: ")
                    name = input("New Name (Bỏ trống nếu giữ nguyên): ")
                    email = input("New Email (Bỏ trống nếu giữ nguyên): ")
                    phone = input("New Phone (Bỏ trống nếu giữ nguyên): ")
                    self.service.update_person(code, name, email, phone)
                    self.service.save_to_txt()
                case "3":
                    code = input("Code: ")
                    self.service.delete_person(code)
                    self.service.save_to_txt()
                case "4":
                    print("\n--- List Members ---")
                    for p in self.service.data_list:
                        print(p)
                case "5":
                    rev = self.service.calculate_revenue()
                    print(f"Revenue: {rev} VNĐ")
                case "6":
                    self.service.export_to_csv()
                case "7":
                    break

    def trainerMenu(self):
        while True:
            print("\nTrainer Menu:")
            print("1. Track Attendance")
            print("2. Update Member Progress")
            print("3. Exit")
            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    code = input("Mã hội viên: ")
                    date_str = input("Ngày đi tập (YYYY-MM-DD): ")
                    self.service.track_attendance(code, date_str)
                    self.service.save_to_txt()
                case "2":
                    code = input("Mã hội viên: ")
                    progress = int(input("Tiến độ mới (0-100): "))
                    self.service.update_progress(code, progress)
                    self.service.save_to_txt()
                case "3":
                    break

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
                    self.service.save_to_txt()
                    print("Goodbye!")
                    break

if __name__ == "__main__":
    Main()