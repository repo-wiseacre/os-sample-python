#!/usr/bin/env python
import os
from flask import Flask, session
from flask import request
import requests
import json
import subprocess
from termcolor import colored

from punisher import publish

application = Flask(__name__)
application.secret_key = os.urandom(25)

#data={}
#innerHTML = ""
dict_innerHTML = {}
dict_state = {}

dropdown = "<tr><td><select class='dropdown' name='stateOption' id='idStateOption'>{options:}</select></td><tr>"
optionlist = ""
    
formatteddropdown = ""


@application.route('/rawpost', methods=['POST'])
def covidDataUpdate():
    print(colored('inside covidDataUpdate', 'green', 'on_red'))
    print(type(request))
    print(type(request.form))
    print(type(request.form['raw']))
    print(request.form['raw'])
    raw=request.form['raw']
    print(colored(request, 'red', 'on_white')) # should display 'bar'

    print("hello called....")
    #response  = requests.get("https://api.covid19india.org/data.json")
    print("Hello world!")
    #print(response.json())
    #data = raw
    
    data = json.loads(raw)
    print("type of data",type(data))
    session['data'] = raw
    print(raw)
    
    return json.dumps({'errors': "errors"})

@application.route('/raw', methods=['GET'])
def getcovidDataUpdate():
    print(colored('inside get>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>','green', 'on_grey'))
    print(type(request))
    print(type(request.args.get('raw')))
    #print(type(request.form[0]))
    print(request.args.get('raw'))
    print(json.dumps(request.args.get('raw')))
    raw=json.dumps(request.args.get('raw'))
    print(colored(raw, 'red', 'on_white')) # should display 'bar'

    print("hello called....")
    #response  = requests.get("https://api.covid19india.org/data.json")
    print("Hello world!")
    #print(response.json())
    data = raw

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
    print(colored('==========================new[]record===========================', 'green', 'on_red'))
    print(raw)
    
    return json.dumps({'errors': "errors"})




@application.route('/state', methods=['GET'])
def covidstate():
    data = json.load(session.get('data'))
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
    
    #print(innerHTML)
    global optionlist
    for keys in dict_state:
        print(dict_state[keys])
        optionlistobj="<option value={key:}>{value:}</option>"
        formattedoptionlistobj = optionlistobj.format(key=keys, value=dict_state[keys])
        optionlist += formattedoptionlistobj
    
    formatteddropdown = dropdown.format(options=optionlist)
    print(colored('==========================new[]record===========================', 'green', 'on_red'))
    
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
    session['data'] = json.dumps(data)
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
        #print(dict_state[keys])
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
    #out = subprocess.Popen(['python', 'punisher.py', 'start'], 
    #       stdout=subprocess.PIPE, 
    #       stderr=subprocess.STDOUT)

    #stdout,stderr = out.communicate()
    #print(stdout)
    #print(stderr)
    
    return formattedhtml_snippet



if __name__ == '__main__':
    application.run()
