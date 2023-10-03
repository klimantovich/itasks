import sys
import random
import secrets
import hmac
import hashlib
from prettytable import PrettyTable

class Rules:
    """Define Game Rules"""
    def __init__(self, count):
        self.moves_count = count
    def get_result(self, move1, move2):
        if move1 == move2: return "draw"
        if move2 > move1:
            if move2 - move1 <= (self.moves_count - 1)/2:
                return "lose"
            return "win"
        if move1 - move2 <= (self.moves_count - 1)/2:
            return "win"
        return "lose"


class Table:
    def __init__(self, moves):
        self.moves = moves
        self.header = moves.copy()
    tab = PrettyTable()
    
    def show(self):
        self.header.insert(0, "PC \\ User")
        result = Rules(len(self.moves))
        self.tab.field_names = self.header
        for i in range(len(self.moves)):
            row = []
            for j in range(len(self.moves)+1):
                if j == 0: 
                    row.append(self.moves[i])
                else:
                    r = result.get_result(j-1, i)
                    row.append(r)
            self.tab.add_row(row) 
        print(self.tab)

class Crypto:
    def __init__(self):
        pass

    def generate_key(self):
        return secrets.token_hex(32)

    def generate_hmac(self, key, message):
        k = b'key'
        m = b'message'
        return hmac.new(k, m, hashlib.sha3_256).hexdigest()

class Game:
    def __init__(self, moves):
        self.moves = moves

    def print_menu(self):
        print("Available Moves:")
        for number, el in enumerate(self.moves):
            print('{} - {}'.format(number+1, el))
        print("0 - Exit")
        print("? - Help")
    
    def make_turn(self):
        while (True):
            security = Crypto()
            key = security.generate_key()
            pc_move = random.randint(0, len(self.moves)-1)
            hmac = security.generate_hmac(key, moves[pc_move])
            print("HMAC: {}".format(hmac.upper()))
            self.print_menu()
            player_move = input("Enter you move: ")
            if player_move == '?':
                table = Table(self.moves)
                table.show()
                continue
            elif player_move == '0':
                return
            elif ((not player_move.isnumeric()) or int(player_move) <= 0) or (int(player_move) > len(self.moves)):
                print("\n")
                continue
            print('Your move: {}'.format(self.moves[int(player_move)-1]))
            print('Computer move: {}'.format(self.moves[pc_move]))
            #RULES
            rules = Rules(len(self.moves))
            result = rules.get_result(int(player_move)-1, pc_move)
            match result:
                case 'draw':
                    print("It's {}!".format(result))
                case _:
                    print('You {}!'.format(result))
            print("HMAC key: {}".format(key.upper()))
            print("\n")
            return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        moves = sys.argv[1:]   
        if len(moves) < 3 | len(moves) % 2 == 0:
            print("Invalid arguments: Number of options must be odd and >= 3")
        elif (len(moves) != len(set(moves))):
            print("Invalid arguments: Arguments should be different")
        else:
            game = Game(moves)
            game.make_turn()

    