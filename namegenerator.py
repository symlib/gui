
def random_key(length):
    import random
    import string
    key = ''
    for i in range(length):
        key += random.choice(string.lowercase + string.uppercase + string.digits+"_")
        #key += random.choice(string.lowercase + string.digits)
    return key