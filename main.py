import curses
from time import time, sleep
import random
from collections import defaultdict, Counter
from load_data import LoadData
from dataclasses import dataclass

ESPACE = '•'

class PrepareData:
    def __init__(self, words):
        self.words = words
        self.count_most_use_letter()

    def count_most_use_letter(self):
        temp = Counter(''.join(self.words))        
        self._most_frequent_letter = [letter for letter, _ in temp.most_common()]
    
    def get_word(self, nbr_letters : int, nbr_word : int) -> list:
        letters_set = set(self._most_frequent_letter[:nbr_letters])

        mots_trouves = [mot for mot in self.words if all(letter in letters_set for letter in mot)]
        
        return random.sample(mots_trouves, min(nbr_word, len(mots_trouves)))

@dataclass
class CollectData:
    time_session = None
    time_by_letter = []
    who_is_false = []
    
    buffer_false_letter = []
    
    letter_time = None
        
    def start_letter(self):
        self.letter_time = time()
    
    def end_letter(self):
        self.time_by_letter.append(time() - self.letter_time)
        self.who_is_false.append(self.buffer_false_letter.copy())
        self.buffer_false_letter.clear()
        self.letter_time = time()
        
    def add_buffer(self, letter : str):
        self.buffer_false_letter.append(letter)
    
    def start_test(self):
        self.reset()
        self.time_session = time()
        self.start_letter()
    
    def end_test(self):
        self.time_session = time() - self.time_session
        self.time_by_letter.pop(0)
    
    def reset(self):
        self.__init__()
    
    def get_data(self):
        return self.time_session, self.time_by_letter, self.who_is_false
    
class Keyboard:
    def __init__(self):
        self.position = 0
        
        self.past_letter = []
        
        self.setting = {'nbr_word' : 3, 'nbr_letter' : 15}
        self.sentence = PrepareData(LoadData().data).get_word(self.setting['nbr_letter'], self.setting['nbr_word'])
        self.sentence = "•".join(self.sentence)
        
        self.collect_data = CollectData()
        
        self.init_screen()
        self.loop()
                    
    def init_screen(self):    
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # error typed text
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Current character
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # good typed text

    def print_classique(self):
        height, width = self.stdscr.getmaxyx()
        rang, col, i = 0, 0, 0
        
        def print_char(letter):
            color = curses.color_pair(3)
            if i < len(self.past_letter):
                color = curses.color_pair(3) if self.past_letter[i] else curses.color_pair(1)
            if i == self.position:
                color = curses.color_pair(2)
            self.stdscr.addstr(rang, col, letter, color)

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
    
    def print_move(self, _front_visibility, _back_visibility, start_col = 5): # print center        
        front_visibility = _front_visibility
        back_visibility = _back_visibility
        
        if _front_visibility == 'auto':
            height, width = self.stdscr.getmaxyx()
            front_visibility = int(width / 2)
            back_visibility = int(width / 2)
            start_col = 0
        
        
        min_index = max(self.position - back_visibility, 0)
        max_index = min(self.position + front_visibility - min(self.position - back_visibility, 0), len(self.sentence))
        col = start_col
        
        back = self.sentence[min_index:self.position]
        current = self.sentence[self.position]
        front = self.sentence[self.position + 1:max_index]
        sentence_show = back + current + front
                
        self.stdscr.clear()
        
        for i, letter in enumerate(sentence_show):
            color = curses.color_pair(3)
            if i + min_index  < len(self.past_letter):
                color = curses.color_pair(3) if self.past_letter[min_index + i] else curses.color_pair(1)
            
            if i + min_index == self.position:
                color = curses.color_pair(2)
            self.stdscr.addstr(2, col, letter, color)
        
            col += 1

        self.stdscr.refresh()
 
    def kyboard(self):
        key = self.stdscr.getch()
        if self.first_letter:
            self.first_letter = False
            self.collect_data.start_test()

        if key == ord(' '):
            if self.sentence[self.position] == ESPACE:
                self.position += 1
                if len(self.past_letter) != self.position:
                    self.past_letter.append(True)
                self.collect_data.end_letter()
                if self.position < len(self.sentence):
                    self.collect_data.start_letter()
            else:
                if len(self.past_letter) == self.position:
                    self.past_letter.append(False)
                self.collect_data.add_buffer(' ')

                
        elif chr(key) == self.sentence[self.position]:  # Check for correct character
            self.position += 1
            if len(self.past_letter) != self.position:
                self.past_letter.append(True)
            self.collect_data.end_letter()
        
            if self.position < len(self.sentence):
                self.collect_data.start_letter()

        elif key == 27:
            self.run = False
            # self.position = 0
            # self.past_letter.clear()
            
            # self.first_letter = True
        else:
            if len(self.past_letter) == self.position:
                self.past_letter.append(False)
            self.collect_data.add_buffer(chr(key))
        
    def loop(self):
        self.first_letter = True
        self.run = True
        while self.run:
            self.print_move(25, 10, 0) 
            self.kyboard()

            if self.position >= len(self.sentence):
                self.collect_data.end_test()
                break
        
t = Keyboard()

class Stat:
    def __init__(self, info : tuple , sentence): # (time_session, time_by_letter, who_is_false)
        self.time_session = info[0]
        self.time_by_letter = info[1]
        self.who_is_false = info[2]
        
        self.sentence = sentence
        
        self.clean_start()
    
    def clean_start(self):
        self.time_by_letter.pop(0)
    
    def get_wpm_word(self):
        return (len(self.sentence.split(ESPACE)) / (self.time_session / 60))
    
    def mean_wpm_letter(self):
        return sum(self.time_by_letter) / len(self.time_by_letter)
    
    def wpm_by_letter(self):
        unique_time_letter = {}
        for i in range(len(self.time_by_letter) - 1):
            # ajouter 1 quand on appelle sentene parce que on a pop(0)
            if self.sentence[i + 1] not in unique_time_letter:
                unique_time_letter[self.sentence[i + 1]] = [self.time_by_letter[i]]
            else:
                unique_time_letter[self.sentence[i + 1]].append(self.time_by_letter[i])
        
        self.mean_time_by_letter = {}
        for i in unique_time_letter:
            self.mean_time_by_letter[i] = sum(unique_time_letter[i]) / len(unique_time_letter[i])
        
        return (self.mean_time_by_letter)

    def count_all_error(self):
        return len(self.who_is_false) - self.who_is_false.count([])
    
    # rajouter quel lettre sont trompe et confondu avec lesquelle ?

stat = Stat(t.collect_data.get_data()[0], t.collect_data.get_data()[1], t.sentence)
print(t.collect_data.who_is_false)


# TODO
# [ ] add history value
# [ ] traiter les erreurs dans stat (total, pourcentage d'erreur par lettre)
# [ ] faire un affichage pour les stats