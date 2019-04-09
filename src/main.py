# - *- coding: utf-8 - *-
import sys
import hashlib

from Process_farm import *
from Hashbreaker import *
from Time import *

if __name__ == '__main__':
    try:
        trigger = sys.argv[1]
        string_pass = sys.argv[2]
        dict_number = int(sys.argv[3]) 
        granulation = int(sys.argv[4]) 
    except:
        print('Did something wrong!')
        exit()

    ptp = Process_farm()
    hbr = Hashbreaker(dict_number)
    time = Time()

    if trigger == '-word':
        hash_to_crack = hbr.create_hash_from_str(hashlib.md5, string_pass)
    else:
        hash_to_crack = string_pass
    password_length = 3
    time.start()
    res = ptp.run(hash_to_crack, hashlib.md5, hbr.crack_hash_from_range, hbr.get_number_of_combinations(password_length), granulation)

    time.stop()

    time_as_str =  '{0:8f}'.format(time.result)
    result_filename = ptp.save_to_file(granulation, time_as_str, res)

    if len(res) == 1:
        print('Do NOT found match password')
    else:
        print('Found password on host: \'' + res[2] + '\' with hash: ' + res[1] + '\n' + 'Your password is: ' + res[0])

    print('\n' + 'Time = ' + time_as_str + '[sec].')
    print('Result save into the file: ' + result_filename )
