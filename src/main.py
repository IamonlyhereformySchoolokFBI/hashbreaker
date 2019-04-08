# - *- coding: utf-8 - *-
import sys
import hashlib

from Process_farm import *
from Hashbreaker import *

ptp = Process_farm()
hbr = Hashbreaker(2)

granulation = 8

hash_to_crack = hbr.create_hash_from_str(hashlib.md5,'bob')
res = ptp.run(hash_to_crack, hashlib.md5, hbr.crack_hash_from_range, hbr.get_number_of_combinations(3), granulation)
print(res)
