from math import *


def scalar_multiplication(scalar, vector):
    return tuple([scalar * x for x in vector])


def vector_addition(vector_1, vector_2):
    if len(vector_1) != len(vector_2):
        return None
    return tuple([vector_1[i] + vector_2[i] for i in range(0, len(vector_1))])


def magnitude_of(vector):
    return sqrt(sum([pow(x, 2) for x in vector]))


def sign_of(number):
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def logical_xor(bool_1, bool_2):
    return (bool_1 and not bool_2) or (not bool_1 and bool_2)
