import numpy as np
import matplotlib.pyplot as plt


# run with python or pythonw (for MacOS)


# __all__ = ['Host', 'Player', 'Board']

class Player:
    # class variables, shared by all instances of this class
    num_players = 0
    max_num_players: int

    # class variable maxNumPlayers has to be set before calling __init__
    def __init__(self, host):
        self.my_host = host
        print("anzahl gewünschte Spieler: ", self.max_num_players)
        # variables local to each created object
        self.number = Player.num_players
        self.high_score = 0
        Player.num_players = Player.num_players + 1
        if self.number == Player.max_num_players - 1:
            print("genügend Player vorhanden.")
        if self.number > Player.max_num_players - 1:
            print("zu viele Player. Oder Turniermodus. Oder losen, wer gegen wen spielt. Oder queueing for playing :-)")
        self.lastStoneAccepted = True

    def propose_stone(self):
        """asks a player to give two integers as coordinates where to put his/her stone.
		returns a position as a tuple or the string 'quit' """
        pos = [-1, -1]
        print("Type of pos ", type(pos))
        print("Du bist", self.get_my_number())
        # get position from player - person
        for i in range(2):
            pos[i] = input(f"gib {i + 1} -te Koordinate der Position an: ")
            # print("whatever ...")
            accept = False
            while (not accept) and not (pos == 'quit'):
                try:
                    int(pos[i])
                    accept = True
                    print("in try, prüfen auf int: accepted")
                except ValueError:
                    pos[i] = input("gib eine Zahl (Integer) ein oder schreibe quit:")

            # exit while with pos[i] either an interger input or the string 'quit'.

            if pos[i] == 'quit':
                print("exit input by typing quit. do something, interrupt whatever.")
                pos = 'quit'
        # end of for , both coordinates requested - or got input 'quit'

        pos = [int(pos[0]), int(pos[1])]
        print("return position", pos)
        return pos

    def negotiate_stone_position(self):

        while (not self.my_host.evaluate_stone(self.get_my_number(), self.propose_stone())):
            print("in while")

    def set_color(self, color):
        self.color = color
        print("I chose " + str(color))

    def get_num_player(self):
        return self.num_players

    def set_num_players(self, num_players):
        self.num_players = num_players

    @classmethod
    def set_max_number_of_players(class_, a_number):
        class_.max_num_players = a_number

    def get_my_number(self):
        return int(self.number)

    def get_other_player_number(self):
        """works for 2 players only"""
        return int((1 + self.number) % 2)


class Brett:
    """Brett soll das Model(l) sein, die Daten des Spieles enthalten. Von der Klasse soll es nur ein Objekt geben (Singleton?)."""

    # wenn es nur ein Objekt dieser Klasse gibt, wozu in Klassen- und Objektvariablen unterscheiden?
    # size = 6
    # brett is a dictionary with key a tupel of integers.
    # the value is 0 when empty, 1 when carrying a stone of player 1, 2 when carrying a stone of player 2
    # values are accessed or set through brett[(1,2)]

    def __init__(self, host, size: int):
        self.my_host = host
        self.size = size
        self.brett = {(k, l): -1 for k in range(self.size) for l in range(self.size)}
        self.score = []  # empty list
        self.accepted_stone = (-1, -1)
        self.max_number_stones = self.size * self.size

    # def setColor (self, color):

    def update_scores(self):
        self.score = [0, 0]

        b = list(self.brett.values())
        for i in range(2):
            self.score[i] = sum(1 for j in range(len(b)) if b[j] == i)

    def get_scores(self):
        return self.score

    def update_board(self, id):
        """When a player has put a new stone on the board newly includes / cought stones turn change color"""
        new_stone = self.accepted_stone
        directions = self.get_directions(new_stone)

        dir_touch_opponent = []

        for direction in directions:
            if self.brett[tuple(x + y for x, y in zip(new_stone, direction))] == (1 + id) % 2:
                dir_touch_opponent.append(direction)
        print("dir touch opponent ", dir_touch_opponent)

        dir_enclose_opponent = []

        for direction in dir_touch_opponent:
            pos = new_stone
            print("initial position ", pos)
            enclose = False
            decided = False
            while not decided:
                try:
                    next_field = self.brett[tuple(x + y for x, y in zip(pos, direction))]
                except KeyError:
                    decided = True

                if next_field == (1 + id) % 2:
                    pos = tuple(x + y for x, y in zip(pos, direction))
                    print("new position ", pos)
                elif next_field == id:
                    dir_enclose_opponent.append(direction)
                    enclose = True
                    decided = True
                else:
                    decided = True

        for direction in dir_enclose_opponent:
            pos = new_stone
            done = False
            while not done:
                next_stone_in_line = tuple(x + y for x, y in zip(pos, direction))
                if self.brett[next_stone_in_line] == (1 + id) % 2:
                    self.brett[next_stone_in_line] = id
                    pos = next_stone_in_line
                else:
                    done = True

    def print_brett(self):
        # it would be nice just to add one point innstead of printing all again from scratch
        k, v = zip(*self.brett.items())
        a = [k for k, v in self.brett.items() if v == 0]
        b = [k for k, v in self.brett.items() if v == 1]
        plt.plot([0, self.size - 1, 0, self.size - 1], [0, 0, self.size - 1, self.size - 1], marker='x', ls='')
        plt.plot(*zip(*a), marker='o', color='r', ls='')
        plt.plot(*zip(*b), marker='o', color='b', ls='')

        plt.draw()
        plt.show(block=False)

    def check_stone(self, id, position):
        print("in Brett : check Stone")
        # not catching the position outt of bounds, also zu groß
        # return brett.checkPositionExists(position) & brett.checkPositionFree(position) & brett.checkEncloseOpponent( id , position)
        if self.check_position_exists(position):
            if self.check_position_free(position):
                if self.check_enclose_opponent(id, position):
                    print("checkStone: OK")
                    return True

        return False

    def check_position_exists(self, position):
        print("in Brett : check position exists")
        if ((position[0] in range(self.size)) & (position[1] in range(self.size))):
            return True
        else:
            return False

    def check_position_free(self, position):
        print("in Brett : check position free")
        try:
            return self.brett[position] == -1
        except KeyError:
            return False

    def get_directions(self, position):
        all_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]

        d2 = [[x + y for x, y in zip(position, direction) if x + y in range(self.size)] for direction in all_directions]
        # for a position and direction: if the go beyond the brett it maybe only one coordinate is affected
        # first only this coordinate is removed. Resulting in tupels of length 0 or 1.
        # these shorter tupels are then removed
        mask = [len(d) == 2 for d in d2]
        # Problem with masking: arrays can be masked, lists cannot

        valid_directions = [all_directions[i] for i in range(8) if mask[i] == True]
        # print("directions d2: " , directions)

        return valid_directions

    def check_enclose_opponent(self, id, position):

        print("in Brett : check enclose opponent")

        directions = self.get_directions(position)

        dir_touch_opponent = []

        for direction in directions:
            if self.brett[tuple(x + y for x, y in zip(position, direction))] == (1 + id) % 2:
                dir_touch_opponent.append(direction)
        print("dir touch opponent ", dir_touch_opponent)

        if len(dir_touch_opponent) == 0:
            return False

        dirEncloseOpponent = []

        for direction in dir_touch_opponent:
            pos = position
            print("initial position ", pos)
            enclose = False
            decided = False
            while not decided:
                try:
                    next_field = self.brett[tuple(x + y for x, y in zip(pos, direction))]
                except KeyError:
                    decided = True

                if next_field == (1 + id) % 2:
                    pos = tuple(x + y for x, y in zip(pos, direction))
                    print("new position ", pos)
                elif next_field == id:
                    return True
                else:
                    decided = True

        return False

    # check that the set stone is adjacent to a stone of the opponent
    # check that there exists a direction such that in that direction
    # at some point lies a stone of the same colour as the set stone

    def set_stone(self, playerID, position):
        if self.check_stone(playerID, position):
            self.brett[position] = playerID
            self.accepted_stone = position
            # player.lastStoneAccepted = True
            return True
        else:
            print("Stone rejected.")
            return False

    def control_new_position(self, id, position):
        pass


class Host:

    def __init__(self):
        self.my_board: Board
        self.my_player: list

    def create_board(self, size):
        self.my_board = Brett(self, size)
        return self.my_board

    def setup_board(self):
        """soll man nicht machen: direkt auf die Daten zugreifen. Besser: Methode benutzen!"""
        self.my_board.brett[(1, 1)] = 0
        self.my_board.brett[(1, 2)] = 0
        self.my_board.brett[(2, 2)] = 1
        self.my_board.brett[(2, 1)] = 1

    # this should return something??

    def invite_players(self):
        pass

    def create_players(self, some_number):
        # set class variable first
        Player.set_max_number_of_players(some_number)

        p = []
        for i in range(some_number):
            p.append(Player(self))

        self.my_player = p

        return p

    def evaluate_stone(self, playerID, position):
        """Check stone and if OK set stone on board"""
        print("Übergebene Parameter ***")
        print(list(self.my_board.brett.values()))
        # print(player.getMyNumber)
        print(position)
        print("in host : evaluate stone")
        if self.my_board.check_stone(playerID, tuple(position)) == True:
            if self.my_board.set_stone(playerID, tuple(position)):
                self.my_player[playerID].lastStoneAccepted = True
                return True
        else:
            return False

    # def game_on(self):
    # return whether the game should go on.
    # is the next player allowed to continue ??
    # return True or False

    @staticmethod
    def next(i):
        return ((1 + i) % 2)


def main():
    print("Starte das Spiel")

    h = Host()

    b = h.create_board(4)

    h.setup_board()

    p = h.create_players(2)

    print(b.print_brett())

    b.update_scores()
    print("Punkte:", b.get_scores())

    game_on = True
    stones_set = 4  # for stones initially set when setting up the board

    current = 0
    last = 0
    max_number_of_turns = b.max_number_stones  # define getter for max_number_of_stones
    # better: move it all into Host or Board !!

    while game_on:
        p[current].negotiate_stone_position()

        # h.update_board()
        # the host updates the board. Information: Who was the last player and where was the stone put (if any WAS put)

        # in setStone the position of the last accepted stone is stored in Brett.acceptedStone
        # the same way you coud store the currently active player ...
        b.update_board(p[current].get_my_number())

        b.print_brett()
        # with the subscriber pattern in a network setting (client / server)  this should change

        b.update_scores()
        print("Punkte:", b.get_scores())

        last = current
        current = h.next(current)

        game_on = (p[last].lastStoneAccepted or p[current].lastStoneAccepted) and (stones_set < max_number_of_turns)

    print("game over")
    # should show a "game over" screen to each player

    scores_at_end = b.get_scores()
    print("Punktestand am Ende:", scores_at_end)
    if scores_at_end[0] > scores_at_end[1]:
        print("Player 1 wins")
    elif scores_at_end[0] < scores_at_end[1]:
        print("Player 2 wins")
    else:
        print("Both win.")


# the host should announce the winner


# Funktioniert nicht, die Eingabe zu prüfen.
# Eingabe 9,9 produziert Keyvalue Error und wird nicht abgefangen

if __name__ == "__main__":
    main()
