from hashlib import md5
key = b'iwrupvqb'
number = 0
while md5(key + str(number).encode('utf-8')).hexdigest()[:5] != '00000':
    number += 1
print('The first number that produces the sought hash is {}'.format(number))
while md5(key + str(number).encode('utf-8')).hexdigest()[:6] != '000000':
    number += 1
print('The first number that produces the next sought hash is {}'.format(number))
