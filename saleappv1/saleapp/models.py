from turtle import back
from typing import re

from colorama import Fore
from flask_admin.tests.fileadmin.test_fileadmin import Base
from flask_babelex import Babel
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime, null, Date
# from sqlalchemy.ext.mypy.names import COLUMN
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime, date

from sqlalchemy.util import nullcontext


class UserRole(UserEnum):
    USER = 1
    CASHIER = 2
    NURSE = 3
    DOCTOR = 4
    ADMIN = 5


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class DanhMucThuoc(BaseModel):
    tenDanhMuc = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='DanhMucThuoc', lazy=True)

    def __str__(self):
        return self.tenDanhMuc


class Thuoc(BaseModel):
    tenThuoc = Column(String(50), nullable=False)
    giaThuoc = Column(Float, default=0)
    donViThuoc = Column(String(50))
    trangThai = Column(Boolean, default=True)
    moTa = Column(Text)
    danhMucThuoc_id = Column(Integer, ForeignKey(DanhMucThuoc.id), nullable=False)
    chiTietPhieuKham = relationship('ChiTietPhieuKham', backref='Thuoc', lazy=True)

    def __str__(self):
        return self.tenThuoc


class User(BaseModel, UserMixin):
    tenUser = Column(String(50), nullable=False)
    tenDangNhap = Column(String(50), nullable=False, unique=True)
    matKhau = Column(String(50), nullable=False)
    ngaySinh = Column(DateTime, default=datetime.now())
    gioiTinh = Column(Boolean, nullable=True)
    soDienThoai = Column(String(50), nullable=True)
    diaChi = Column(String(100), nullable=True)
    anhDaiDien = Column(String(100), nullable=False)
    trangThai = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    phieuKham = relationship("PhieuKham", backref="User", lazy=True)
    hoaDon = relationship("HoaDon", backref="User", lazy=True)
    chiTietDanhSachKham = relationship("ChiTietDanhSachKham", backref="User", lazy=True)
    # Moi quan he 1 - 1 tren mang no chi xai uselist = false;
    lichSuBenh = relationship("LichSuBenh", backref="User", lazy=True, uselist=False)

    def __str__(self):
        return self.tenUser


class HoaDon(BaseModel):
    tenHoaDon = Column(String(50), nullable=False)
    # ngayKham = Column(DateTime, default=datetime.now())
    ngayKham = Column(Date, default= datetime.now())
    tongTien = Column(Float, nullable=True)
    user_id = Column("User", ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.tenHoaDon


class PhieuKham(BaseModel):
    tenPhieuKham = Column(String(50), nullable=False)
    ngayKham = Column(DateTime, default=datetime.now())
    trieuChung = Column(String(100), nullable=True)
    chuanDoan = Column(String(100), nullable=True)
    user_id = Column("User", ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.tenPhieuKham


class ChiTietPhieuKham(BaseModel):
    soLuongThuoc = Column(Integer, nullable=True)
    Thuoc_id = Column("Thuoc", ForeignKey(Thuoc.id), nullable=False)
    phieuKham_id = Column("PhieuKham", ForeignKey(PhieuKham.id), nullable=False)


class DanhSachKham(BaseModel):
    tenDanhSachKham = Column(String(50), nullable=True)
    ngayKham = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.tenDanhSachKham


class ChiTietDanhSachKham(BaseModel):
    danhSachKham_id = Column("DanhSachKham", ForeignKey(DanhSachKham.id), nullable=False)
    user_id = Column("User", ForeignKey(User.id), nullable=False)

    # def __str__(self):
    #     return self.name


class Benh(BaseModel):
    tenBenh = Column(String(50), nullable=True)
    chiTietLichSuBenh = relationship("ChiTietLichSuBenh", backref="Benh", lazy=True)

    def __str__(self):
        return self.tenBenh


class LichSuBenh(BaseModel):
    tenLichSuBenh = Column(String(50), nullable=True)
    user_id = Column("User", ForeignKey(User.id), nullable=False)
    chiTietLichSuBenh = relationship("ChiTietLichSuBenh", backref="LichSuBenh", lazy=True)

    def __str__(self):
        return self.tenLichSuBenh


class ChiTietLichSuBenh(BaseModel):
    lichSuBenh_id = Column("LichSuBenh", ForeignKey(LichSuBenh.id), nullable=False)
    benh_id = Column("Benh", ForeignKey(Benh.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())

        u1 = User(tenUser="Tr???n ????ng Tu???n", tenDangNhap="admin", matKhau="123456", gioiTinh=True, soDienThoai = "0123", diaChi="TPHCM",
                  anhDaiDien="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg",
                  user_role=UserRole.ADMIN)
        u2 = User(tenUser="Nguy???n Th??? Ph????ng Trang", tenDangNhap="cashier", matKhau="123", gioiTinh=False, soDienThoai = "0124",
                  diaChi="TPHCM",
                  anhDaiDien="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/PTrang1.jpg",
                  user_role=UserRole.CASHIER)
        u3 = User(tenUser="Nguy???n Th??? Mai Trang", tenDangNhap="nurse", matKhau="123", gioiTinh=False, soDienThoai = "0125", diaChi="TPHCM",
                  anhDaiDien="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/MaiTrang-ouitN(1).png",
                  user_role=UserRole.NURSE)
        u4 = User(tenUser="H??? Quang Kh???i", tenDangNhap="doctor", matKhau="123", gioiTinh=True, soDienThoai = "0126", diaChi="TPHCM",
                  anhDaiDien="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Khai_1.jpg",
                  user_role=UserRole.DOCTOR)
        u5 = User(tenUser="L??u Quang Ph????ng", tenDangNhap="user", matKhau="123", gioiTinh=True, soDienThoai = "0127", diaChi="TPHCM",
                  anhDaiDien="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Phuong_2.jpg",
                  user_role=UserRole.USER)

        u6 = User(tenUser="????ng S??? Tu??n", tenDangNhap="user1", matKhau="123", gioiTinh=True, soDienThoai="0128",
                  diaChi="Ph?? Nhu???n",
                  anhDaiDien="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Phuong_2.jpg",
                  user_role=UserRole.USER)

        dmt1 = DanhMucThuoc(tenDanhMuc="Thu???c n?????c")
        dmt2 = DanhMucThuoc(tenDanhMuc="Thu???c vi??n")
        dmt3 = DanhMucThuoc(tenDanhMuc="Thu???c b???t")

        t1 = Thuoc(tenThuoc="Paracetammol", giaThuoc=50000, donViThuoc="Vi??n", moTa="Hi", danhMucThuoc_id=2)
        t2 = Thuoc(tenThuoc="Vitamin C", giaThuoc=10000, donViThuoc="Vi??n", moTa="Hi", danhMucThuoc_id=2)
        t3 = Thuoc(tenThuoc="Y", giaThuoc=5000, donViThuoc="Milli", moTa="Hi", danhMucThuoc_id=1)
        t4 = Thuoc(tenThuoc="Sensacool", giaThuoc=20000, donViThuoc="G??i", moTa="Hi", danhMucThuoc_id=3)
        t5 = Thuoc(tenThuoc="Adrenaline", giaThuoc=30000, donViThuoc="G??i", moTa="Hi", danhMucThuoc_id=3)
        t6 = Thuoc(tenThuoc="Men Vi Sinh", giaThuoc=15000, donViThuoc="G??i", moTa="Hi", danhMucThuoc_id=3)

        pk1 = PhieuKham(tenPhieuKham="Phi???u 1", trieuChung="??au b???ng", chuanDoan="Lo??t d??? d??y", user_id=5)
        pk2 = PhieuKham(tenPhieuKham="Phi???u 2", trieuChung="??au l??ng", chuanDoan="Tho??i h??a ?????t s???ng", user_id=3)
        pk3 = PhieuKham(tenPhieuKham="Phi???u 3", trieuChung="??au tim", chuanDoan="Nh???i m??u c?? tim", user_id=4)

        ctpk1_pk1 = ChiTietPhieuKham(soLuongThuoc=3, Thuoc_id=3, phieuKham_id=1)
        ctpk2_pk1 = ChiTietPhieuKham(soLuongThuoc=2, Thuoc_id=5, phieuKham_id=1)
        ctpk3_pk1 = ChiTietPhieuKham(soLuongThuoc=10, Thuoc_id=6, phieuKham_id=1)
        ctpk1_pk2 = ChiTietPhieuKham(soLuongThuoc=5, Thuoc_id=6, phieuKham_id=2)
        ctpk2_pk2 = ChiTietPhieuKham(soLuongThuoc=4, Thuoc_id=4, phieuKham_id=2)
        ctpk1_pk3 = ChiTietPhieuKham(soLuongThuoc=8, Thuoc_id=2, phieuKham_id=3)
        ctpk2_pk3 = ChiTietPhieuKham(soLuongThuoc=15, Thuoc_id=6, phieuKham_id=3)

        ds1 = DanhSachKham(tenDanhSachKham="Danh s??ch 1")
        ds2 = DanhSachKham(tenDanhSachKham="Danh s??ch 2")

        ctdsk1_ds1 = ChiTietDanhSachKham(danhSachKham_id=1, user_id="3")
        ctdsk2_ds1 = ChiTietDanhSachKham(danhSachKham_id=1, user_id="5")

        ctdsk1_ds2 = ChiTietDanhSachKham(danhSachKham_id=2, user_id="4")

        b1 = Benh(tenBenh="??au l??ng")
        b2 = Benh(tenBenh="??au ?????u")
        b3 = Benh(tenBenh="??au b???ng")
        b4 = Benh(tenBenh="??au r??ng")
        b5 = Benh(tenBenh="??au tim")

        lsb1 = LichSuBenh(tenLichSuBenh="L???ch s??? b???nh 1", user_id=3)
        lsb2 = LichSuBenh(tenLichSuBenh="L???ch s??? b???nh 2", user_id=5)
        lsb3 = LichSuBenh(tenLichSuBenh="L???ch s??? b???nh 3", user_id=4)

        ctlsb1_lsb1 = ChiTietLichSuBenh(lichSuBenh_id=1, benh_id=1)
        ctlsb2_lsb1 = ChiTietLichSuBenh(lichSuBenh_id=1, benh_id=2)
        ctlsb3_lsb1 = ChiTietLichSuBenh(lichSuBenh_id=2, benh_id=3)
        ctlsb1_lsb2 = ChiTietLichSuBenh(lichSuBenh_id=2, benh_id=4)
        ctlsb2_lsb2 = ChiTietLichSuBenh(lichSuBenh_id=2, benh_id=5)
        ctlsb1_lsb3 = ChiTietLichSuBenh(lichSuBenh_id=3, benh_id=5)

        hd1 = HoaDon(tenHoaDon="H??a ????n 1", tongTien=1000000, user_id=3)
        hd2 = HoaDon(tenHoaDon="H??a ????n 2", tongTien=2000000, user_id=5)
        hd3 = HoaDon(tenHoaDon="H??a ????n 3", tongTien=4000000, user_id=4)
        hd4 = HoaDon(tenHoaDon="H??a ????n 4", tongTien=2600000, user_id=2)
        hd5 = HoaDon(tenHoaDon="H??a ????n 5", tongTien=1700000, user_id=5)
        hd6 = HoaDon(tenHoaDon="H??a ????n 6", tongTien=2000000, user_id=1)
        hd7 = HoaDon(tenHoaDon="H??a ????n 7", tongTien=1400000, user_id=3)
        hd8 = HoaDon(tenHoaDon="H??a ????n 8", tongTien=2400000, user_id=1)

        db.session.add_all([u1, u2, u3, u4, u5, u6])
        db.session.add_all([dmt1, dmt2, dmt3])
        db.session.add_all([t1, t2, t3, t4, t5, t6])
        db.session.add_all([b1, b2, b3, b4, b5])
        db.session.add_all([pk1, pk2, pk3])
        db.session.add_all([ctpk1_pk1, ctpk2_pk1, ctpk3_pk1, ctpk1_pk2, ctpk2_pk2, ctpk1_pk3, ctpk2_pk3])
        db.session.add_all([ds1, ds2])
        db.session.add_all([ctdsk1_ds1, ctdsk2_ds1, ctdsk1_ds2])
        db.session.add_all([lsb1, lsb2, lsb3])
        db.session.add_all([ctlsb1_lsb1, ctlsb2_lsb1, ctlsb3_lsb1, ctlsb1_lsb2, ctlsb2_lsb2, ctlsb1_lsb3])
        db.session.add_all([hd1, hd2, hd3, hd4, hd5, hd6, hd7, hd8])

        db.session.commit()
