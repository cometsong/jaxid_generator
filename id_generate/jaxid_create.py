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
    def __init__(self, id_model, column='jaxid', prefix='J'):
        # id_model = exec()
        # if not isinstance(id_model, Model):
            # print("Model '{}' does not have column {}? Does not exist!".format(
                    # id_model, column))
        # else:
            self.id_model = JAXIdDetail
            self.column = column
            self.prefix = prefix
            self.rand_size = 5

    def generate(self):
        """Use id_generator and add preceding 'J' character for the
            6 characater JAXid or 'B' for BoxID or 'P' for PlateID
        """
        ID = ''.join([self.prefix, RandomID().generate(size=self.rand_size)])
        if self.id_does_not_exist(ID):
            return ID
        else:
            self.generate()

    def id_does_not_exist(self, id):
        if self.id_exists(id):
            return false
        else:
            return True

    def id_exists(self, id):
        try:
            e = self.id_model.objects.get(id)
            return True
        except ObjectDoesNotExist as err:
            return err

    def ids_exist(self, ids):
        id_list = []
        try:
            for id in ids:
                id_list.append(id)
            e = self.id_model.objects.get_queryset(id_list)
            return e
        except Error as err:
            return err # TODO: return error message!

    def create_id_records(self, ids):
        id_list = []
        try:
            for id in ids:
                id_list.append(id)
            e = self.id_model.objects.bulk_create(id_list)
            return e
        except Error as err:
            return err # TODO: return error message!

