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
    # user_id = relationship("User", backref='user', lazy=True)
    name = Column(String(50), nullable=False)
class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    medical_report = relationship("MedicalReport", backref='user', lazy=True)
    list_user_id = Column(Integer, ForeignKey(ListUser.id), nullable=False)

    def __str__(self):
        return self.name



class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


# prod_tag = db.Table('prod_tag',
#                     Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
#                     Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))

class Disease(BaseModel):
    name = Column(String(50), nullable=False)

class DiseaseList(BaseModel):
    name = Column(String(50), nullable=False)
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
class MedicalReport(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    # details = relationship('Receipt', backref='receipt', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)

class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    # image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    medical_report = relationship('MedicalReportDetail', backref='product', lazy=True)
    # medical_report_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)

    # tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
    #                     backref=backref('products', lazy=True))

    def __str__(self):
        return self.name



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
#     receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    price = Column(Float, default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # p1 = Product(name='iPhone 13 Pro Max', description='Apple, 128GB', price=24000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p2 = Product(name='iPhone 14 Pro', description='Apple, 128GB', price=34000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p3 = Product(name='Galaxy Tab S8', description='Samsung, 128GB', price=28000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
        #              category_id=2)
        # p4 = Product(name='S22 Pro', description='Samsung, 128GB', price=28000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p5 = Product(name='Galaxy Tab S8', description='Samsung, 128GB', price=32000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
        #              category_id=2)
        #
        # db.session.add_all([p1, p2, p3, p4, p5])
        # db.session.commit()
        #
        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='thanh', username='admin', password=password,
        #          user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg')
        # db.session.add(u)
        # db.session.commit()
