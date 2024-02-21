from DAO import DAO
from TrangThaiDaoTao import TrangThaiDaoTao

class TrangThaiDaoTaoDAO(DAO):

    def __init__(self):
        super().__init__()

    def xoaTatCaCuaMoHinh(self, id_mo_hinh):
        try:
            query = "DELETE FROM tbltrang_thai_dao_tao WHERE id_mo_hinh = %s";
            self.cursor.execute(query, (id_mo_hinh,))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def themTrangThai(self, tts):
        query = "DELETE FROM tbltrang_thai_dao_tao WHERE id_mo_hinh = %s";
        self.cursor.execute(query, (tts[0].moHinh.id,))
        self.connection.commit()
        for tt in tts:
            try:
                query = "INSERT INTO tbltrang_thai_dao_tao (su_dung, id_mau, id_mo_hinh) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (tt.suDung, tt.mau.id, tt.moHinh.id))
                self.connection.commit()
                print("Đã thêm mới")
            except Exception as e:
                print(e)
                self.connection.rollback()
        return True