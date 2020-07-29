#!/usr/bin/env python
import os
import pika
import sys
import requests
import json
from termcolor import colored
class publish:

    def __init__(self,consume_queue_name, publish_queue_name):
        self.con_queue_name = consume_queue_name
        self.pub_queue_name = publish_queue_name
        print(self.con_queue_name)
        print(self.pub_queue_name)
        self.response = requests.get("https://api.covid19india.org/data.json")
        #self.connection = pika.BlockingConnection(pika.URLParameters("amqp://fovucomg:iXDPcLo0zLE4tcjYU-fKZAIyxeXv2143@codfish.rmq.cloudamqp.com/fovucomg"))
        self.connection = pika.BlockingConnection(pika.URLParameters(os.environ.get("CLOUDAMQP_URI"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.con_queue_name, durable=True)
        self.channel.queue_declare(queue=self.pub_queue_name, durable=True)

    def start(self):
        
        self.channel.basic_consume(queue=self.con_queue_name, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    def stop(self, queue_name):
        self.channel.stop_consuming()

    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        #self.response = body
        self.callAPI()
        #if type(self.response) is dict :
            #print("dict")
        #print(type(json.dumps(self.response.json())))
        #print(json.dumps(self.response))
        
        #print(colored(response.json(),'green','on_red'))
        #param={'raw':'aaaaa'}
        #strURI="http://flask-requests-json-meessage.apps.us-east-1.starter.openshift-online.com/raw?raw={params}"
        #formattedstrURI = strURI.format(params=json.dumps(self.response.json()))
        #print(formattedstrURI)
        #response = requests.get(formattedstrURI)
        #print(type(response))        
        #print(colored(str(response),'green','on_red'))



    def callAPI(self):
        #self.response = ""
        new_response  = requests.get("https://api.covid19india.org/data.json")
        #print(new_response.json())
        old_response = self.response
        #print(old_response)
        result = self.assignResponse(old_response,'same') if json.dumps(old_response.json()) == json.dumps(new_response.json()) else self.assignResponse(new_response, 'updated')
        
        self.response = result
        
    def assignResponse(self,returns, status):
        from datetime import datetime
        # datetime object containing current date and time
        now = datetime.now()
        print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)	
        print(colored(status+':'+dt_string, 'green', 'on_white'))

        #if status=="updated" :
        self.publishAPIMessage()

        return returns

    def callServerAPI(self):
        parampost = "{params}"
        formattedparam = parampost.format(params = json.dumps(self.response.json()))
        param={'raw':formattedparam}
        response = requests.post("http://flask-requests-json-meessage.apps.us-east-1.starter.openshift-online.com/rawpost",data=param)
        
    def publishAPIMessage(self):
        parampost = "{params}"
        formattedparam = parampost.format(params = json.dumps(self.response.json()))
        param={'raw':formattedparam}
        self.channel.queue_declare(queue=self.pub_queue_name, durable=True)
        self.ROUTING_KEY = self.pub_queue_name
        self._channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY,json.dumps(param, ensure_ascii=False))

def main(argv):
    print("argvs ",argv)
    msg = publish("callAPIRequest","consumeAPIResponse")
    msg.callAPI()
    if argv == "start" :
        msg.start()
    if argv=="stop" :
        msg.stop("callAPIRequest")

if __name__ == "__main__":
    print("call main function")
    main(sys.argv[1])
