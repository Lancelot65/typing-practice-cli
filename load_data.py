from json import load 
    
class load_data:
    PATH_DICT = {
    'english' : 'data/english_word.json',
    'frensh' : 'data/frensh_word.json',
    'spanish' : 'data/spanish_word.json'
    }
    
    def __init__(self, language = 'frensh') -> None:
        """
        Args:
            language (str, optional): change the language of words. Defaults to 'frensh'.
                option : english, frensh, spanish
        """
        self.language = language
        self._load()
    
    def _load(self) -> None:
        with open(self.PATH_DICT[self.language], 'r', encoding='utf-8') as file:
            self.data = load(file)[:5000]

    def get_data(self):
        return self.data