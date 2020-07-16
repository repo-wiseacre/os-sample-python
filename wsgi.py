from flask import Flask
from flask import request
import requests
import json
import pika

application = Flask(__name__)



innerHTML = ""
dict_innerHTML = {}
dict_state = {}

dropdown = "<tr><td><select class='dropdown' name='stateOption' id='idStateOption'>{options:}</select></td><tr>"
optionlist = ""
    
formatteddropdown = ""



@application.route('/state', methods=['GET'])
def covidstate():
    stateOption=request.args.get('stateOption')
    statecode = stateOption
    print(statecode)
    statename = dict_state[statecode]
    print(statename)
    innerHTML = dict_innerHTML[statecode]
    print(innerHTML)
    html_snippet = "<head><title>HTML in 10 Simple Steps or Less</title><meta http-equiv='refresh' content='5' /></head>"
    #html_snippet = ""
    html_snippet+="<head>covid results {heading:}</head><body><table><tr><td>Select state </td></tr>{select:}{innerHTMLS:}</table></body>"

    formattedhtml_snippet = html_snippet.format(heading="statewise", select=formatteddropdown ,innerHTMLS=innerHTML)

    return formattedhtml_snippet



@application.route('/')
def covid():
    print("hello called....")
    response  = requests.get("https://api.covid19india.org/data.json")
    print("Hello world!")
    #print(response.json())
    data = response.json()

    cords = data["statewise"]
    #print(cords)
    print(cords[0]["state"])

    for covid in data['statewise']:
        covidkeys = covid.keys()
        innerHTML=""
        for key in covidkeys:
            innerHTMLobj = "<tr><td>{labels:}: </td><td>{values:}</td></tr>"
            formattedinnerHTMLobj = innerHTMLobj.format(labels=key, values=covid[key])
            #print(formattedinnerHTMLobj)
            innerHTML += formattedinnerHTMLobj
            #print(innerHTML)
        dict_innerHTML[covid["statecode"]] = innerHTML
        dict_state[covid["statecode"]] = covid["state"]
    #print(innerHTML)
    global optionlist
    for keys in dict_state:
        print(dict_state[keys])
        optionlistobj="<option value={key:}>{value:}</option>"
        formattedoptionlistobj = optionlistobj.format(key=keys, value=dict_state[keys])
        optionlist += formattedoptionlistobj
    
    formatteddropdown = dropdown.format(options=optionlist)

    #html_snippet = "<head><title>HTML in 10 Simple Steps or Less</title><meta http-equiv='refresh' content='5' /></head>"
    #html_snippet = ""
    html_snippet="<head>covid results {heading:}</head><head><link rel='stylesheet' href='../dropdown.css'></head><body><form action='/state' method='get'><table><tr><td>Select state </td></tr>{select:}<tr><td>{innerHTMLS:}</td></tr><tr><td><input type='submit' value='submit state'></td><tr></table></form></body>"

    formattedhtml_snippet = html_snippet.format(heading="statewise", select=formatteddropdown ,innerHTMLS=dict_innerHTML["TT"])

    
    #print(html_snippet)

    #html_snippet="<body><table><tr><td>covid results</td></tr>"+innerHTML+"</table></body>"
    
    #!/usr/bin/env python


    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=process.env.CLOUDAMQP_URI))
    channel = connection.channel()

    channel.queue_declare(queue='hello')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
    
    
    return formattedhtml_snippet

if __name__ == '__main__':
    application.run()
