from flask import Flask, request, jsonify
import requests
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mail import Mail,Message
import re
from time import strftime
from random import randint
import base64, re
import bcrypt
mongo = PyMongo(app)
CORS(app)

@app.route('/Register',methods=['POST'])
def register():
    try:
        data = mongo.db.register
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        emailid = request.json['emailid']
        password = request.json['password']
        mobilenumber = request.json['mobilenumber']
        gender = request.json['gender']
        updated_time = strftime("%Y/%m/%d %H:%M:%S %I%p")
        user_id_list = [i['UserId'] for i in data.find()]
        if len(user_id_list) == 0:
            user_id = 1
        else:
            user_id = int(user_id_list[-1]) + 1
        if data.count_documents({'mobilenumber': mobilenumber}) != 0 or data.count_documents({'EmailId': emailid}) != 0:
            return jsonify({'status': 'failure', 'message': 'User is already registered '})
        else:
            if re.fullmatch('^([a-zA-Z]{1,20})$', firstname):#check for first name properly
                if re.fullmatch('^([a-zA-Z]{1,20})$', lastname):#check for last name properly
                    if re.fullmatch('\w[a-zA-Z0-9@_.]*@[a-z0-9]+[.][a-z]+', emailid):#check for emailid properly
                        if re.match(pattern=r'(^(0/91))?([0-9]{10}$)', string=mobilenumber):#check for mobilenumber properly
                            if re.match(r'[A-Za-z0-9@#$%^&+=]{6,12}', password):#check for password properly
                                output = []
                                data.insert_one({'UserId': int(user_id),'FirstName': firstname,'LastName': lastname,'MobileNumber': mobilenumber,
                                             'EmailId': emailid,'Password': password,'Gender': gender,'UpdatedTime': updated_time})
                                output.append({'user_id':user_id,'firstname':firstname,'lastname':lastname,'mobilenumber':mobilenumber,'emailid':emailid,
                                               'password':password,'gender':gender,'updated_time':updated_time})
                                return jsonify({'status': 'success', 'message': 'User is registered','result':output})
                            else:
                                return jsonify({'status': 'failure', 'message': 'Invalid Password.'})
                        else:
                            return jsonify({'status': 'failure', 'message': 'Invalid Mobile Number'})
                    else:
                        return jsonify({'status': 'failure', 'message': 'Invalid EmailId'})
                else:
                    return jsonify({'status': 'failure', 'message': 'Invalid lastname'})
            else:
                return jsonify({'status': 'failure', 'message': 'Invalid firstname'})
    except Exception as e:
        return jsonify(status="Fail", message=str(e))


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)

# {
#     "firstname": "Abhi",
#     "lastname": "po",
#     "emailid": "abhi@gmail.com",
#     "password": "Dbc@1",
#     "mobilenumber": 9848952855,
#     "gender": "male"
# }
