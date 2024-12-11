import curses
from time import time
import random
from collections import defaultdict
from load_data import load_data

ESPACE = '•'

class data_tools:
    def __init__(self, words):
        self.words = words
        self.count_most_use_letter()

    def count_most_use_letter(self):
        letter_count = defaultdict(int)

        for word in self.words:
            for letter in word:
                letter_count[letter] += 1

        self.most_frequent_letter = list(dict(sorted(letter_count.items(), key=lambda item: item[1], reverse=True)))
    
    def get_word(self, nbr_letters : int, nbr_word : int) -> list:
        letters_set = set(self.most_frequent_letter[:nbr_letters])

        mots_trouves = [mot for mot in self.words if set(mot).issubset(letters_set)]
        
        return random.sample(mots_trouves, min(nbr_word, len(mots_trouves)))

class time_information:
    def __init__(self, sentence : str):
        self.time_session = None
        self.time_by_letter = []
        
        self.letter_time = None
        
        self.sentence = sentence
    
    def start_letter(self):
        self.letter_time = time()
    
    def end_letter(self):
        self.time_by_letter.append(time() - self.letter_time)
        self.letter_time = time()
    
    def start_test(self):
        self.time_session = time()
        self.start_letter()
    
    def end_test(self):
        self.time_session = time() - self.time_session
        self.time_by_letter.pop(0)
    
    def reset(self):
        self.__init__()
    
    def get_wpm_word(self):
        return (len(self.sentence.split(ESPACE)) / (self.time_session/ 60))
    
    def mean_wpm_letter(self):
        return sum(self.time_by_letter) / len(self.time_by_letter)

class kyboard:
    def __init__(self):
        self.position = 0
        
        self.past_letter = []
            
        self.setting = {'nbr_word' : 30, 'nbr_letter' : 15}
        self.data = load_data().data
        self.data_tools = data_tools(self.data)
        self.sentence = self.data_tools.get_word(self.setting['nbr_letter'], self.setting['nbr_word'])
        self.sentence = "•".join(self.sentence)
        
        self.time_info = time_information(self.sentence)
        
        self.init_screen()
        self.loop()
                    
    def init_screen(self):    
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # error typed text
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Current character
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)  # good typed text
    
    # def print(self):
    #     self.stdscr.clear()
    #     # Display
    #     for i in range(len(self.sentence[:self.position])):
    #         self.stdscr.addstr(0, i, self.sentence[i], curses.color_pair(3) if self.past_letter[i] else curses.color_pair(1))
    #     self.stdscr.addstr(0, self.position, self.sentence[self.position], curses.color_pair(2))
    #     self.stdscr.addstr(0, self.position + 1, self.sentence[self.position + 1:])
    #     self.stdscr.refresh()
    
    # def print(self):
    #     height, width = self.stdscr.getmaxyx()
    #     rang = 0 
    #     col = 0
        

    #     for i, letters in enumerate(self.sentence):
    #         if col + 1 >= width:
    #             rang += 1
    #             col = 0  # Réinitialiser la colonne
    #         if i < len(self.past_letter):
    #             self.stdscr.addstr(rang, col, self.sentence[i], curses.color_pair(3) if self.past_letter[i] else curses.color_pair(1))
    #         else:
    #             self.stdscr.addstr(rang, col, letters, curses.color_pair(3))
    #         if i == self.position:
    #             self.stdscr.addstr(rang, col, letters, curses.color_pair(2))

    #         col += 1
                
    #     self.stdscr.refresh()

    def print(self):
        height, width = self.stdscr.getmaxyx()
        rang, col, i = 0, 0, 0
        
        def print_char(letter):
            if i < len(self.past_letter):
                self.stdscr.addstr(rang, col, letter, curses.color_pair(3) if self.past_letter[i] else curses.color_pair(1))
            else:
                self.stdscr.addstr(rang, col, letter, curses.color_pair(3))
            if i == self.position:
                self.stdscr.addstr(rang, col, letter, curses.color_pair(2))

        liste_words = self.sentence.split(ESPACE)
        for word in liste_words:
            if len(word) + col >= width:
                rang +=1
                col = 0
            for letters in word:
                if col + 1 >= width:
                    rang += 1
                    col = 0  # Réinitialiser la colonne
                print_char(letters)

                col += 1
                i += 1
            if liste_words.index(word) == len(liste_words) - 1:
                break
            if col + 1 >= width:
                rang += 1
                col = 0  # Réinitialiser la colonne
            
            print_char(ESPACE)
                
            col += 1
            i += 1
                
        self.stdscr.refresh()

    
    def kyboard(self):
        key = self.stdscr.getch()
        if self.first_letter:
            self.first_letter = False
            self.time_info.start_test()

        if key == ord(' '):
            if self.sentence[self.position] == ESPACE:
                self.position += 1
                if len(self.past_letter) != self.position:
                    self.past_letter.append(True)
                    self.time_info.end_letter()
                    self.time_info.start_letter()

                
        elif chr(key) == self.sentence[self.position]:  # Check for correct character
            self.position += 1
            if len(self.past_letter) != self.position:
                self.past_letter.append(True)
                self.time_info.end_letter()
                
                if self.position < len(self.sentence):
                    self.time_info.start_letter()

        elif key == 27:
            self.run = False
            # self.position = 0
            # self.past_letter.clear()
            
            # self.first_letter = True
        else:
            if len(self.past_letter) == self.position:
                self.past_letter.append(False)
    
    def loop(self):
        self.first_letter = True
        self.run = True
        while self.run:
            self.print()                
                    
            self.kyboard()

            if self.position >= len(self.sentence):
                self.time_info.end_test()
                break

    def __del__(self):
        self.stdscr.erase()
        
try:
    ky = kyboard()
    print(ky.time_info.get_wpm_word())
except Exception as e:
    print(e)
    
# TODO
# [ ] : faire un truc qui défile sur le coté tout seul quand on écrit
# [ ] : emepche les mots de se couper 