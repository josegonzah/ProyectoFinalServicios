import socket
import threading
msgFromClient="BUY, vodka, 1, 123456, 1234"
bytesToSend=str.encode(msgFromClient)
bufferSize          = 1024
serverAddressPort   = ("127.0.0.2", 5555)
def Connect2Server():
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)
print("Client - Main thread started")  
ThreadList  = []
ThreadCount = 10
for index in range(ThreadCount):
    ThreadInstance = threading.Thread(target=Connect2Server())
    ThreadList.append(ThreadInstance)
    ThreadInstance.start()
for index in range(ThreadCount):
    ThreadList[index].join()