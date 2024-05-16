import streamlit as st
from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player

class LastCoinStanding(TwoPlayerGame):
    def __init__(self, players, initial_coins=25, max_coins_per_turn=4):
        self.players = players
        self.nplayer = 1
        self.num_coins = initial_coins
        self.max_coins = max_coins_per_turn

    def possible_moves(self):
        return [str(x) for x in range(1, min(self.max_coins, self.num_coins) + 1)]

    def make_move(self, move):
        self.num_coins -= int(move)

    def win(self):
        return self.num_coins == 0

    def is_over(self):
        return self.win()

    def scoring(self):
        return 100 if self.win() else 0

    def is_valid_move(self, move):
        return move.isdigit() and 1 <= int(move) <= min(self.max_coins, self.num_coins)

    def switch_player(self):
        self.nplayer = 3 - self.nplayer  # Chuyển đổi sang người chơi tiếp theo

    @property
    def current_player(self):
        return self.nplayer

    def opponent(self):
        return 3 - self.nplayer

class AI_Player(Human_Player):
    def __init__(self, AI_algo):
        self.AI_algo = AI_algo

    def get_move(self, game):
        move = self.AI_algo(game)
        return str(move)

def main():
    st.title("Last Coin Standing")

    play_mode = st.radio("Chọn chế độ chơi:", ("Người với AI", "Người với Người"))
    player_names = []
    for i in range(2):
        player_name = st.text_input(f"Nhập tên của Người chơi {i+1}:", f"Người chơi {i+1}")
        player_names.append(player_name)

    difficulty_level = st.selectbox("Chọn mức độ khó của AI:", ("Dễ", "Trung bình", "Khó"))

    if st.button("Bắt đầu trò chơi"):
        if len(set(player_names)) < 2:
            st.write("Tên người chơi phải khác nhau và không được để trống.")
        else:
            difficulty_map = {"Dễ": 2, "Trung bình": 4, "Khó": 6}
            difficulty = difficulty_map[difficulty_level]
            if play_mode == "Người với AI":
                players = [Human_Player(), AI_Player(Negamax(difficulty))]
            else:
                players = [Human_Player(), Human_Player()]

            game = LastCoinStanding(players)
            play_game(game, player_names)

def play_game(game, player_names):
    move_number = 0  # Initialize move number
    while not game.is_over():
        st.write(f"Còn {game.num_coins} tiền xu trong chồng")

        current_player_name = player_names[game.current_player - 1]
        move_number += 1  # Increment move number
        form_key = f"player_{game.current_player}_form"  # Generate unique key for form
        move_key = f"move_{move_number}"  # Generate unique key for text input
        with st.form(key=form_key):
            move = st.text_input(f"{current_player_name}, nhập nước đi:", key=move_key)
            submit_button = st.form_submit_button("Thực hiện nước đi")
            if submit_button:
                if game.current_player == 1:
                    if game.is_valid_move(move):
                        game.make_move(move)
                        game.switch_player()
                    else:
                        st.write("Nước đi không hợp lệ. Hãy thử lại.")
                else:
                    st.write("AI đang chơi...")
                    ai_move = game.get_move()
                    game.make_move(ai_move)
                    game.switch_player()

    winner_name = player_names[game.opponent() - 1]
    st.write(f"{winner_name} đã thắng!")

if __name__ == "__main__":
    main()
