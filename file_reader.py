import msgpack

is_plasma: bool = False
shotn: int = 11111

path: str = '//192.168.10.41/d/data/db/'

if is_plasma:
    path += 'plasma/'
else:
    path += 'debug/'
path += 'ophir/%05d.msgpk' % shotn
with open(path, mode='rb') as file:
    data = msgpack.unpackb(file.read())
    pass

print('OK')
