from django.core.exceptions import ObjectDoesNotExist
from .models import JaxIdMasterList

def id_exists(id):
    try:
        e = JaxIdMasterList.objects.get(jaxid=id)
        return True
    except ObjectDoesNotExist:
        return False

def ids_exist(ids):
    id_list = []
    try:
        for id in ids:
            id_list.append()
        e = JaxIdMasterList.objects.bulk_create(id_list)
        return e
    except Error:
        return False # TODO: return error message!

def create_id_record(id):
    try:
        e = JaxIdMasterList.objects.create(jaxid=id)
        return e
    except Error:
        return False # TODO: return error message!

def create_id_records(ids):
    id_list = []
    try:
        for id in ids:
            id_list.append(JaxIdMasterList(jaxid=id))
        e = JaxIdMasterList.objects.bulk_create(id_list)
        return e
    except Error:
        return False # TODO: return error message!

