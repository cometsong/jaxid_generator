from django.core.exceptions import ObjectDoesNotExist
from .models import JAXIdDetail

import string
import random
import re
from itertools import product

#TODO: import generator.unusable_ids # list of all obscene and unforgivable string sequences
# [list comp ... if ['jaxid'][1:] not in unusable_ids.stringlist ]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Globals ~~~~~
DIGITS = string.digits
UPPERS = string.ascii_uppercase
ALPHADIGITS = DIGITS + UPPERS

# Defaults
ID_LENGTH = 5
ID_MODEL = JAXIdDetail
ID_FIELD = 'jaxid'
ID_CONTROLS = [ 'XC000', 'PC000', 'NC000' ]

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
    def __init__(self, prefix='J', amount=0):
        self.prefix = prefix
        self.amount = amount
        self.id_model = ID_MODEL
        self.id_length = ID_LENGTH
        self.new_id_list = []
        self.id_alphanum = False

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
        #       then slice [1:] to remove Prefix letter on each ID
        return [ d['jaxid'][1:]
                for d in ID_MODEL.objects.values('jaxid')
                if not self.id_is_control(d['jaxid'][1:]) ]

    def get_max_id_used(self):
        ids = self.get_all_ids_used()
        try:
            print(f'get_max_id_used begin; with alphanum: {self.id_alphanum}')
            if self.id_alphanum:
                id_is_type = lambda item: not self.id_is_numeric(item)
            else:
                id_is_type = lambda item: True
            # max_id = max( ids ) # = 99999
            max_id = max( [id for id in ids if id_is_type(id)] )
        except ValueError as ve:
            print('ERROR: ValueError in "get_max_id_used"! ' + str(ve))
            min_id = '0'*ID_LENGTH # if table Empty
            max_id = min_id
        print(f'get_max_id_used - max_id: {max_id}')
        return max_id

    def new_id_num(self, minimum=0):
        seq_chars = DIGITS
        id_len = self.id_length
        try:
            for id in (''.join(i) for i in product(seq_chars, repeat=id_len)
                    if not self.id_is_control(''.join(i))
                    and int(''.join(i)) > int(minimum) ):
                yield id
        except Exception as e:
            print('Exception!: '+e)

    def new_id_alphanum(self, minimum):
        """generate new alphanumeric id
           check it is: not numeric, not control, more than 'minimum'
           TODO: make checks faster!
        """
        seq_chars = ALPHADIGITS
        id_len = self.id_length
        for id in (''.join(i) for i in product(seq_chars, repeat=id_len)
                if not self.id_is_numeric(''.join(i))
                and not self.id_is_control(''.join(i))
                and ''.join(i) > minimum ):
            yield id

    def new_id_alphanum_TEST(self, minimum):
        """generate new alphanumeric id
           check it is: not numeric, not control, more than 'minimum'
           TODO: make checks faster!
        """
        seq_chars = ALPHADIGITS
        id_len = self.id_length
        for id in (''.join(i) for i in product(seq_chars, repeat=id_len)):
            if re.match('[A-Z]', id) and not self.id_is_control(id) and id > minimum :
                yield id

    def generate_new_ids(self, amount=0):
        print('Starting generate_new_ids()')
        prefix = self.prefix
        if amount:
            _amount = int(amount)
        else:
            _amount = int(self.amount)

        try:
            print('generate initial setup beginning')
            # MAX_NUM_ID preexisting or justcreated
            max_num_id_generated = False
            if len(self.new_id_list) > 0:
                max_id_in_list = self.new_id_list.sort[-1]
                if id_is_numeric(max_id_in_list) \
                        and max_id_in_list ==  prefix+MAX_NUM_ID:
                    max_num_id_generated = True
            # print(f'generate first max_num_id_generated: {max_num_id_generated}')

            if self.id_exists(prefix+MAX_NUM_ID) or max_num_id_generated:
                self.id_alphanum = True
                minimum = self.get_max_id_used()
                new_id = self.new_id_alphanum(minimum)
            else:
                self.id_alphanum = False
                minimum = self.get_max_id_used()
                new_id = self.new_id_num(minimum)
        except Exception as e:
            self.id_alphanum = False
            raise e

        try:
            print('generate for in amount')
            for x in range(_amount):
                new_id_seq = ''.join([prefix,next(new_id)])

                # check reached MAX_NUM_ID during generation:
                if new_id_seq == prefix+MAX_NUM_ID:
                    self.id_alphanum = True
                    self.generate_new_ids(amount=_amount-x)

                self.new_id_list.append(new_id_seq)
                yield new_id_seq

        except Exception as e:
            raise e

