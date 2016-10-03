import os
import hashlib


def md5(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        digest.update(f.read())
    return digest.hexdigest()

startpath = input()
d = {}
for path in os.walk(startpath):
    for file in path[2]:
        file_path = path[0] + '\\' + file
        if file[0] != '.' and file[0] != '~':
            hash_file = md5(file_path)
            if d.get(hash_file):
                d[hash_file].extend([file])
            else:
                d[hash_file] = [file]

for key in d:
    if len(d[key]) > 1:
        print(*d[key], sep=':')
