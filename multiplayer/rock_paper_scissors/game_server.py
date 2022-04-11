import pickle
import socket
from _thread import *
from game_network import Game

from multiplayer.basic_demo.player import Player

server = "127.0.0.1"
port = 5555
#  initiate socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the defined ip,port address
try:
    s.bind((server, port))
except socket.error as err:
    str(err)

#  socket will handle 2 simultaneous connections at once for both players
s.listen(2)

print("Waiting for connection, server started!")

connected = set()  # connection set
games = {}  # list of connected games
idCount = 0


def threaded_client(conn, player_, gameId_):
    """

    :param conn: the connected socket
    :param player_: the player id
    :param gameId_: the current game id
    :return:
    """
    global idCount
    conn.send(str.encode(str(player_)))  # send encoded string representing the current player id

    reply = ""
    while True:
        data = conn.recv(4096).decode()  # from received string get the game data/state

        # check the current game is referenced in the games list
        try:
            if gameId_ in games:
                game = games[gameId_]

                if not data:
                    break
                else:
                    if data == "reset":  # reset the game
                        game.resetPlays()
                    elif data != "get":  # if not get
                        game.play(player_, data)    # store the current player move and switch flag to other player

                    reply = game
                    conn.send(pickle.dumps(reply))  # send current game data/status object serialized, this keeps the
                    # game alive by sending updated status to player(s)

            else:   # terminate game
                break
        except:
            break

    print("Lost connection")

    # if game is terminated try to delete the game id reference from list
    try:
        del games[gameId_]
        print("Closing game", gameId_)
    except:
        pass

    idCount -= 1
    conn.close()


while True:
    connection, address = s.accept()  # accept incoming socket connection and destructure it
    print("connected to:", address)

    idCount += 1  # update player id count
    player = 0  # start with player id 0
    gameId = (idCount - 1) // 2  # calculate the floor of game id

    # if so far one player joined create a new game and store it in games list
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("creating a new game ...")
    else:  # to players are present set tracked game object ready flag to true
        games[gameId].ready = True
        player = 1  # set current payer to player 1

    # start a separate thread for the game in the background
    start_new_thread(threaded_client, (connection, player, gameId))
