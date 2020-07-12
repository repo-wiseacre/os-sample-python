from flask import Flask
import requests
import json

application = Flask(__name__)


@application.route('/')
def hello():
    print("hello called....")
    response  = requests.get("https://api.covid19india.org/data.json")
    print("Hello world!")
    print(response.json())
    weatherreport = response.json()

    cords = weatherreport["coord"]
    print(cords["lon"],"aaaaaa")

    html_snippet = "<head><title>HTML in 10 Simple Steps or Less</title><meta http-equiv='refresh' content='5' /></head><body><table><tr><td>weather cords</td></tr><tr><td>longitude: </td><td>{var1:}</td></tr><tr><td>lattitude: </td><td>{var2:}</td></tr></table></body>"

    print()
    
    for covid in data['statewise']:
        covidkeys = covid.keys()
        for key in covidkeys
        html_snippet=html_snippet,covid[key]
    
    return html_snippet.format(var1=cords["lon"], var2=cords["lat"])

if __name__ == '__main__':
    app.run()
