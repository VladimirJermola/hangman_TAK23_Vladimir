class Score:
    def __init__(self, name, word, missing, seconds, time):
        self.__name = name
        self.__word = word
        self.__missing = missing
        self.__seconds = seconds
        self.__time = time

    @property
    def name(self):
        return self.__name

    @property
    def word(self):
        return self.__word

    @property
    def missing(self):
        return self.__missing

    @property
    def seconds(self):
        return self.__seconds

    @property
    def time(self):
        return self.__time
'''
    @name.setter
    def name(self, value):
        self.__name = value

    @word.setter
    def word(self, value):
        self.__word = value

    @missing.setter
    def missing(self, value):
        self.__missing = value

    @seconds.setter
    def seconds(self, value):
        self.__seconds = value

    @time.setter
    def time(self, value):
        self.__time = value
'''
