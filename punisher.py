#!/usr/bin/env python
import os
import pika
import sys
import requests
import json
from termcolor import colored
class publish:

    def __init__(self,queue_name):
        self.response = requests.get("https://api.covid19india.org/data.json")
        #self.connection = pika.BlockingConnection(pika.URLParameters("amqp://fovucomg:iXDPcLo0zLE4tcjYU-fKZAIyxeXv2143@codfish.rmq.cloudamqp.com/fovucomg"))
        self.connection = pika.BlockingConnection(pika.URLParameters(os.environ.CLOUDAMQP_URI))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, durable=True)

    def start(self, queue_name):
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    def stop(self, queue_name):
        self.channel.stop_consuming()

    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        #self.response = body
        self.callAPI()
        
        response = requests.post("http://localhost:5000/raw",data=self.response)


    def callAPI(self):
        #self.response = ""
        new_response  = requests.get("https://api.covid19india.org/data.json")
        #print(new_response.json())
        old_response = self.response
        #print(old_response)
        result = old_response if json.dumps(old_response.json()) == json.dumps(new_response.json()) else new_response.json()
        print(colored('Updated', 'green', 'on_white'))
        self.response = result
        


def main(argv):
    print("argvs ",argv)
    msg = publish("sample_rabbit_queue")
    msg.callAPI()
    if argv == "start" :
        msg.start("sample_rabbit_queue")
    if argv=="stop" :
        msg.stop("sample_rabbit_queue")

if __name__ == "__main__":
    print("call main function")
    main(sys.argv[1])
