from datetime import datetime
import glob
import random
import sqlite3
from tkinter import messagebox

from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db' # Andmebaas
        # pip install Pillow => vajalik piltidega majandamiseks
        self.__image_files = glob.glob('images/*.png') # list mängu piltidega
        self.__secret_word = None
        self.__new_secret_word_string = None
        self.__wrong_letters = []
        self.__image_id = 0
        self.__name = None
        self.__seconds = None

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def secret_word(self):
        return self.__secret_word

    @property
    def new_secret_word_string(self):
        return self.__new_secret_word_string

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def image_id(self):
        return self.__image_id

    @property
    def name(self):
        return self.__name

    @property
    def seconds(self):
        return self.__seconds

    @database.setter
    def database(self, value):
        self.__database = value

    @secret_word.setter
    def secret_word(self, value):
        self.__secret_word = value

    @new_secret_word_string.setter
    def new_secret_word_string(self, value):
        self.__new_secret_word_string = value

    @wrong_letters.setter
    def wrong_letters(self, value):
        self.__wrong_letters = value

    @image_id.setter
    def image_id(self, value):
        self.__image_id = value

    @name.setter
    def name(self, value):
        self.__name = value

    @seconds.setter
    def seconds(self, value):
        self.__seconds = value

    def read_scores_data(self):
        """
        Loeb andmabaasi tabelist edetabel kõik kirjed
        :return:
        """
        connection = None
        try:
            connection = sqlite3.connect(self.database)
            sql = "SELECT * FROM scores ORDER BY seconds;"
            cursor = connection.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))

            return result
        except sqlite3.Error as error:
            print(f'Viga ühenduda andmebaasiga {self.__database}: {error}')
        finally:
            if connection:
                connection.close()

    def add_or_not_database(self):
        connection = None
        if self.__name:
            try:
                connection = sqlite3.connect(self.database)
                today = datetime.now().strftime("%Y-%m-%d %T")
                resulting_string = ','.join(self.wrong_letters)
                sql = 'INSERT INTO scores' + '(name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?);'
                connection.execute(sql, (self.name, self.secret_word, resulting_string.upper(), self.seconds, today))
                connection.commit()
            except sqlite3.Error as error:
                print(f"Viga ühenda andmebaasi {self.__database}: {error}")
            finally:
                if connection:
                    connection.close()

    def get_new_word(self):
        connection = None
        try:
            #connection = sqlite3.connect(self.word_database)
            #sql = "SELECT word FROM words;"
            connection = sqlite3.connect(self.database)
            sql = "SELECT word FROM words;"
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            number_entries = len(data)
            n = random.randint(0, int(number_entries) -1)
            word = data[n]
            return word
        except sqlite3.Error as error:
            print(f'Viga ühenduda andmebaasiga {self.__word_database}: {error}')
        finally:
            if connection:
                connection.close()

    def get_secret_word(self):
        secret_word = self.get_new_word()
        secret_word_string = ''.join(secret_word)
        self.__secret_word = secret_word_string.lower()
        print(self.secret_word)
        new_secret_word_string = '_' * len(secret_word_string)
        self.__new_secret_word_string = new_secret_word_string
        return self.__new_secret_word_string


    def is_letter(self, letter):
        if letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZÜÕÖÄ':
            messagebox.showinfo("Viga", "Palun sisestage TÄHT!", icon="error")
            #print('Please enter a LETTER.')
            return False
        else:
            return True
