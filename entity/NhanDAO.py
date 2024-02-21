from DAO import DAO
from Nhan import Nhan
class NhanDAO(DAO):
    def __init__(self):
        super().__init__()

    def getNhanById(self, id):
        query = "SELECT id, ten, mo_ta from tblnhan WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()

        if result:
            return Nhan(result[0], result[1], result[2])
