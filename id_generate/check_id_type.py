import re

def check_id_type(row_dict):
    """Determine which type of id this record holds.
    Varying on specific field values and lack thereof.
    Results: 'specimen', 'extraction', 'library', 'pool', 'Invalid'
    """
    parent = row_dict['parent_jaxid']
    sample = row_dict['sample_type']
    nucleic = row_dict['nucleic_acid_type']
    seqtype = row_dict['sequencing_type']

    ic = re.IGNORECASE
    pool = re.compile('pool', flags=ic)
    zero = re.compile('^Z$')

    if pool.match(parent):
        return 'pool'
    elif zero.match(sample) and zero.match(nucleic) and zero.match(seqtype):
        return 'Invalid!'
    elif zero.match(nucleic) and zero.match(seqtype):
        return 'specimen'
    elif zero.match(seqtype):
        return 'extraction'
    else: # none == 'Z'
        return 'library'

