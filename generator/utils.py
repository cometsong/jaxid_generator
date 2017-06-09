import operator

def tuple_index_elements(theset, elemnum=1):
    """gets tuple of each element(default=1)
        within nested list/tuple/etc of lists/tuples
    """
    get = operator.getitem
    return tuple([get(get(theset,each),elemnum)
            for each in range(theset.__len__())])

