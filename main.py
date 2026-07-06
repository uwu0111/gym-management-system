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
                        self.service.add_person(Member(code, name, email, phone, month))
                    elif loai == "2":
                        month = int(input("Số tháng đăng ký VIP: "))
                        self.service.add_person(MemberVIP(code, name, email, phone, month))
                    elif loai == "3":
                        kn = int(input("Số năm kinh nghiệm: "))
                        hours = int(input("Số giờ dạy: "))
                        self.service.add_person(Trainer(code, name, email, phone, kn, hours))
                case "2":
                    code = input("Code: ")
                    name = input("New Name (Bỏ trống nếu giữ nguyên): ")
                    email = input("New Email (Bỏ trống nếu giữ nguyên): ")
                    phone = input("New Phone (Bỏ trống nếu giữ nguyên): ")
                    self.service.update_person(code, name, email, phone)
                case "3":
                    code = input("Code: ")
                    self.service.delete_person(code)
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
                case "2":
                    code = input("Mã hội viên: ")
                    progress = int(input("Tiến độ mới (0-100): "))
                    self.service.update_progress(code, progress)
                case "3":
                    break

    def memberMenu(self):
        while True:
            print("\nMember Menu:")
            print("1. View Progress")
            print("2. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                code = input("Nhập mã hội viên của bạn: ")
                for p in self.service.data_list:
                    if p.code == code and isinstance(p, (Member, MemberVIP)):
                        print(f"Hội viên: {p.name} | Tiến độ tập luyện: {p.progress}%")
            elif choice == "2":
                break

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
                    print("Goodbye!")
                    break

if __name__ == "__main__":
    Main()