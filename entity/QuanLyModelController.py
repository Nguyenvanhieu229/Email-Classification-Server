from flask import Flask, request, jsonify, render_template, session
import os
from MoHinhDAO import MoHinhDAO
from TrangThaiDaoTaoDAO import TrangThaiDaoTaoDAO
from TrangThaiDaoTaoThongKeDAO import TrangThaiDaoTaoThongKeDAO
from MauDAO import MauDAO
from MoHinh import MoHinh
from TrangThaiDaoTao import TrangThaiDaoTao
from TrangThaiDaoTaoDAO import TrangThaiDaoTaoDAO
import threading

session_data = {}
training = False

class QuanLyModelController:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'hieu'
        self.app.add_url_rule('/quan-ly-model', 'quanlymodel', self.hienTrangChu, methods=['GET']);
        self.app.add_url_rule('/xoa', 'xoamodel', self.xoaModel, methods=['GET'])
        self.app.add_url_rule('/chi-tiet', 'chitietmodel', self.chiTietModel, methods = ['GET'])
        self.app.add_url_rule('/su-dung', 'sudungmodel', self.suDungModel, methods = ['GET', 'POST'])
        self.app.add_url_rule('/ngung-su-dung', 'ngungsudungmodel', self.ngungSuDungModel, methods=['GET'])
        self.app.add_url_rule('/chon-mau', 'chonmau', self.chonMau, methods = ['GET'])
        self.app.add_url_rule('/dao-tao-lai', 'daotaolai', self.daoTaoLai, methods = ['POST'])
        self.app.add_url_rule('/them-model', 'themmodel', self.themModel, methods = ['GET'])
        self.app.add_url_rule('/dao-tao-moi', 'daotaomoi', self.daoTaoMoi, methods=['POST'])
        self.app.add_url_rule('/classification', 'gannhan', self.ganNhan, methods=['POST'])

    def run(self):
        port = int(os.environ.get('PORT', 2209))
        self.app.run(host='0.0.0.0', debug=True, port=port)

    def themModel(self):
        if 'maus' not in session_data:
            maus = MauDAO().getAllMau()
            session_data['maus'] = maus
        return render_template('chon_mau_moi.html', maus=session_data['maus'])

    def suDungModel(self):
        id = int(request.args.get('id'))
        for model in session_data['models']:
            if model.id == id:
                model.state = "active"
                MoHinhDAO().thayDoiTrangThai(model)
                return render_template('chi_tiet_model.html', thongke=session_data['thongke'], model=model)

    def ngungSuDungModel(self):
        id = int(request.args.get('id'))
        for model in session_data['models']:
            if model.id == id:
                model.state = "Inactive"
                MoHinhDAO().thayDoiTrangThai(model)
                return render_template('chi_tiet_model.html', thongke=session_data['thongke'], model=model)

    def daoTaoLai(self):
        global training
        if training == True:
            pass
        training = True
        id = int(request.form.get('id_model'))
        model = None
        for tmp in session_data['models']:
            if tmp.id == id:
                model = tmp

        ids = [int(i) for i in request.form.getlist('id_maus')]
        maus = []
        for mau in session_data['maus']:
            if mau.id in ids:
                maus.append(mau)

        tmp = MoHinh().daoTao(maus)
        model.duongDanModel = tmp.duongDanModel
        model.duongDanVector = tmp.duongDanVector
        model.accuracy = tmp.accuracy
        model.precision = tmp.precision
        model.recall = tmp.recall
        model.f1_score = tmp.f1_score
        MoHinhDAO().capNhatMoHinh(model)

        tts = []
        for mau in maus:
            tts.append(TrangThaiDaoTao(1, mau, model))
        TrangThaiDaoTaoDAO().themTrangThai(tts)


        thongke = TrangThaiDaoTaoThongKeDAO().thongKeTheoMoHinh(id)
        session_data['thongke'] = thongke
        training = False
        return render_template('chi_tiet_model.html', thongke=thongke, model=model)

    def daoTaoMoi(self):

        ids = [int(i) for i in request.form.getlist('id_maus')]
        maus = []
        for mau in session_data['maus']:
            if mau.id in ids:
                maus.append(mau)

        tmp = MoHinh().daoTao(maus)
        model = MoHinhDAO().themMoHinh(tmp)
        session_data['models'].append(model)

        tts = []
        for mau in maus:
            tts.append(TrangThaiDaoTao(1, mau, model))
        TrangThaiDaoTaoDAO().themTrangThai(tts)

        thongke = TrangThaiDaoTaoThongKeDAO().thongKeTheoMoHinh(model.id)
        session_data['thongke'] = thongke
        return render_template('chi_tiet_model.html', thongke=thongke, model=model)

    def chonMau(self):
        id = int(request.args.get('id'))
        for model in session_data['models']:
            if model.id == id:
                if 'maus' not in session_data:
                    maus = MauDAO().getAllMau()
                    session_data['maus'] = maus
                return render_template('chon_mau.html', maus = session_data['maus'], model = model)

    def hienTrangChu(self):
        models = MoHinhDAO().getAllModel()
        session_data['models'] = models
        return render_template("home.html", models = models)

    def xoaModel(self):
        id = int(request.args.get('id'))
        TrangThaiDaoTaoDAO().xoaTatCaCuaMoHinh(id)
        MoHinhDAO().xoaMoHinhBangID(id)

        models = []
        for model in session_data['models']:
            if model.id != id:
                models.append(model)
        session_data['models'] = models
        return render_template('home.html', models = session_data['models'])

    def chiTietModel(self):
        id = int(request.args.get('id'))
        for model in session_data['models']:
            if model.id == id:
                thongke = TrangThaiDaoTaoThongKeDAO().thongKeTheoMoHinh(id)
                session_data['thongke'] = thongke
                return render_template('chi_tiet_model.html', thongke = thongke, model = model)

    def ganNhan(self):
        try:
            data = request.get_json()
            print(data)
            model = MoHinhDAO().getModelActive()
            result = model.duDoan(data['noiDung'])
            return result
        except Exception as e:
            print(e)
            return jsonify({"loi": "Đã có lỗi xảy ra, hãy liên hệ với Hiếu"})


app = QuanLyModelController()
app.run()