from models import Member, MemberVIP, Trainer
from services import GymService

def init_test_data():
    # Khởi tạo dịch vụ (nó sẽ liên kết với file gym_data.json)
    service = GymService()
    
    # Ép dữ liệu test của bạn về đúng cấu trúc Class của nhóm
    gym_database = [
        Member("G01", "Nguyen Hoang Nam", "nam@gmail.com", "09111", 2),
        Member("G02", "Tran Van An", "an@gmail.com", "09112", 12),
        Member("G03", "Le Quang Binh", "binh@gmail.com", "09113", 1),
        Member("G06", "Dang Thu Thao", "thao@gmail.com", "09114", 3),
        Member("G07", "Vu Minh Hieu", "hieu@gmail.com", "09115", 6),
        Member("G08", "Nguyen Thi Mai", "mai@gmail.com", "09116", 1),
        
        MemberVIP("G04", "Pham Minh Duc", "duc.vip@gmail.com", "09221", 5),
        MemberVIP("G05", "Hoang Ngoc Lan", "lan.vip@gmail.com", "09222", 2),
        MemberVIP("G09", "Bui Tien Dung", "dung.vip@gmail.com", "09223", 12),
        MemberVIP("G10", "Nguyen Kieu Oanh", "oanh.vip@gmail.com", "09224", 6),
        MemberVIP("G11", "Tran Quoc Bao", "bao.vip@gmail.com", "09225", 3),
        
        # Mặc định kinh nghiệm 2 năm, số phía sau là số giờ dạy
        Trainer("PT01", "Nguyen Van Huynh", "huynh@gmail.com", "09331", 2, 25),
        Trainer("PT02", "Chu Ba Thong", "thong@gmail.com", "09332", 2, 40),
        Trainer("PT03", "Le Thanh Tung", "tung@gmail.com", "09333", 2, 55),
        Trainer("PT04", "Mai Lan Phuong", "phuong@gmail.com", "09334", 2, 30),
        Trainer("PT05", "Doan Van Hau", "hau@gmail.com", "09335", 2, 20)
    ]
    
    print("--- Bắt đầu nạp dữ liệu thử nghiệm ---")
    for person in gym_database:
        service.add_person(person)
    
    # Giả lập thêm một vài dữ liệu về Điểm danh và Lịch tập để test các hàm tính toán
    print("\n--- Tạo dữ liệu lịch tập & điểm danh mẫu ---")
    service.assign_schedule("G01", "Tập ngực buổi sáng")
    service.update_progress("G01", 80) # Tiến độ 80%
    
    service.assign_schedule("G02", "Giảm cân thần tốc")
    service.update_progress("G02", 95) # Tiến độ 95%
    
    service.assign_schedule("G04", "Tập cơ bắp VIP")
    service.update_progress("G04", 40) # Tiến độ 40%
    
    # Điểm danh thử 2 ngày
    service.check_attendance("G01", "2026-07-05")
    service.check_attendance("G02", "2026-07-05")
    service.check_attendance("G01", "2026-07-06") # G01 đi học cả 2 ngày
    
    print("\n🎉 ĐÃ NẠP DATA TEST THÀNH CÔNG! Bây giờ hãy mở file main.py lên để kiểm tra.")

if __name__ == "__main__":
    init_test_data()