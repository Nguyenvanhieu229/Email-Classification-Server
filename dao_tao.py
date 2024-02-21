import json
import requests
from flask import send_file, Response
import numpy as np
import joblib
import xu_ly_mau
from nltk import re_show
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import random
import string
import base64
import xu_ly_mau
import os


def test_gui_base64():

    with open('default_model.joblib', 'rb') as fin:
        data = fin.read()

    with open('model.txt', 'w', encoding='utf-8') as fout:
        fout.write(base64.b64encode(data).decode('utf-8'))

    with open('default_vector.joblib', 'rb') as fin:
        data = fin.read()

    with open('vector.txt', 'w', encoding='utf-8') as fout:
        fout.write(base64.b64encode(data).decode('utf-8'))

def test_nhan_lai_mo_hinh_base64():

    with open("model.txt", 'r', encoding='utf-8') as fin:
        data = fin.read()
        model = base64.b64decode(data.encode('utf-8'))

    with open("vector.txt", 'r', encoding='utf-8') as fin:
        data = fin.read()
        vector = base64.b64decode(data.encode('utf-8'))

    with open("received_model.joblib", 'wb') as fout:
        fout.write(model)
    with open("received_vector.joblib", 'wb') as fout:
        fout.write(vector)

    model = joblib.load("received_model.joblib")
    vector = joblib.load("received_vector.joblib")

    email = ['Day la mot email gui tu nghuyen van hieu']
    print(model.predict(vector.transform(email)))




#
# def chuyenDoi(i):
#     if i == "_label_học_tập":
#         return 1
#     elif i == "_label_đơn_hàng":
#         return 2
#     elif i == "_label_quảng_cáo":
#         return 3
#     elif i == "_label_cảnh_báo":
#         return 4
#     elif i == "_label_ngân_hàng":
#         return 5
#     elif i == "_label_thư_rác":
#         return 6
#
#
# def tao_chuoi_ngau_nhien(do_dai):
#     ky_tu = string.ascii_lowercase + string.digits
#     chuoi_ngau_nhien = ''.join(random.choice(ky_tu) for _ in range(do_dai))
#     return chuoi_ngau_nhien
#
# def analys(vector, model, test_file):
#
#     test_datas = []
#     labels = []
#
#     try:
#         for email in test_file:
#             try:
#                 label, email_data = email.strip().split(' ', 1)
#                 labels.append(label)
#                 test_datas.append(email_data)
#             except:
#                 pass
#     except:
#         return json.dumps({'result':'noi dung mau khong hop le'})
#
#     soluong = [0,0,0,0,0,0,0]
#     total = len(test_datas)
#     Y_test = []
#     for i in labels:
#         nhan = chuyenDoi(i)
#         soluong[nhan] += 1
#         Y_test.append(nhan)
#
#
#     X_test = vector.transform(test_datas)
#     Y_predict = model.predict(X_test)
#
#     res = []
#
#     for y in range(1, 7):
#         tp = 0
#         tn = 0
#         fp = 0
#         fn = 0
#
#         for i in range(len(Y_test)):
#             if Y_test[i] == y and Y_predict[i] == y:
#                 tp += 1
#             if Y_test[i] != y and Y_predict[i] != y:
#                 tn += 1
#             if Y_test[i] != y and Y_predict[i] == y:
#                 fp += 1
#             if Y_test[i] == y and Y_predict[i] != y:
#                 fn += 1
#
#         acc = (tp + tn) / (tp + tn + fp + fn)
#         if tp == 0:
#             pre = 0
#             rec = 0
#             f1 = 0
#         else:
#             pre = tp / (tp + fp)
#             rec = tp / (tp + fn)
#             f1 = 2 * pre * rec / (pre + rec)
#         tupl = (acc, pre, rec, f1)
#         res.append(tupl)
#
#     last_acc = 0
#     last_pre = 0
#     last_rec = 0
#     last_f1 = 0
#
#     for i in range(6):
#         last_acc += res[i][0] * soluong[i+1]
#         last_pre += res[i][1] * soluong[i+1]
#         last_rec += res[i][2] * soluong[i+1]
#         last_f1 += res[i][3] * soluong[i+1]
#
#     last_acc /= total
#     last_pre /= total
#     last_rec /= total
#     last_f1 /= total
#
#     res = (last_acc, last_pre, last_rec, last_f1)
#     return res
#
#
# def train_model(train_data, test_data):
#
#     email_datas = []
#     labels = []
#     try:
#         for email in train_data:
#             try:
#                 label, email_data = email.strip().split(' ', 1)
#                 labels.append(label)
#                 email_datas.append(email_data)
#             except:
#                 pass
#     except Exception as e:
#         print(e)
#         return json.dumps({'result':'noi dung mau khong hop le'})
#
#     Y_train = [chuyenDoi(i) for i in labels]
#     vectorizer = CountVectorizer()
#     X_train = vectorizer.fit_transform(email_datas)
#
#     model = LogisticRegression(max_iter=1000)
#     model.fit(X_train, Y_train)
#
#     chi_so = analys(vectorizer, model, test_data)
#
#     acc, pre, rec, f1 = chi_so
#     chuoi_ngau_nhien = tao_chuoi_ngau_nhien(10)
#     model_name = "model_" + chuoi_ngau_nhien + ".joblib"
#     vector_name = "vector_" + chuoi_ngau_nhien + ".joblib"
#
#     joblib.dump(vectorizer, vector_name)
#     joblib.dump(model, model_name)
#
#     with open(model_name, 'rb') as fin:
#         model_content = base64.b64encode(fin.read()).decode('utf-8')
#
#     with open(vector_name, 'rb') as fin:
#         vector_content = base64.b64encode(fin.read()).decode('utf-8')
#
#     result = {'accuracy':acc,
#               'precision':pre,
#               'recall':rec,
#               'f1_score':f1,
#               'model': model_content,
#               'vector':vector_content}
#     print("ok")
#     return json.dumps(result)
#
#
# def chiaTap(train_file):
#     # try:
#     #     samples = train_file.readlines()
#     # except:
#     #     return json.dumps({'result':'Loi khong the doc file'})
#     #
#     # try:
#     #     mau = [i.decode('utf-8') for i in samples]
#     # except:
#     #     return json.dumps({'result':'Mau khong o dinh dang utf-8'})
#     mau = train_file.split("\n")
#     print(len(mau))
#     nhan = [0, [], [], [], [], [], []]
#     label = [0, '_label_học_tập', '_label_đơn_hàng', '_label_quảng_cáo', '_label_cảnh_báo', '_label_ngân_hàng', '_label_thư_rác']
#
#     for i in range(1,7):
#         for sp in mau:
#             if sp.startswith(label[i]):
#                 nhan[i].append(sp)
#
#     train_data = []
#     test_data = []
#     for i in range(1,7):
#         random.shuffle(nhan[i])
#         sl_train = round(len(nhan[i]) * 7 / 10)
#         train_data = train_data + nhan[i][:sl_train]
#         test_data = test_data + nhan[i][sl_train:]
#     print(len(train_data), len(test_data))
#     return (train_data, test_data)
#
# def layMoHinhDangSuDung():
#
#     # data = {'yeu_cau' : 'lay_mo_hinh_dang_su_dung'}
#     # json_data = json.dumps(data)
#     url = "http://192.168.105.209/httmmm/public/api/backend/quanlymohinh/file"
#     responce = requests.post(url)
#     print("gui api thanh cong")
#     if responce.status_code == 200:
#         print("thuc hien api thành cong")
#         responce_data = responce.json()
#         # print(responce_data['model'].encode('utf-8')[0:10])
#         # print(responce_data['model'].encode('utf-8')[0:10])
#         model = base64.b64decode(responce_data['model'].encode('utf-8'))
#         vector = base64.b64decode(responce_data['vector'].encode('utf-8'))
#         with open("received_model.joblib", 'wb') as fout:
#             fout.write(model)
#         with open("received_vector.joblib", 'wb') as fout:
#             fout.write(vector)
#
#         return (joblib.load("received_model.joblib"), joblib.load("received_vector.joblib"))
#
#
#
#
# def duDoan(data):
#
#     try:
#         content = data.split("*Phan_de_phan_tach*")
#         #print(content[0:10])
#     except Exception as e:
#         print(e)
#         return json.dumps({"loi": "Khong dung dinh dang utf-8"})
#
#     try:
#         model, vector = layMoHinhDangSuDung()
#     except Exception as e:
#         print(e)
#         model = joblib.load("default_model.joblib")
#         vector = joblib.load("default_vector.joblib")
#
#     mau = vector.transform(content)
#     res = model.predict(mau)
#     result = " ".join([str(i) for i in res])
#     print(result)
#     return json.dumps({'nhan':result})
#
# def test_gui_base64():
#
#     with open('default_model.joblib', 'rb') as fin:
#         data = fin.read()
#
#     with open('model.txt', 'w', encoding='utf-8') as fout:
#         fout.write(base64.b64encode(data).decode('utf-8'))
#
#     with open('default_vector.joblib', 'rb') as fin:
#         data = fin.read()
#
#     with open('vector.txt', 'w', encoding='utf-8') as fout:
#         fout.write(base64.b64encode(data).decode('utf-8'))
#
# def test_nhan_lai_mo_hinh_base64():
#
#     with open("model.txt", 'r', encoding='utf-8') as fin:
#         data = fin.read()
#         model = base64.b64decode(data.encode('utf-8'))
#
#     with open("vector.txt", 'r', encoding='utf-8') as fin:
#         data = fin.read()
#         vector = base64.b64decode(data.encode('utf-8'))
#
#     with open("received_model.joblib", 'wb') as fout:
#         fout.write(model)
#     with open("received_vector.joblib", 'wb') as fout:
#         fout.write(vector)
#
#     model = joblib.load("received_model.joblib")
#     vector = joblib.load("received_vector.joblib")
#
#     email = ['Day la mot email gui tu nghuyen van hieu']
#     print(model.predict(vector.transform(email)))
#
#
