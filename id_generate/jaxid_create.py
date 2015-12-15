from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from .models import JAXIdDetail

import string
import random

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
    # def __init__(self, id_model, column='jaxid', prefix='J'):
    def __init__(self, prefix='J'):
        # id_model = exec()
        # if not isinstance(id_model, Model):
            # print("Model '{}' does not have column {}? Does not exist!".format(
                    # id_model, column))
        # else:
            self.id_model = JAXIdDetail
            # self.column = column
            self.prefix = prefix
            self.rand_size = 5

    def generate(self):
        """Use id_generator and add preceding 'J' character for the
            6 characater JAXid or 'B' for BoxID or 'P' for PlateID
        """
        ID = ''.join([self.prefix, RandomID().generate(size=self.rand_size)])
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

