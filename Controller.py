from tkinter import simpledialog

from GameTime import GameTime
from View import View
from Model import Model
from Score import Score


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)


    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()
        self.__view.draw_scoreboard(window,data)


    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end') # Sisestuskast tühjaks
        self.__view.char_input['state'] = 'disabled'

    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    def btn_new_click(self):
        self.buttons_to_game()
        # Muuda pilti id-ga 0
        #self.__view.change_image(self.__model.image_id)
        self.__view.change_image(0)
        self.__view.lbl_result['text'] = self.__model.get_secret_word()
        self.__view.lbl_error['fg'] = 'black'
        self.__view.lbl_error['text'] = f'Vigased tähed: '

        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__game_time.stop()
        self.buttons_no_game()
        self.__view.change_image(len(self.__model.image_files) - 1)

    def btn_send_click(self):
        letter_to_find = self.__view.char_input.get().lower()
        if letter_to_find != 1:
            letter = letter_to_find[0]
            letter_to_find = letter
        
        
        if self.__model.is_letter(letter_to_find.upper()):
            indices_of_letter = [index for index, letter in enumerate(self.__model.secret_word) if letter == letter_to_find]

            if indices_of_letter:
                for index in indices_of_letter:
                    word =list(self.__model.new_secret_word_string)
                    word[index] = letter_to_find
                    self.__model.new_secret_word_string = word
                self.__view.lbl_result['text'] = self.__model.new_secret_word_string

            else:
                self.__model.wrong_letters.append(letter_to_find)
                resulting_string = ','.join(self.__model.wrong_letters)
                self.__model.image_id += 1
                self.__view.change_image(self.__model.image_id)
                self.__view.lbl_error['fg'] = 'red'
                self.__view.lbl_error['text'] = f'Vigased tähed: {resulting_string}'


        self.__view.char_input.delete(0, 'end')
        if self.__model.image_id == 11:
            print('Game over!')
            self.buttons_no_game()
            self.__game_time.stop()
            self.__view.lbl_result['text'] = 'MÄNG LÄBI!'

        resulting_word = ''.join(self.__model.new_secret_word_string)
        if self.__model.secret_word == resulting_word:
            print('Game over!')
            self.buttons_no_game()
            self.__game_time.stop()
            time = self.__game_time.counter
            self.__model.seconds = int(time)
            self.ask_name()

        return
    def ask_name(self):
        name = simpledialog.askstring("Game over", "Game over" +'\n'+"What is the players name")
        if name == None:
            return
        else:
            self.__model.name = name.strip()
            self.__model.add_or_not_database()
