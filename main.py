# Flask API Made by NYT92

# Credit to WeaveAche and Profility for the code
# https://github.com/WeaveAche/hanime-auto-coins-collector
# https://github.com/Profility/hanime-scraper

# api url : https://hani.nsdev.ml (deploy on deta.sh)
# docs : https://aslnk.ml/zwi3ag

# PLEASE DONT ABUSE IT JUST PLEASE JUST FUCKING DONT ABUSing IT...........
# Im not good at this shit so dont call me copy&paste guy 
# also i want to port this to nodejs but the process is kinda hard so i will do it later

import requests
import json
import time
import hanime
from hashlib import sha256
from dateutil import parser
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

base_url = "https://hanime.tv/"

def rate_limit(func):
    def wrapper(*args, **kwargs):
        time.sleep(0.5)
        return func(*args, **kwargs)
    return wrapper

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error=str(e)), 500

@app.route('/')
def index(): 
    return jsonify(
        {
            'status': 'ok', 
            'Warning':'Never use this API in production and abusing there system, this is just for testing purposes and for fun only',
        }
    ), 200

@app.route("/login", methods=["GET"])
def res():
    # Credit to WeaveAche 
    # WeaveAche/hanime-auto-coins-collector 
    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()    

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2","X-Time": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        return received

    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        return info

    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/login/summary", methods=["GET"])
def summary():
    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()    

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2","X-Time": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)

        ret = {}

        ret["session_token"] = received["session_token"]
        ret["name"] = received["user"]["name"]
        ret["coins"] = received["user"]["coins"]
        ret["premium"] = received["user"]["alt_premium_status"]
        ret["email"] = received["user"]["email"]
        ret["avatar"] = received["user"]["avatar_url"]
        ret["id"] = received["user"]["id"]
        ret["slug"] = received["user"]["slug"]
        ret["video_view"] = received["user"]["video_views"]

        return ret

    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        sum = ({
            "data": {
                "id": info["id"],
                "name":info["name"],
                "coin":info["coins"],
                "premium_status":info["premium"],
                "email":info["email"],
                "avatar":info["avatar"],
                "slug":info["slug"],
                "all_video_views":info["video_view"]
                }
            }
        )
        return sum
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/login/coins", methods=["GET"])
def login_coins():
    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")
    
    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()    

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "app2","X-Claim": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {}

        ret["session_token"] = received["session_token"]
        ret["uid"] = received["user"]["id"]
        ret["name"] = received["user"]["name"]
        ret["coins"] = received["user"]["coins"]
        ret["last_clicked"] = received["user"]["last_rewarded_ad_clicked_at"]

        available_keys = list(received["env"]["mobile_apps"].keys())

        if "_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["_build_number"]
        elif "osts_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["osts_build_number"]
        elif "severilous_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["severilous_build_number"]
        else:
            return ("Unable to find the build number for the latest mobile app.")
        return ret

    def getCoins(s:requests.Session,version,uid):
        s.headers.update(getXHeaders())
        curr_time = str(int(time.time()))
        to_hash = f"coins{version}|{uid}|{curr_time}|coins{version}"
        data = {"reward_token": getSHA256(to_hash)+f"|{curr_time}" ,"version":f"{version}"}
        response = s.post(f"{host}/rapi/v4/coins",data=data)

        print(json.loads(response.text))
        return jsonify({"rewarded_amount": json.loads(response.text)['rewarded_amount']}), 200

    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        
        if time.time() - parser.parse(info["last_clicked"]).timestamp() < 3*3600:
            return jsonify({"error":"You have already clicked on an ad less than 3 hrs ago.", "total_coins":info["coins"], "info":"There will be 500 response but when you refresh the page the total coins show up, It is so hard to fix it because i have to waited for 3 hours to test again"})
        getCoins(s,info["version"],info["uid"])
    try:
        info = main()
        return info, 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route('/getInfo', methods=["GET"])
def info():
    id = request.args.get('id')
    return jsonify(
        {
            "info": hanime.info(id), 
            "description": hanime.description(id),
            "tags": hanime.tags(id),
            "thumbnails": hanime.thumbnail(id),
            "video": base_url + "videos/hentai/" + id,
            "downloadURL" : hanime.download(request.args.get('id')),
        }
    ), 200

@app.route('/getVideo', methods=["GET"])
def getVideo():
    url = base_url + "api/v8/video?id="+ request.args.get('id')
    result = requests.get(url)
    result = result.json()
    ret = {
        "url" : base_url + "/videos/hentai/" + request.args.get('id'),
        "downloadURL" : hanime.download(request.args.get('id')),
        "info" : "1080p is currently not supported with our apis due to the hanime api server limit access to the premium contents"
    }
    ret["1080"] = result["videos_manifest"]["servers"][0]["streams"][0]
    ret["720"] = result["videos_manifest"]["servers"][0]["streams"][1]
    ret["480"] = result["videos_manifest"]["servers"][0]["streams"][2]
    ret["360"] = result["videos_manifest"]["servers"][0]["streams"][3]

    return jsonify(ret), 200


@app.route('/getDownloadURL', methods=["GET"])
def getDownloadURL():
    return jsonify({"download_url" : hanime.download(request.args.get('id'))})

@app.route('/getLanding', methods=["GET"])
def getallld():
    request_url = base_url + "api/v8/landing"
    result = requests.get(request_url)
    result = result.json()
    return result
        
if __name__ == "__main__":
    app.run()