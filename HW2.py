import sys
import os
import hashlib
import collections


def md5(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        digest.update(f.read())
    return digest.hexdigest()

hash_to_file = collections.defaultdict(list)
for path, _, files in os.walk(sys.argv[1]):
    for file in files:
        file_path = os.path.join(path, file)
        if not file.startswith(('.', '~')) and not os.path.islink(file_path):
            hash_file = md5(file_path)
            hash_to_file[hash_file].append(file_path)

for value in hash_to_file.values():
    if len(value) > 1:
        print(*value, sep=':')
