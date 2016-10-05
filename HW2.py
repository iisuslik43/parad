import sys
import os
import hashlib
import collections


def md5(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        digest.update(f.read())
    return digest.hexdigest()

hash_to_files = collections.defaultdict(list)
for directory, _, files in os.walk(os.path.abspath(sys.argv[1])):
    for file in files:
        path_to_file = os.path.join(directory, file)
        if not file.startswith(('.', '~')) and not os.path.islink(path_to_file):
            hash_to_files[md5(path_to_file)].append(path_to_file)

for equal_files in hash_to_files.values():
    if len(equal_files) > 1:
        print(*equal_files, sep=':')
