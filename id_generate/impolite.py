
IMPOLITE_WORDS = 'impolite_words.txt'

def id_is_impolite(self, id):
    with open(IMPOLITE_WORDS, 'r') as imp:
        if re.match(imp.readline(), id):
            return True

