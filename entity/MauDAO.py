from DAO import DAO
from Mau import Mau
from Nhan import Nhan
from NhanDAO import NhanDAO

class MauDAO(DAO):
    def __init__(self):
        super().__init__()

    def getAllMau(self):
        query = "SELECT id, noi_dung_goc, noi_dung_sach, ngay_them, mo_ta, id_nhan FROM tblmau"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        maus = []
        for row in result:
            id_nhan = row[5]
            nhan = NhanDAO().getNhanById(id_nhan)
            mau = Mau(row[0], row[1], row[2], row[3], row[4], nhan)
            maus.append(mau)

        return maus

