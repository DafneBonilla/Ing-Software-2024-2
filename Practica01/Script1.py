import random

# Class for the tennis match
class TennisMatch:
    def __init__(self):
        self.players = [self.get_player_name(1), self.get_player_name(2)]
        self.sets_to_win = 2  # Best of 3 sets
        self.score = [[0, 0, 0], [0, 0, 0]]  # [Won sets, won games, score in current game]
        self.winner = None
        self.current_server = random.randint(1, 2)
        self.games_played_in_set = 0
        self.sets_played = 0
        self.games_played = 0
    # Function to play the match
    def play_match(self):
        while not self.winner:
            self.current_server = self.play_set()
            if self.score[0][0] == self.sets_to_win:
                self.winner = self.players[0]
            elif self.score[1][0] == self.sets_to_win:
                self.winner = self.players[1]
        print(f"\nThe winner of the match is {self.winner}!!!")
    # Function to play a set
    def play_set(self):
        self.games_played_in_set = 0
        while True:
            self.sets_played += 1
            self.games_played_in_set = 0  # Reiniciar contador de juegos al comenzar un nuevo set
            self.print_set_score()
            self.current_server = self.play_game()
            if self.check_set_winner():
                return self.current_server
    # Function to show game number
    def play_game(self):
        while True:
            self.games_played_in_set += 1
            print(f"\nGame {self.games_played_in_set}")
            self.current_server = self.play_point()
            if self.check_game_winner():
                return self.current_server
    # Function to show serve and play a point
    def play_point(self):
        server = self.players[self.current_server - 1]
        receiver = self.players[2 - self.current_server]
        print(f"{server} serves")
        point_winner = self.get_point_winner(server, receiver)
        self.update_score(point_winner)
        return 3 - self.current_server
    # Function to get the point winner
    def get_point_winner(self, server, receiver):
        while True:
            try:
                point_winner = int(input(f"Enter the player who won the point (1 for {server}, 2 for {receiver}): "))
                if point_winner in [1, 2]:
                    return point_winner
                else:
                    print("Invalid input. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter 1 or 2.")
    # Function to update the score
    def update_score(self, point_winner):
        winner_index = point_winner - 1
        loser_index = 1 - winner_index
        winner_score = self.score[winner_index][2]
        loser_score = self.score[loser_index][2]
        if winner_score == "Ganador":
            self.score[winner_index][1] += 1
            self.score[winner_index][2] = 0
            self.score[loser_index][2] = 0
        elif winner_score == "AD" or loser_score == "AD":
            self.score[winner_index][2] = "Ganador"
            self.score[loser_index][2] = 0
        elif winner_score == 40 and loser_score == 40:
            self.score[winner_index][2] = "AD"
        elif winner_score == 40 or loser_score == "AD":
            self.score[winner_index][2] = "Ganador"
            self.score[loser_index][2] = 0
        elif winner_score == 30:
            self.score[winner_index][2] = 40
        elif winner_score == 15:
            self.score[winner_index][2] = 30
        elif winner_score == 0:
            self.score[winner_index][2] = 15
        self.score[winner_index][1] += 1
        self.print_score()
    # Function to check the game winner
    def check_game_winner(self):
        winner_score = self.score[self.current_server - 1][1]
        loser_score = self.score[2 - self.current_server][1]
        if winner_score >= 4 and winner_score - loser_score >= 2:
            self.score[self.current_server - 1][0] += 1
            self.score[self.current_server - 1][1] = 0
            self.score[2 - self.current_server][1] = 0
            print(f"{self.players[self.current_server - 1]} wins the game!")
            return True
        elif winner_score == 3 and loser_score == 3: 
            self.score[self.current_server - 1][2] = "AD"
            self.score[2 - self.current_server][2] = 40
        return False
    # Function to define a winner
    def check_set_winner(self):
        winner_score = self.score[self.current_server - 1][0]
        loser_score = self.score[2 - self.current_server][0]
        if winner_score >= 1 and winner_score - loser_score >= 1:
            return True
        return False
    # Function to show the set number
    def print_set_score(self):
        print(f"\nSet {self.sets_played}")
    # Function to show the score
    def print_score(self):
        print(f"Point Score: {self.players[0]}: {self.score[0][2]} - {self.score[1][2]} :{self.players[1]}")
        print(f"Game Score: {self.players[0]}: {self.score[0][1]} - {self.score[1][1]} :{self.players[1]}")
    # Function to get the player name
    def get_player_name(self, player_number):
        while True:
            player_name = input(f"Enter the name of player {player_number}: ")
            if player_name:
                return player_name
            else:
                print("Player name cannot be empty. Please enter a valid name.")
# Main program
tennis_match = TennisMatch()
tennis_match.play_match()
