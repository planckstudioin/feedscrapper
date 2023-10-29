import json
import requests
import instagram
import os
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask import Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import send_file

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/clean')
def remove_img():
    directory = "./tmp/img/"
    os.system("find " + directory + " -mtime +7 -delete")
    s = """Deleted"""
    return s

@app.route('/img/<id>')
def feed_img(id):
    p = "./tmp/img/" + id + ".jpg"
    return send_file(p, mimetype='image/jpg')

@app.route('/instagram/user/<username>')
def feed_instagram_user(username):
    s = """Hello Instagram user, {u}"""
    ig = instagram.Instagram()
    fg = ig.gen_user_media_rss(username, 12)
    r = Response(response=fg.rss_str(pretty=True), status=200, mimetype="application/rss+xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r

@app.route('/instagram/hashtag/<hashtag>')
def feed_instagram_hashtag(hashtag):
    s = """Hello Instagram #, {u}"""
    return s.format(u=hashtag)

@app.route('/status')
def status():
    s = '''{"status": "OK"}'''
    return s

class FeedScrapper(Resource):
    def get(self):
        u = request.args.get('query')
        p = request.args.get('page')
        o = request.args.get('orientation')
        premium = request.args.get('premium')
        e = request.args.get('extra')
        t = request.args.get('type')

        url = "https://www.freepik.com/search?format=search&orientation="+o+"&premium=&"+premium+"&page=" + \
            str(p) + "&query=" + u + "&type=" + t + e

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

api.add_resource(FeedScrapper,'/freepik/', methods = ['GET'])

if __name__ == '__main__':
    app.run()