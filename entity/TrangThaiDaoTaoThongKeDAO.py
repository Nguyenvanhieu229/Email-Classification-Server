from DAO import DAO
from TrangThaiDaoTaoThongKe import TrangThaiDaoTaoThongKe

class TrangThaiDaoTaoThongKeDAO(DAO):
    def __init__(self):
        super().__init__()

    def thongKeTheoMoHinh(self, id_mo_hinh):
        da_dao_tao = 0
        query = "SELECT COUNT(*) FROM tbltrang_thai_dao_tao WHERE id_mo_hinh = %s"
        self.cursor.execute(query, (id_mo_hinh,))

        result = self.cursor.fetchone()

        if result:
            da_dao_tao = result[0]

        tong_so_luong = 0
        query = "SELECT COUNT(*) FROM tblmau"
        self.cursor.execute(query)

        result = self.cursor.fetchone()

        if result:
            tong_so_luong = result[0]

        return TrangThaiDaoTaoThongKe(tong_so_luong, tong_so_luong - da_dao_tao)
