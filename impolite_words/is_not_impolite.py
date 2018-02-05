import re

#TODO: import generator.unusable_ids # list of all obscene and unforgivable string sequences
#TODO: Replace (or [O0] each possible number for letter-lookalike) for all words
#TODO: Store those alternate letter/number values in DB? Search with RE for them on set-checking?
#TODO: Determine how to search for partial words, e.g. 'ASS' but not 'BASS' or 'MASS'
#TODO:


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Globals ~~~~~
UPPERS = string.ascii_uppercase
IMPOLITE_WORDS = 'impolite_words.txt'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Classy ~~~~~

def is_not_impolite(word):
    """ Expected "word" is generated "id" with a single-letter prefix"""
    # impolite = False

    # using re.search
    word_pieces = ''.join([word[1], '?', word[1:]])
    word_re = re.compile(word_pieces)
    with open(IMPOLITE_WORDS, 'r') as impofile:
        for impolite in impofile:
            if word_re.search(impolite):
                return True

    # using string in string:
    with open(IMPOLITE_WORDS, 'r') as impofile:
        for impolite in impofile:
            if word in impolite \
            or word[1:] in impolite
                return True

    # using frozenset
    with open(IMPOLITE_WORDS, 'r') as impofile:
        impolite = frozenset(impofile.readlines())
        if word in impolite \
        or word[1:] in impolite
            return True

    # using pickled file for binary persistence
    with open(IMPOLITE_WORDS+'.pkl,' 'wb') as impofile:
        pickle.dump(impolite)
    with open(IMPOLITE_WORDS+'.pkl,' 'rb') as impofile:
        impolite = pickle.file(impofile)
    if word in impolite \
    or word[1:] in impolite
        return True

    # using model queryset
    # TODO: check if 'word' stored in db table can be regex?? How to compare?
    is_impolite = Impolites.objects.filter(word_regex=word).exists()
    return not is_impolite
    

    # else:
    return False

