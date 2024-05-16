import streamlit as st
from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player

class LastCoinStanding(TwoPlayerGame):
    def __init__(self, players, player_names, initial_coins=25, max_coins_per_turn=4):
        self.players = players
        self.player_names = player_names
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

    def get_winner_name(self):
        return self.player_names[self.opponent() - 1]

def main():
    st.title("Last Coin Standing")
    
    player_names = [st.text_input(f"Người chơi {i+1} tên là:", value=f"Người chơi {i+1}") for i in range(2)]
    difficulty = st.selectbox("Chọn mức độ khó của AI:", ["Dễ", "Trung bình", "Khó"])
    difficulty_map = {"Dễ": 2, "Trung bình": 4, "Khó": 6}
    difficulty_level = difficulty_map[difficulty]

    if st.button("Bắt đầu trò chơi", key="start_game"):
        if len(set(player_names)) < 2:
            st.write("Tên người chơi phải khác nhau và không được để trống.")
        else:
            ai_player = AI_Player(Negamax(difficulty_level))
            human_player = Human_Player()
            game = LastCoinStanding([human_player, ai_player], player_names)
            st.session_state.game = game

    if "game" in st.session_state:
        game = st.session_state.game
        
        if not game.is_over():
            st.write(f"Còn {game.num_coins} tiền xu trong chồng")
            
            if game.current_player == 1:
                move = st.text_input("Người chơi 1, nhập nước đi:", key="move_1")
                if st.button("Thực hiện nước đi", key="move_button_1"):
                    if game.is_valid_move(move):
                        game.make_move(move)
                        game.switch_player()
                        st.session_state.move_1 = ""  # Clear the input after move
                    else:
                        st.write("Nước đi không hợp lệ. Hãy thử lại.")
            else:
                st.write("AI đang chơi...")
                ai_move = game.get_move()
                game.make_move(ai_move)
                game.switch_player()

        if game.is_over():
            winner_name = game.get_winner_name()
            st.write(f"{winner_name} đã thắng!")
            if st.button("Chơi lại", key="play_again"):
                del st.session_state.game

if __name__ == "__main__":
    main()
