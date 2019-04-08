# - *- coding: utf-8 - *-
import sys
import hashlib

from charset import *

class Hashbreaker:

    def __init__(self, number):
        self.dict = self.create_dictionary(number)
        self.base = len(self.dict)

    def crack_hash(self, hash_to_crack ,rest_array, hash_method):
        result = []
        plain_word = self.create_keyword(rest_array)
        hash_word = hash_method(plain_word.encode()).hexdigest()
        
        if hash_word == hash_to_crack:
            result.append(plain_word)
            result.append(hash_word)
            return result

        result.append(0)
        return result

    def crack_hash_from_range(self, hash_to_crack, first_number, scope, hash_method):
        for number in range(first_number, first_number + scope):
            digits = self.how_many_digit(number)
            rest_array = self.create_rest_array(number, digits)
            result = self.crack_hash(hash_to_crack, rest_array, hash_method)

            # notice that always rest_array will have 1 on the end(beginning coz its reversed )
            # so we never gets [0][0][0] word, this section force it
            if rest_array[0] == 1 and len(result) == 1:
                rest_array[0] -= 1
                result = self.crack_hash(hash_to_crack, rest_array, hash_method)
            if len(result) == 2:
                    return result
    
        return result

    @staticmethod
    def create_dictionary(number):  # 1 2 4 8 16 32
        dictionary = []
        binary = bin(number)
        binary = list(reversed(binary))
        for i in range(0, len(binary) - 2):
            if binary[i] is '1':
                dictionary += full_dict[i]

        return dictionary

    def get_number_of_combinations(self, number_of_letters):
        number_of_combinations = 0
        
        for i in range(1, number_of_letters + 1):
            number_of_combinations += self.base**i  

        return number_of_combinations

    def how_many_digit(self,tmp_number):
        digit = 1

        while True:
            if (self.base**digit) <= tmp_number:
                digit += 1
            else:
                break
        return digit

    def create_rest_array(self, tmp_number, n_times):
        tab = []

        for i in range(n_times):
            tab.append(tmp_number % self.base)
            tmp_number = tmp_number // self.base

        tab = list(reversed(tab))

        return tab 

    def create_keyword(self, rest_array):
        tab = []
        for i in range(len(rest_array)):
            tab.append(self.dict[rest_array[i]])
        tab = "".join(tab)
        return tab

    @staticmethod
    def create_hash_from_str(hash_method, str):
        str = hash_method(str.encode()).hexdigest()

        return str
