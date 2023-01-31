# from flask import Flask, request

# app = Flask(__name__)

# # Only get method is allowed for this api
# @app.route('/', methods=['GET'])
# def index():
#     print(request.get_json())
#     return dict({'data': 'Hello World!!'})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
# from data import fetch_sales_data
from paginate import paginate
# from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
api = Api(app, prefix='/mentorskool/api/v1')
auth = HTTPBasicAuth()  ## In the API, select the BasicAuthorization

# dotenv_path = Path('.')
# print(dotenv_path)
load_dotenv(find_dotenv())

username = os.environ.get("user") ## username was giving the different result
password = os.environ.get("password")

USER_DATA = {
    username: password
}

@auth.verify_password
def verify(username, password):
    if not (username, password):
        return False
    return USER_DATA.get(username) == password

# Only get method is allowed for this api
class FetchSalesData(Resource):
    @auth.login_required
    def get(self):
        start = request.args.get("start", type=int)
        limit = request.args.get("limit", type=int)

        if not start:
            start = 1
        
        if limit is None:
            limit=30
        elif limit>100:
            limit=100

        if start < 0 or limit < 0:
            return {"message": "Pass the valid values for parameters"}, 400

        final_data = paginate(start, limit)

        if final_data.get("message"):
            return final_data, 400
        else:
            return final_data, 200
        # if limit:
        #     # return jsonify()
        #     data = fetch_sales_data(limit)
        # else:
        #     data = fetch_sales_data()  ## Default limit is 30 and max limit is 100
        # return data


api.add_resource(FetchSalesData, '/sales')

if __name__ == '__main__':
    app.run(debug=True)