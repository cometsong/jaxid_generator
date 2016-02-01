from django.core.exceptions import ObjectDoesNotExist
from .models import JAXIdDetail

import string
import random
import re
from itertools import product


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Globals ~~~~~
DIGITS = string.digits
UPPERS = string.ascii_uppercase
ALPHADIGITS = DIGITS + UPPERS

# Defaults
ID_LENGTH = 5
ID_MODEL = JAXIdDetail
ID_FIELD = 'jaxid'
ID_CONTROLS = [ 'XC000', 'PC000', 'NC000' ]
# ID_CONTROLS.__iter__

NUMERIC_RE = ''.join(['\\d' for num in range(ID_LENGTH)])
MAX_NUM_ID = ''.join([ '9'  for num in range(ID_LENGTH)])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Classy ~~~~~

class RandomID(object):
    """RandomID generates a string of random alphanumeric chars"""
    def __init__(self):
        self.size = 10

    def generate(self, size=0, chars=string.ascii_uppercase + string.digits):
        """Generate random string of 'size' chars"""
        if size < 1:
            size = self.size
        return ''.join(random.choice(chars) for _ in range(size))


class JAXidGenerate(object):
    def __init__(self, prefix='J', amount=10):
        self.prefix = prefix
        self.amount = amount
        self.id_model = ID_MODEL
        self.id_length = ID_LENGTH
        self.ids_used = self.get_all_ids_used()
        self.new_id_list = []

    def generate_random(self):
        """Use id generator and add preceding 'J' character for the
            6 characater JAXid or 'B' for BoxID or 'P' for PlateID
        """
        ID = ''.join([self.prefix, RandomID().generate(size=self.id_length)])
        if self.id_exists(ID):
            return self.generate_random()
        else:
            return ID

    def id_is_control(self, id):
        return id in ID_CONTROLS.__iter__()

    def id_is_numeric(self, id):
        return re.match(NUMERIC_RE, id)

    def id_exists(self, id):
        try:
            e = self.id_model.objects.get(jaxid=id)
            return True
        except ObjectDoesNotExist as err:
            return False

    def get_all_ids_used(self):
        # NOTE: .values() returns a QuerySet, a list of dicts;
        #       then get elem['jaxid']
        #       then append [1:] to remove Prefix letter on each ID
        return [ d['jaxid'][1:]
                for d in ID_MODEL.objects.values('jaxid')
                if not self.id_is_control(d['jaxid'][1:]) ]

    def get_max_id_used(self):
        ids = list(self.get_all_ids_used())
        try:
            max_id = max(ids)
        except ValueError:
            min_id = ''.join(['0' for num in range(ID_LENGTH)])
            max_id = min_id
        return max_id

    def get_max_alpha_id_used(self):
        ids = self.get_all_ids_used()
        try:
            max_id = max( [id for id in ids.__iter__()
                if re.search("[A-Z]",id[1:])
                and id not in ID_CONTROLS] )
        except ValueError:
            max_id = ''.join(['0' for num in range(ID_LENGTH-1)])+'9'
            # max_id = ''.join([self.prefix,min_id])
        return max_id

    def new_id_num(self, minimum):
        seq_chars = DIGITS
        id_len = self.id_length
        for id in (''.join(i) for i in product(seq_chars, repeat=id_len)
                if not self.id_is_control(''.join(i))
                and ''.join(i) > minimum ):
            yield id

    def new_id_alphanum(self, minimum):
        seq_chars = ALPHADIGITS
        id_len = self.id_length
        for id in (''.join(i) for i in product(seq_chars, repeat=id_len)
                if not self.id_is_numeric(''.join(i))
                and not self.id_is_control(''.join(i))
                and ''.join(i) > minimum ):
            yield id

    def generate_new_ids(self, amount=0):
        print('Starting generate_new_ids()')
        new_id_list = self.new_id_list
        pre = self.prefix
        amt = amount if amount else self.amount

        try: # is MAX_NUM_ID passed in from previous iteration?
            max_num_in_list = self.new_id_list[-1]
            if self.new_id_list[-1] == self.prefix+MAX_NUM_ID:
                max_num_in_list = True
        except:
            max_num_in_list = False

        try:
            if self.id_exists(self.prefix+MAX_NUM_ID) \
                    or max_num_in_list:
                minimum = self.get_max_alpha_id_used()
                new_id = self.new_id_alphanum(minimum)
            else:
                minimum = self.get_max_id_used()
                new_id = self.new_id_num(minimum)

            for x in range(amt):
                new_id_next = new_id.__next__()
                new_id_seq = ''.join([pre,new_id_next])
                new_id_list.append(new_id_seq)

                # check reached MAX_NUM_ID during generation:
                if new_id_seq == self.prefix+MAX_NUM_ID:
                    # minimum = self.get_max_alpha_id_used()
                    # new_id = self.new_id_alphanum(minimum)
                    self.new_id_list = new_id_list
                    self.generate_new_ids(amount=amt-x)

        except StopIteration:
            pass
        return new_id_list

