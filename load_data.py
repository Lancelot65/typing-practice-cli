from json import load 
    
class LoadData:
    PATH_DICT = {
    'english' : 'data/english_word.json',
    'french' : 'data/french_word.json',
    'spanish' : 'data/spanish_word.json'
    }
    
    def __init__(self, language = 'french') -> None:
        """
        Args:
            language (str, optional): change the language of words. Defaults to 'frensh'.
                option : english, frensh, spanish
        """
        if language not in self.PATH_DICT:
            raise ValueError(f"Language '{language}' is not supported. Choose from {list(self.PATH_DICT.keys())}.")
        self.language = language
        self._load()
    
    def _load(self) -> None:
        try:
            with open(self.PATH_DICT[self.language], 'r', encoding='utf-8') as file:
                self.data = load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.PATH_DICT[self.language]}")
        except ValueError as e:
            raise ValueError(f"Error loading JSON: {e}")
        

    def get_data(self):
        return self.data