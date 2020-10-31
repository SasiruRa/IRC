import threading
import socket

host = "127.0.0.1"
port = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []


def boardcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            boardcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            boardcast('{} left the chat!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print("connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print('Nickname of the client is {}'.format(nickname))

        boardcast("{} joined the chat".format(nickname).encode('ascii'))
        client.send("connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listning")
receive()
