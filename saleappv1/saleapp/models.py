from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    CASHIER = 2
    NURSE = 3
    DOCTOR = 4
    ADMIN = 5


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class ListUser(BaseModel):
    name = Column(String(50), nullable=False)
    user = relationship("User", backref="ListUser", lazy=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    list_user_id = Column(Integer, ForeignKey(ListUser.id), nullable=False)
    medical_report = relationship("MedicalReport", backref='user', lazy=True)
    receipt = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    price = Column(Float, default=0)

class DiseaseList(BaseModel):
    name = Column(String(50), nullable=False)
    # disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    disease = relationship("Disease", backref = "DiseaseList", lazy = True)

class Disease(BaseModel):
    name = Column(String(50), nullable=False)
    # disease_list = relationship("DiseaseList", backref="Disease", lazy=True)
    medical_report = relationship("MedicalReport", backref='Disease', lazy=True)
    disease_list_id = Column(Integer, ForeignKey(DiseaseList.id), nullable=False)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    unit = Column(String(50))
    description = Column(Text)
    price = Column(Float, default=0)
    # image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    medical_report_detail = relationship('MedicalReportDetail', backref='product', lazy=True)

    def __str__(self):
        return self.name


class MedicalReport(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    # details = relationship('Receipt', backref='receipt', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    medical_report_detail = relationship("MedicalReportDetail", backref='Disease', lazy=True)


class MedicalReportDetail(BaseModel):
    name = Column(String(50), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    medical_report_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)


# class Tag(BaseModel):
#     name = Column(String(50), nullable=False, unique=True)
#
#     def __str__(self):
#         return self.name


# class Receipt(BaseModel):
#     created_date = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
#     details = relationship('ReceiptDetails', backref='receipt', lazy=True)


# class ReceiptDetails(BaseModel):
#     quantity = Column(Integer, default=0)
#     price = Column(Float, default=0)
#     product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=F
if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())

        l1 = ListUser(name="Danh sách Admin")
        l2 = ListUser(name="Danh sách nhân viên")
        l3 = ListUser(name = "Danh sách bệnh nhân")

        u1 = User(name="Tuấn", username="admin", password=password,
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", active = True,
                  user_role=UserRole.ADMIN, list_user_id=1)
        u2 = User(name="Thái", username="admin", password=password,
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", active=True,
                  user_role=UserRole.NURSE, list_user_id=2)
        u3 = User(name="Trang", username="admin", password=password,
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", active=True,
                  user_role=UserRole.DOCTOR, list_user_id=2)
        u4 = User(name="Hùng", username="admin", password=password,
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", active=True,
                  user_role=UserRole.CASHIER, list_user_id=2)
        u5 = User(name="Thành", username="admin", password=password,
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", active=True,
                  user_role=UserRole.USER, list_user_id=3)

        ld1 = DiseaseList(name = "Tim")
        ld2 = DiseaseList(name="Mạch")

        d1 = Disease(name = "Thiếu máu cơ tim", disease_list_id = 1)
        d2 = Disease(name = "Bệnh viêm cơ tim", disease_list_id = 1)
        d3 = Disease(name = "Bệnh mạch vành", disease_list_id = 2)
        d4 = Disease(name = "Bệnh động mạch ngoại biên", disease_list_id = 2)

        c1 = Category(name="Thuốc thể rắn")
        c2 = Category(name="Thuốc thể mềm")
        c3 = Category(name="Thuốc thể lỏng")

        p1 = Product(name = "Thuốc A", unit = "viên", description = "Uống", price = 100000, active = 1, category_id = 1)
        p2 = Product(name="Thuốc B", unit="viên", description="Ngậm", price=30000, active=1, category_id=1)
        p3 = Product(name="Thuốc C", unit="gói", description="Uống", price=150000, active=1, category_id=3)
        p4 = Product(name="Thuốc D", unit="bịch", description="Nhai", price=200000, active=1, category_id=2)
        p5 = Product(name="Thuốc E", unit="bịch", description="Uống", price=500000, active=1, category_id=2)

        db.session.add_all([c1, c2, c3, l1, l2, l3, u1, u2, u3, u4, u5, ld1, ld2, d1, d2, d3, d4, p1, p2, p3, p4, p5])
        db.session.commit()