from django.core.exceptions import ObjectDoesNotExist
from .models import JAXIdMasterList

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


def generate_JAX_id(prefix='J'):
    """Use id_generator and add preceding 'J' character for the 6 characater
        JAXid or 'B' for BoxID or 'P' for PlateID
    """
    id_size=5
    return ''.join([prefix, RandomID().generate(size=id_size)])



def id_exists(id):
    try:
        e = JAXIdMasterList.objects.get(jaxid=id)
        return True
    except ObjectDoesNotExist:
        return False

def ids_exist(ids):
    id_list = []
    try:
        for id in ids:
            id_list.append()
        e = JAXIdMasterList.objects.bulk_create(id_list)
        return e
    except Error:
        return False # TODO: return error message!

def create_id_record(id):
    try:
        e = JAXIdMasterList.objects.create(jaxid=id)
        return e
    except Error:
        return False # TODO: return error message!

def create_id_records(ids):
    id_list = []
    try:
        for id in ids:
            id_list.append(JAXIdMasterList(jaxid=id))
        e = JAXIdMasterList.objects.bulk_create(id_list)
        return e
    except Error:
        return False # TODO: return error message!

