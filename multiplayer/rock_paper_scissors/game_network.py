class Game:

    def __init__(self, _id):
        self.p1MadeMove = False  # player 1 took his turn flag
        self.p2MadeMove = False  # player 2 took his turn flag
        self.ready = False  # game is ready to play flag ( both player present )
        self.id = _id
        self.moves = ["", ""]   # hold the action played by each of the two players
        self.wins = [0, 0]  # hold which player or both played status
        self.ties = 0   # if it's a tie game

    def get_player_moves(self, p):
        """
        :param p: [0,1]
        :return: player move
        """
        return self.moves[p]

    def play(self, player, move):
        """

        :param player: the player number
        :param move: the string representing the move the player chose
        :return:
        """
        self.moves[player] = move

        # update player turn flags based on player number
        if player == 0:
            self.p1MadeMove = True
        else:
            self.p2MadeMove = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1MadeMove and self.p2MadeMove

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1

        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetPlays(self):
        """
        reset both players status to false

        """
        self.p1MadeMove = False
        self.p2MadeMove = False





