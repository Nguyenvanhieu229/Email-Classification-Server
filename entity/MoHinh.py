from datetime import datetime
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import random
import string
import xu_ly_mau
import regex as re
from underthesea import word_tokenize
import json


def chuyenDoi(i):
    if i == "_label_học_tập":
        return 1
    elif i == "_label_đơn_hàng":
        return 2
    elif i == "_label_quảng_cáo":
        return 3
    elif i == "_label_cảnh_báo":
        return 4
    elif i == "_label_ngân_hàng":
        return 5
    elif i == "_label_thư_rác":
        return 6

def tao_chuoi_ngau_nhien(do_dai):
    ky_tu = string.ascii_lowercase + string.digits
    chuoi_ngau_nhien = ''.join(random.choice(ky_tu) for _ in range(do_dai))
    return chuoi_ngau_nhien

def tien_xu_ly_mau(sample):
    sample = xu_ly_mau.remove_html(sample)
    sample = xu_ly_mau.convert_unicode(sample)
    sample = word_tokenize(sample, format="text")
    sample = sample.lower()
    sample = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ?!@*,_]', ' ',
                      sample)
    sample = re.sub(r'\s+', ' ', sample).strip()
    return sample


class MoHinh:
    def __init__(self, id = 0, duongDanModel = "", duongDanVector = "", ngayHuanLuyen = "", accuracy = 0, precision = 0, recall = 0, f1_score = 0, state = "Inactive"):
        self.id = id
        self.duongDanModel = duongDanModel
        self.duongDanVector = duongDanVector
        self.ngayHuanLuyen = ngayHuanLuyen
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score
        self.state = state

    def duDoan(self, data):

        try:
            content = data
            print(content)
        except Exception as e:
            print(e)
            return json.dumps({"loi": "Khong dung dinh dang utf-8"})

        model = joblib.load(self.duongDanModel)
        vector = joblib.load(self.duongDanVector)

        content = [tien_xu_ly_mau(data)]
        mau = vector.transform(content)
        res = model.predict(mau)
        result = " ".join([str(i) for i in res])
        print(result)
        return json.dumps({'nhan': result})

    def analys(self, vector, model, test_data):

        test_datas = [i.noiDungSach for i in test_data]
        labels = [i.nhan.id for i in test_data]
        total = len(test_data)

        soluong = [0, 0, 0, 0, 0, 0, 0]
        Y_test = []
        for nhan in labels:
            soluong[nhan] += 1
            Y_test.append(nhan)

        X_test = vector.transform(test_datas)
        Y_predict = model.predict(X_test)

        res = []

        for y in range(1, 7):
            tp = 0
            tn = 0
            fp = 0
            fn = 0

            for i in range(len(Y_test)):
                if Y_test[i] == y and Y_predict[i] == y:
                    tp += 1
                if Y_test[i] != y and Y_predict[i] != y:
                    tn += 1
                if Y_test[i] != y and Y_predict[i] == y:
                    fp += 1
                if Y_test[i] == y and Y_predict[i] != y:
                    fn += 1

            acc = (tp + tn) / (tp + tn + fp + fn)
            if tp == 0:
                pre = 0
                rec = 0
                f1 = 0
            else:
                pre = tp / (tp + fp)
                rec = tp / (tp + fn)
                f1 = 2 * pre * rec / (pre + rec)
            tupl = (acc, pre, rec, f1)
            res.append(tupl)

        last_acc = 0
        last_pre = 0
        last_rec = 0
        last_f1 = 0

        for i in range(6):
            last_acc += res[i][0] * soluong[i + 1]
            last_pre += res[i][1] * soluong[i + 1]
            last_rec += res[i][2] * soluong[i + 1]
            last_f1 += res[i][3] * soluong[i + 1]

        last_acc /= total
        last_pre /= total
        last_rec /= total
        last_f1 /= total

        res = (round(last_acc,4), round(last_pre,4), round(last_rec,4), round(last_f1,4))
        return res

    def train_model(self, train_data, test_data):

        email_datas = [i.noiDungSach for i in train_data]
        Y_train = [i.nhan.id for i in train_data]

        vectorizer = CountVectorizer()
        X_train = vectorizer.fit_transform(email_datas)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, Y_train)

        chi_so = self.analys(vectorizer, model, test_data)
        print(chi_so)
        acc, pre, rec, f1 = chi_so
        chuoi_ngau_nhien = tao_chuoi_ngau_nhien(4)
        model_name = "D:\\HTTM\\model_" + chuoi_ngau_nhien + ".joblib"
        vector_name = "D:\\HTTM\\vector_" + chuoi_ngau_nhien + ".joblib"

        joblib.dump(vectorizer, vector_name)
        joblib.dump(model, model_name)
        return MoHinh(0, model_name, vector_name, datetime.now(), acc, pre, rec, f1, "Inactive")



    def chiaTap(self, maus):
        nhan = [0, [], [], [], [], [], []]

        for i in range(1, 7):
            for sp in maus:
                if i == sp.nhan.id:
                    nhan[i].append(sp)

        train_data = []
        test_data = []
        for i in range(1, 7):
            random.shuffle(nhan[i])
            sl_train = round(len(nhan[i]) * 7 / 10)
            train_data = train_data + nhan[i][:sl_train]
            test_data = test_data + nhan[i][sl_train:]
        print(len(train_data), len(test_data))
        return (train_data, test_data)

    def daoTao(self, maus):
        train_data, test_data = self.chiaTap(maus)
        result = self.train_model(train_data, test_data)
        return result


