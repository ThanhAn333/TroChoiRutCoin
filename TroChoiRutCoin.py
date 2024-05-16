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
        self.nplayer = 3 - self.nplayer

    @property
    def current_player(self):
        return self.nplayer

    def opponent(self):
        return 3 - self.nplayer

def main():
    
    st.title("Last Coin Standing")

    mode = st.radio("Chọn chế độ chơi:", ("Người với AI", "Người với Người"))

    if mode == "Người với AI":
        difficulty = st.selectbox("Chọn mức độ khó của AI:", ("Dễ", "Trung bình", "Khó"))
        difficulty_map = {"Dễ": 2, "Trung bình": 4, "Khó": 6}
        players = [Human_Player(), AI_Player(Negamax(depth=difficulty_map[difficulty]))]
    else:
        players = [Human_Player(), Human_Player()]

    player_names = []
    for i in range(2):
        player_name = st.text_input(f"Tên người chơi {i+1}:", f"Người chơi {i+1}")
        player_names.append(player_name)

    start_game = st.button("Bắt đầu trò chơi")

     if start_game:
        game = LastCoinStanding(players)
        count = 0
        while not game.is_over():
            st.write(f"Còn {game.num_coins} tiền xu trong chồng")
            move = st.text_input(f"Nhập nước đi của người chơi {game.current_player}:", key=count)
            
            submit_button = st.button("Thực hiện nước đi")
            if submit_button:
                if game.is_valid_move(move):
                    game.make_move(move)
                    if not game.is_over():
                        game.switch_player()
                        if isinstance(game.players[game.nplayer - 1], AI_Player):
                            ai_move = game.get_move()
                            game.make_move(ai_move)
                            if not game.is_over():
                                game.switch_player()
                    else:
                        winner_index = game.opponent_index() - 1 if mode == "Người với AI" else game.nplayer - 1
                        winner_name = "Bot" if winner_index == 1 else player_names[0]
                        st.write(f"{winner_name} đã thắng!")
                        break
                else:
                    st.write("Nước đi không hợp lệ. Hãy thử lại.")
            
            count += 1

if __name__ == "__main__":
    main()
