from flask import Flask
import requests
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_routes")
def strava_routes_encoding():
    response = requests.get("https://www.strava.com/routes")
    return response.headers["Content-Encoding"]

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
