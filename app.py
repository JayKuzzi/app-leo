from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
import requests
import requests_cache

requests_cache.install_cache('weather_api_cache', backend='sqlite', expire_after=36000)

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)

weather_url_template = 'https://api.breezometer.com/weather/v1/current-conditions?lat={lat}&lon={lon}&key={key}'
MY_API_KEY = "b44b2edecf4748de95c8180a73960c41"


# Welcome Page
@app.route('/')
def hello_world():
    return 'Hello,this is index!'


# Quire all users
@app.route('/user', methods=['GET'])
def user():
    rows = session.execute("""Select * From app.user""")
    for user in rows:
        return ('<h2>This is all users : {} </h2>'.format(rows.current_rows))
    return ('<h1>That data does not exist!</h1>')


# Quire user by name
@app.route('/user/<name>', methods=['GET'])
def profile(name):
    rows = session.execute("""Select * From app.user where name = '{}' ALLOW FILTERING""".format(name))
    for user in rows:
        return ('<h2>This is info : {} by name: {}</h2>'.format(rows.current_rows, name))
    return ('<h1>That data does not exist!</h1>')


# Quire weather
@app.route('/weather', methods=['GET'])
def weatherchart():
    my_latitude = '51'
    my_longitude = '-0.0395857'
    weather_url = weather_url_template.format(lat=my_latitude, lon=my_longitude, key=MY_API_KEY)
    resp = requests.get(weather_url)
    print (resp.json())
    if resp.ok:
        return ('{}').format(resp.json())
    else:
        return ('<h1>Fail!</h1>')
    return ("Done!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
