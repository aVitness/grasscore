from flask import Flask, request, session, redirect
import requests
from flask_cors import CORS



discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=910623293751562281&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin&response_type=code&scope=identify%20email%20guilds"


def get_access_token(code):
    payload = {
        "client_id": "910623293751562281",
        "client_secret": " ",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/login",
        "scope": "identify%20email%20guilds"
        }

    access_token = requests.post(url="https://discord.com/api/oauth2/token", data=payload).json()
    return access_token.get("access_token")


def get_user_json(access_token):
    url = "https://discord.com/api/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.get(url=url, headers=headers).json()


app = Flask(__name__)
app.config["SECRET_KEY"] = "test123"
CORS(app)
data = {}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


@app.route("/hello/<id>", methods=["POST"])
def hello(id):
    if id not in data:
        return {"ERROR": "No such id. Authorize first"}
    if request.args.get('token') != data[id]["access_token"]:
        return {"ERROR": "Invalid access token"}
    return data.get(id)


@app.route("/login")
def login():
    global data
    code = request.args.get("code")

    at = get_access_token(code)
    session["token"] = at
    user = get_user_json(at)
    data[user.get("id")] = user
    data[user.get("id")]["access_token"] = at
    return redirect(f"http://localhost:3000/account?id={user.get('id')}&access_token={at}")


if __name__ == "__main__":
    app.run()
