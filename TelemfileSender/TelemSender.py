import time
import json
from threading import Thread
import os
import socket
import zlib


def GetFiles(fileloc: str, fileType: str):
    files = [os.listdir(fileloc)]
    FilesList = []
    for temp in files:
        if len(temp) != 0:

            for g in range(len(temp)):
                if temp[g].endswith(fileType):
                    FilesList.append(temp[g])
                    pass
    return FilesList


dirTek = "TeknoTelem/"  # teknofest telemetrilerin klasörü
dirTel = "Telems/"  # kırmızı kanatların telemetri klasörü
teknoTelemFiles = GetFiles(dirTek, ".json")
myTelemFiles = GetFiles(dirTel, ".json")
#
# okuduğu dosya biterse o thread hata verir
#
#
timeMult = 2  # hız kat sayısı ne kadar arttırılırsa o kadar hızlı verileri gönderir

SendTekno = True  # teknofest verilerini gönder
SendTelem = True  # kırmızı kanatların telemetri verilerini gönder


def SendMessageTCP(Data="", IP='', Port=0, compress=False, receive=False, PacketSize=65536):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # soketi oluştur ve client olarak ata
    client.settimeout(0.8)
    client.connect((IP, Port))  # soketi bağla

    if compress:

        client.send(zlib.compress(Data.encode("utf-8")))  # mesajı sıkıştır gönder
    else:
        client.send(Data.encode("utf-8"))  # mesajı sıkıştırmadan gönder
        # mesaj var ise al
    if receive:
        a = client.recv(PacketSize)
        return a.decode("utf-8")
    return ""


def SendMessageUDP(Data="", IP='', Port=0, compress=False, receive=False):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # soketi oluştur ve client olarak ata
    if compress:
        client.sendto(zlib.compress(Data.encode("utf-8")), (IP, Port))  # mesajı sıkıştır gönder
    else:
        client.sendto(Data.encode("utf-8"), (IP, Port))  # mesajı sıkıştırmadan gönder
    if receive:
        a = client.recvfrom(65536)  # mesaj var ise al
        mess, addr = a
        return mess.decode("utf-8"), addr
    return ""


def Read(FileName):
    with open(FileName) as file:  # json dosyasını aç
        return file.readlines()  # verileri oku


def TeknoSend(fileList, dir):
    a = 790
    print("TeknoStarted")
    while 1:
        time.sleep(1 / timeMult)
        msg = Read(dir + fileList[a])
        try:  # tcp bağlantılarını tryın içine yaz

            SendMessageTCP(msg[0], "127.0.0.1", 2589, receive=False, compress=False)
        except Exception as e:
            pass
        SendMessageUDP(msg[0], "127.0.0.1", 8052, receive=False, compress=True)
        SendMessageUDP(msg[0], "127.0.0.1", 5006, receive=False, compress=False)
        a += 1

def readMessageTCP(IP='', Port=0, PacketSize=65536):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # soketi oluştur ve client olarak ata
    client.settimeout(0.8)
    client.connect((IP, Port))  # soketi bağla
    a = client.recv(PacketSize)
    return a.decode("utf-8")

def readMessageUDP(IP='', Port=0, PacketSize=65536):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # soketi oluştur ve client olarak ata
    client.settimeout(0.8)
    client.connect((IP, Port))  # soketi bağla
    a = client.recv(PacketSize)
    return a.decode("utf-8")


            

def Telemend(telList, dir):
    b = 0

    print("TelemStarted")
    while 1:
        time.sleep(0.3 / timeMult)
        msg = Read(dir + telList[b])
        msg = json.loads(msg[0])
        fulmes = msg

        msg = msg["telem"]
        msg = [json.dumps(msg)]
        try:  # tcp bağlantılarını tryın içine yaz
            pass
            # SendMessageTCP(json.dumps(fulmes)+"1", "127.0.0.1", 13000, receive=False, compress=False)
        except Exception as e:
            pass

        SendMessageUDP(msg[0], "127.0.0.1", 5005, receive=False)
        SendMessageUDP(msg[0], "127.0.0.1", 8053, receive=False, compress=True)

        b += 1


if (SendTekno):
    Thread(target=TeknoSend, args=(teknoTelemFiles, dirTek),daemon=True).start()

Telemend(myTelemFiles, dirTel)
