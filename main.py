import curses
from time import perf_counter
import random
from collections import defaultdict

class database:
    def __init__(self):
        self.load_word()
        self.count_most_use_letter()

    def load_word(self):
        with open ('frequency.txt', 'r', encoding='utf8') as file:
            self.words = file.read().splitlines()
    
    def count_most_use_letter(self):
        letter_count = defaultdict(int)

        for word in self.words:
            for letter in word:
                letter_count[letter] += 1

        
        self.most_frequent_letter = list(dict(sorted(letter_count.items(), key=lambda item: item[1], reverse=True)))
    
    def get_word(self, letters : list, nbr_word : int) -> list:
        letters_set = set(letters)

        mots_trouves = [mot for mot in self.words if set(mot).issubset(letters_set)]
        
        return random.sample(mots_trouves, min(nbr_word, len(mots_trouves)))
        
class kyboard:
    def __init__(self):
        self.position = 0
        
        self.past_letter = []
            
        self.db = database()
        
        self.setting = {'nbr_word' : 3, 'nbr_letter' : 10}
        self.sentence = self.db.get_word(self.db.most_frequent_letter[:self.setting['nbr_letter']], self.setting['nbr_word'])
        self.sentence = "•".join(self.sentence)
        
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
    
    def print(self):
        self.stdscr.clear()
        # Display
        for i in range(len(self.sentence[:self.position])):
            self.stdscr.addstr(0, i, self.sentence[i], curses.color_pair(3) if self.past_letter[i] else curses.color_pair(1))
        self.stdscr.addstr(0, self.position, self.sentence[self.position], curses.color_pair(2))
        self.stdscr.addstr(0, self.position + 1, self.sentence[self.position + 1:])
        self.stdscr.refresh()
    
    def kyboard(self):
        key = self.stdscr.getch()
        if self.first_letter:
            self.first_letter = False

        if key == ord(' '):
            if self.sentence[self.position] == '•':
                self.position += 1
                if len(self.past_letter) != self.position:
                    self.past_letter.append(True)

                
        elif chr(key) == self.sentence[self.position]:  # Check for correct character
            self.position += 1
            if len(self.past_letter) != self.position:
                self.past_letter.append(True)

        elif key == 27:
            self.position = 0
            self.past_letter.clear()
            self.first_letter = True
        else:
            if len(self.past_letter) == self.position:
                self.past_letter.append(False)
    
    def loop(self):
        self.first_letter = True
        while True:
            self.print()                
                    
            self.kyboard()

            if self.position >= len(self.sentence):
                break


        self.stdscr.erase()

kyboard()