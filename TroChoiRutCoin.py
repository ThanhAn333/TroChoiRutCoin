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
    def current_player_name(self):
        return self.players[self.nplayer - 1].name

    def opponent(self):
        return 3 - self.nplayer

def main():
    
    st.title("Last Coin Standing")

    mode = st.radio("Chọn chế độ chơi:", ("Người với AI", "Người với Người"))

    if mode == "Người với AI":
        difficulty = st.selectbox("Chọn mức độ khó của AI:", ("Dễ", "Trung bình", "Khó"))
        difficulty_map = {"Dễ": 2, "Trung bình": 4, "Khó": 6}
        players = [Human_Player(name="Người chơi 1"), AI_Player(Negamax(depth=difficulty_map[difficulty]), name="Bot")]
    else:
        players = [Human_Player(name="Người chơi 1"), Human_Player(name="Người chơi 2")]

    start_game = st.button("Bắt đầu trò chơi")

    if start_game:
        game = LastCoinStanding(players)
        while not game.is_over():
            st.write(f"Còn {game.num_coins} tiền xu trong chồng")
            move = st.text_input(f"Nhập nước đi của người chơi {game.current_player_name}:", key=f"{game.current_player_name}_text_input")
            
            if st.button("Thực hiện nước đi"):
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
                        st.write(f"{game.current_player_name} đã thắng!")
                        break
                else:
                    st.write("Nước đi không hợp lệ. Hãy thử lại.")

if __name__ == "__main__":
    main()
