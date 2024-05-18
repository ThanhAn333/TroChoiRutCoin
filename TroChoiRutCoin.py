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

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def main():
    st.title("Trò Chơi Rút Xu Cuối Cùng")
    st.sidebar.title("Hướng dẫn trò chơi")
    
    st.sidebar.markdown("""
    - Mục tiêu: Không rút xu cuối cùng từ chồng tiền xu.
    - Mỗi lượt, người chơi có thể rút từ 1 đến 4 xu.
    - Người chơi nào rút xu cuối cùng làm cho chồng xu trở thành rỗng sẽ thua cuộc.
    """)
    
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
        st.session_state.game = LastCoinStanding(players)
        st.session_state.move_count = 0
        st.session_state.game_over = False
        st.session_state.current_player_name = player_names[0]
        st.session_state.mode = mode

    if 'game' in st.session_state and not st.session_state.game_over:
        game = st.session_state.game
        move_count = st.session_state.move_count
        
        st.write(f"Còn {game.num_coins} tiền xu trong chồng")
        
        if isinstance(game.players[game.current_player - 1], Human_Player):
            move = st.text_input(f"Nhập nước đi của {st.session_state.current_player_name}:", key=f"move_input_{move_count}")
            submit_button = st.button("Thực hiện nước đi", key=f"submit_button_{move_count}")
            if submit_button:
                if game.is_valid_move(move):
                    game.make_move(move)
                    move_count += 1
                    st.session_state.move_count = move_count
                    if game.is_over():
                        st.session_state.game_over = True
                        if st.session_state.mode == "Người với AI":
                            if isinstance(game.players[game.current_player - 1], AI_Player):
                                st.write(f"Chúc mừng {player_names[0]}! Bạn đã thắng!")
                            else:
                                st.write("AI đã thắng!")
                        else:
                            winner = player_names[game.opponent() - 1]
                            st.write(f"Chúc mừng {winner}! Bạn đã thắng!")
                    else:
                        game.switch_player()
                        st.session_state.current_player_name = player_names[game.current_player - 1]
                        if isinstance(game.players[game.current_player - 1], AI_Player):
                            ai_move = game.get_move()
                            st.write(f"AI chọn: {ai_move}")
                            game.make_move(ai_move)
                            move_count += 1
                            st.session_state.move_count = move_count
                            if game.is_over():
                                st.session_state.game_over = True
                                st.write(f"Chúc mừng {player_names[0]}! Bạn đã thắng!")
                            else:
                                game.switch_player()
                                st.session_state.current_player_name = player_names[game.current_player - 1]
                else:
                    st.write("Nước đi không hợp lệ. Hãy thử lại.")
        else:
            ai_move = game.get_move()
            st.write(f"AI chọn: {ai_move}")
            game.make_move(ai_move)
            move_count += 1
            st.session_state.move_count = move_count
            if game.is_over():
                st.session_state.game_over = True
                st.write(f"Chúc mừng {player_names[0]}! Bạn đã thắng!")
            else:
                game.switch_player()
                st.session_state.current_player_name = player_names[game.current_player - 1]
    if st.session_state.get('game_over', False):
        if st.button("Chơi lại"):
            reset_game()
            st.experimental_rerun()
if __name__ == "__main__":
    main()
