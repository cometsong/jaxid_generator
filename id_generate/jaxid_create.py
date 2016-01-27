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

ID_LENGTH = 5
ID_MODEL = JAXIdDetail

# NOTE: .values() returns a QuerySet, a list of dicts; then get elem['jaxid']
ids_used = [d['jaxid'] for d in JAXIdDetail.objects.values('jaxid')]
MAX_ID_USED = max(ids_used)[1:] # [1:] to remove prefix letter


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
        self.id_found_highest_numeric = self.id_exists('99999')

    def new_id_num(self, minimum):
        seq_chars = DIGITS
        id_length = self.id_length
        for id in (''.join(i) for i in product(seq_chars, repeat=id_length)):
            yield id

    def new_id_alphanum(self, minimum):
        seq_chars = ALPHADIGITS
        id_length = self.id_length
        numeric_re = str(['\d' for num in range(id_length)])
        for id in (''.join(i) for i in product(seq_chars, repeat=id_length)
                    if not re.match(numeric_re, ''.join(i)) ):
            yield id

    def generate_random(self):
        """Use id generator and add preceding 'J' character for the
            6 characater JAXid or 'B' for BoxID or 'P' for PlateID
        """
        ID = ''.join([self.prefix, RandomID().generate(size=self.id_length)])
        if self.id_exists(ID):
            return self.generate()
        # if self.id_exists('JIT4T3'):
            # return 'foo'
        else:
            return ID

    def id_exists(self, id):
        try:
            e = self.id_model.objects.get(jaxid=id)
        except ObjectDoesNotExist as err:
            return False

    def generate_new_ids(self, prefix='J'):
        minimum=MAX_ID_USED
        new_id_list = []
        try:
            if self.id_found_highest_numeric:
                new_id = self.new_id_alphanum(minimum)
            else:
                new_id = self.new_id_num(minimum)

            for i in range(self.amount):
                new_id_seq = ''.join([prefix,new_id.__next__()])
                new_id_list.append(new_id_seq)
        except StopIteration:
            pass
        return new_id_list

