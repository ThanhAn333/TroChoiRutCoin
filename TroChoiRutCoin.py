def main():
    st.title("Last Coin Standing")

    mode = st.radio("Chọn chế độ chơi:", ("Người với AI", "Người với Người"))

    if mode == "Người với AI":
        difficulty = st.selectbox("Chọn mức độ khó của AI:", ("Dễ", "Trung bình", "Khó"))
        difficulty_map = {"Dễ": 2, "Trung bình": 4, "Khó": 6}
        players = [Human_Player(), AI_Player(Negamax(difficulty_map[difficulty]))]
    else:
        players = [Human_Player(), Human_Player()]

    player_names = []
    for i in range(2):
        player_name = st.text_input(f"Tên người chơi {i+1}:", f"Người chơi {i+1}")
        player_names.append(player_name)

    start_game = st.button("Bắt đầu trò chơi")

    if start_game:
        game = LastCoinStanding(players)
        while not game.is_over():
            st.write(f"Còn {game.num_coins} tiền xu trong chồng")
            move = st.text_input(f"Nhập nước đi của người chơi {game.current_player}:", key=f"move_{game.current_player}")
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

if __name__ == "__main__":
    main()
