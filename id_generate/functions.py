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
