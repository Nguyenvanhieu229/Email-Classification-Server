from flask import Flask, request, jsonify, render_template
import my_email
from datetime import datetime
import os
from server_thong_minh import ServerThongMinh
from dao.model_dao import ModelDAO

session_data = {}

class XuLyAPI:

    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'hieu'
        self.app.add_url_rule('/get-email', 'getemail_api', self.get_email_api, methods=['POST'])
        self.app.add_url_rule('/classification', 'classification_api', self.classification_api, methods=['POST'])
        self.app.add_url_rule('/training', 'training_api', self.training_api, methods=['POST'])
        self.app.add_url_rule('/clean-sample', 'clean_simple_api', self.clean_simple_api, methods=['POST'])
        self.app.add_url_rule('/model', 'model_api', self.model_home_api, methods=['GET'])
        self.app.add_url_rule('/chi-tiet', 'model_ct_api', self.model_api, methods=['GET'])

    def run(self):
        port = int(os.environ.get('PORT', 2209))
        self.app.run(host='0.0.0.0', debug=True, port=port)

    def model_api(self):
        print(request.args.get("id"))
        return render_template("chi_tiet_model.html", tong = 10, chua_train = 5, model = session_data['models'][request.args.get("id")])

    def model_home_api(self):
        models = ModelDAO().getAllModel()
        dic = {}
        for model in models:
            dic[model.id] = {'model' : model}

        session_data['models'] = dic
        return render_template('home.html', models = models)

    def classification_api(self):
        try:
            data = request.get_json()
            result = ServerThongMinh().duDoan(data['noi_dung'])
            return result
        except Exception as e:
            print(e)
            return jsonify({"loi": "Đã có lỗi xảy ra, hãy liên hệ với Hiếu"})

    def training_api(self):
        try:
            # file = request.files['file']
            # train_file = file.read().decode('utf-8')
            data = request.get_json()
            train_file = data['train_sample']
            result = ServerThongMinh().daoTao(train_file)
            return result
        except Exception as e:
            print(e)
            return jsonify({"loi": str(e)})



    def clean_simple_api(self):
        try:
            data = request.get_json()
            result = ServerThongMinh().tien_xu_ly_mau(data['noi_dung'])
            return jsonify({"result": result})
        except Exception as e:
            print(e)
            return jsonify({'result': 'Có vẻ có lỗi xảy ra, hãy liên hệ với Hiếu'})

    def get_email_api(self):
        data = request.get_json()
        emailadd = data['email']
        password = data['password']
        server = data['server']
        ngay = int(data['ngay'])
        thang = int(data['thang'])
        nam = int(data['nam'])
        ngay_tim = datetime(nam, thang, ngay)
        result = my_email.get_email(emailadd, password, server, ngay_tim)
        return result

if __name__ == '__main__':
    app = XuLyAPI();
    app.run()