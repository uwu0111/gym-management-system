# models.py

class Person:
    def __init__(self, code, name, email, phone):
        self.code = code
        self.name = name
        self.email = email
        self.phone = phone

class Member(Person):
    def __init__(self, code, name, email, phone, month=1):
        super().__init__(code, name, email, phone)
        self.month = int(month)

class MemberVIP(Member):
    pass

class Trainer(Person):
    def __init__(self, code, name, email, phone, experience=1):
        super().__init__(code, name, email, phone)
        self.experience = int(experience)