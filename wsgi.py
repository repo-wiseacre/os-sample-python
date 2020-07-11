from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    response  = requests.get("http://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=439d4b804bc8187953eb36d2a8c26a02")
    print("Hello world!")
    print(response.json())
    weatherreport = response.json()

    cords = weatherreport["coord"]
    print(cords["lon"],"aaaaaa")

    html_snippet = "<head><title>HTML in 10 Simple Steps or Less</title><meta http-equiv='refresh' content='5' /></head><body><table><tr><td>weather cords</td></tr><tr><td>longitude: </td><td>{var1:}</td></tr><tr><td>lattitude: </td><td>{var2:}</td></tr></table></body>"

    print()

    return html_snippet.format(var1=cords["lon"], var2=cords["lat"])

if __name__ == '__main__':
    app.run()
