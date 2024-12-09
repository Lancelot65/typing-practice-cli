import curses
from time import perf_counter
import random


class database:
    def __init__(self):
        self.load_word()
        self.count_most_use_letter()

    def load_word(self):
        with open ('frequency.txt', 'r', encoding='utf8') as file:
            self.words = file.read().split('\n')
    
    def count_most_use_letter(self):
        letter_count = {}

        for word in self.words:
            for letter in word:
                if word in letter_count:
                    letter_count[letter] += 1
                else:
                    letter_count[letter] = 1
        
        self.most_frequent_letter = list(dict(sorted(letter_count.items(), key=lambda item: item[1], reverse=True)))
    
    def get_word(self, letters : list, nbr_word : int) -> list:
        lettres_set = set(letters)
        mots_trouves = []

        for mot in self.words:
            if set(mot).issubset(lettres_set):
                mots_trouves.append(mot)
        random.shuffle(mots_trouves)
        return mots_trouves[:nbr_word]
        
class kyboard:
    def __init__(self):
        self.new_space = '•'
        self.position = 0
        self.sentence = "voici•ma•phrase"
        
        self.past_letter = []
        self.time_letter_liste = []
    
        self.start_time = None
        self.time_letter = None       
        
        
        
        
        self.db = database()
        
        self.setting = {'nbr_word' : 30, 'nbr_letter' : 10}
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
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)  # good character
    
    def print(self):
        self.stdscr.clear()  # Clear the screen
        # Display the current state
        for i in range(len(self.sentence[:self.position])):
            self.stdscr.addstr(0, i, self.sentence[i], curses.color_pair(3) if self.past_letter[i] else curses.color_pair(1))  # Correctly typed
        self.stdscr.addstr(0, self.position, self.sentence[self.position], curses.color_pair(2))  # Current character
        self.stdscr.addstr(0, self.position + 1, self.sentence[self.position + 1:])  # Remaining characters
        self.stdscr.refresh()  # Refresh the screen to show changes
    
    def kyboard(self):
        key = self.stdscr.getch()
        if self.first_letter:
            self.start_time = perf_counter()
            self.time_letter = perf_counter()
            first_letter = False

        if key == ord(' '):
            if self.sentence[self.position] == '•':
                self.position += 1
                if len(self.past_letter) == self.position:
                    pass
                else:
                    self.past_letter.append(True)
                    self.time_letter_liste.append(perf_counter() - self.time_letter)
                    self.time_letter = perf_counter()
                
        elif chr(key) == self.sentence[self.position]:  # Check for correct character
            self.position += 1
            if len(self.past_letter) == self.position:
                pass
            else:
                self.past_letter.append(True)
                self.time_letter_liste.append(perf_counter() - self.time_letter)
                self.time_letter = perf_counter()
        elif key == 27:
            self.position = 0
            self.past_letter.clear()
            self.time_letter_liste.clear()
            self.first_letter = True
        else:
            self.past_letter.append(False)
    
    def loop(self):
        self.first_letter = True
        while True:
            self.print()
                    
            self.kyboard()

            if self.position >= len(self.sentence):
                break


        self.stdscr.erase()
        
        
# dt = database()

# dt.load_word()
# dt.count_most_use_letter()
# print(dt.get_word(dt.most_frequent_letter[:8], 100))

kyboard()