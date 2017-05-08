
def random_key(length):
    import random
    import string
    key = ''
    for i in range(length):
        key += random.choice(string.lowercase + string.uppercase + string.digits+"_")
        #key += random.choice(string.lowercase + string.digits)
    return key

#!/usr/bin/env python
# -*- coding: utf-8 -*-


from itertools import islice
import random

import string
# top-level domains
TLDS = ('com net org mil edu de biz de ch at ru de tv com st br fr de nl dk ar jp eu it es com us ca pl').split()

def gen_name(length):
    """Generate a random name with the given number of characters."""
    return ''.join(random.choice(string.lowercase + string.uppercase + string.digits+"_"+"."+"-") for _ in xrange(length))

def address_generator():
    """Generate fake e-mail addresses."""
    # while True:
    user = gen_name(random.randint(3, 15))
    host = gen_name(random.randint(4, 15))
    return '%s@%s.%s' % (user, host, random.choice(TLDS))