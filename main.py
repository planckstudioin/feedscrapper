import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class Scrapper(Resource):
    def get(self):

        u = request.args.get('query')
        p = request.args.get('page')
        o = request.args.get('orientation')
        premium = request.args.get('premium')
        e = request.args.get('extra')

        url = "https://www.freepik.com/search?format=search&orientation="+o+"&premium=&"+premium+"&page=" + \
            str(p) + "&query=" + u + e

        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }

        response = requests.request("GET", url, headers=headers)
        data = BeautifulSoup(response.text, 'html.parser')
        # find all with the image tag
        images = data.find_all('img', src=True, class_="lzy")
        print(images)
        image_src = [x['data-src'] for x in images]
        img = []

        for i in image_src:
            iu = i.split(".jpg")
            img.append(iu[0] + ".jpg")

        res = {
            "img": img,
            "keywords": u
        }

        text = json.dumps(res, sort_keys=True, indent=4)
        return res

api.add_resource(Scrapper,'/freepik/', methods = ['GET'])

if __name__ == '__main__':
    app.run()