#open tcp-ip client and try to connect to mission planner

import socket
import time
import threading

def connectMissionPlanner(IP, Port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, Port))
    return client

def sendMissionPlanner(client, message):
    client.send(message.encode())


def main():
    IP = "0.0.0.0"
    Port = 5763
    client = connectMissionPlanner(IP, Port)
    #print the message
    message = "Hello World"
