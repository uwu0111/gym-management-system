from abc import ABC, abstractmethod
class Person(ABC):
    def __init__(self, code, name, email, phone):
        self.code = code
        self.name = name
        self.email = email
        self.phone = phone
    def __str__(self):
        return f"{self.code}  {self.name}  {self.email}  {self.phone}  Salary: {self.getSalary()}"
    @abstractmethod
    def getSalary(self):
        pass
class Member(Person):
    def __init__(self, code, name, email, phone, month):
        super().__init__(code, name, email, phone)
        self.month = month
    def getSalary(self):
        return self.month * 60000
    def __str__(self):
        return f"{super().__str__()}  Month: {self.month}"
class MemberVIP(Person):
    def __init__(self, code, name, email, phone, month):
        super().__init__(code, name, email, phone)
        self.month = month
    def getSalary(self):
        return self.month * 60000 * 1.5 
    def __str__(self):
        return f"{super().__str__()}  Month: {self.month}"
class Trainer(Person):
    def __init__(self, code, name, email, phone, kinhnghiem, hours):
        super().__init__(code, name, email, phone)
        self.kinhnghiem = kinhnghiem
        self.hours = hours
    def getSalary(self):
        return self.kinhnghiem * 2000000 + self.hours * 70000
    def __str__(self):
        return f"{super().__str__()}  Kinh nghiệm: {self.kinhnghiem}  Hours: {self.hours}"
