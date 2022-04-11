import pickle
import socket
from _thread import *

"""
The server
creates to players for our game 
receives and send the data both players to their connected clients
only listens to 2 clients at a time representing out players 
"""
from multiplayer.basic_demo.player import Player

server = "127.0.0.1"  # ip of this server
port = 5555  # port number used to receive and send packets

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))  # bind socket to the server
except socket.error as err:
    str(err)

s.listen(2)  # start listening for incoming connections ( 2 simultaneously )

print("Waiting for connection, server started!")

# initialize and array of player objects and diff. positions
players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 255, 0))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))  # encode and send a player object
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # receive and deserialize a data object
            players[player] = data  # update  player properties with received data

            if not data:  # no data received
                print("Disconnected")
                break
            else:  # prepare other player object to send in response
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received", data)
                print("Sending", reply)

            conn.send(pickle.dumps(reply))  # send serialized object of player object
        except socket.error as e:
            print(e)
            break

    print("Lost connection")
    conn.close()  # should always close socket connection when there's an error


currentPlayer = 0
while True:
    connection, address = s.accept()  # destructure the properties of accepted incoming connection
    print("connected to:", address)

    # create a new background thread
    start_new_thread(threaded_client, (connection, currentPlayer))
    currentPlayer += 1  # updates the player turn
