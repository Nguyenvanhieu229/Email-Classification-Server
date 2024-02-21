from DAO import DAO
from MoHinh import MoHinh

class MoHinhDAO(DAO):
    def __init__(self):
        super().__init__()

    def getAllModel(self):
        query = "SELECT id, duong_dan_model, duong_dan_vector, ngay_huan_luyen, accuracy, `precision`, recall, f1_score, state FROM tblmo_hinh "
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        models = []

        for row in result:
            model = MoHinh(row[0], row[1], row[2], row[3], row[4], row[5]
                          ,row[6], row[7], row[8])
            models.append(model)

        return models

    def getModelActive(self):
        query = "SELECT id, duong_dan_model, duong_dan_vector, ngay_huan_luyen, accuracy, `precision`, recall, f1_score, state FROM tblmo_hinh  WHERE state = 'active' LIMIT 1"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        models = []
        for row in result:
            model = MoHinh(row[0], row[1], row[2], row[3], row[4], row[5]
                           , row[6], row[7], row[8])
            return model
            # models.append(model)

        # return models


    def capNhatMoHinh(self, model):
        try:
            query = "UPDATE tblmo_hinh SET duong_dan_model = %s, duong_dan_vector = %s, ngay_huan_luyen = %s, accuracy = %s, `precision` = %s, recall = %s, f1_score = %s, state= %s WHERE id = %s";
            self.cursor.execute(query, (model.duongDanModel, model.duongDanVector, model.ngayHuanLuyen, model.accuracy, model.precision, model.recall, model.f1_score, model.state,model.id))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def themMoHinh(self, model):
        query = "INSERT INTO tblmo_hinh (duong_dan_model, duong_dan_vector, ngay_huan_luyen, accuracy, `precision`, recall, f1_score, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (model.duongDanModel, model.duongDanVector, model.ngayHuanLuyen, model.accuracy, model.precision, model.recall, model.f1_score, model.state))
        model.id = self.cursor.lastrowid
        self.connection.commit()
        return model

    def xoaMoHinhBangID(self, id):
        try:
            query = "DELETE FROM tblmo_hinh WHERE id = %s";
            self.cursor.execute(query, (id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def thayDoiTrangThai(self, model):
        try:
            query = " UPDATE tblmo_hinh SET state= %s WHERE id = %s";
            self.cursor.execute(query, (model.state,model.id))
            self.connection.commit()
            if model.state == "active":
                query = 'UPDATE tblmo_hinh SET state= "inactive" WHERE id != %s';
                self.cursor.execute(query, (model.id,))
                self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False
