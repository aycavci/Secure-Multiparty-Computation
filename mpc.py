import random


def generate_u_array(num_clients, sensitive_value):

    # Array initialization for distinct u values (shares).
    u_array = []

    for i in range(0, num_clients-1):
        # Generate random integer between 0 and sensitive value
        u = random.randint(0, sensitive_value)
        # If the u_array consists generated number, while generating different number from the list
        # keep generating random number.
        if u_array.count(u) != 0:
            while u_array.count(u) == 0:
                u = random.randint(0, sensitive_value)
        # Append u value to the array.
        u_array.append(u)
        # Subtract randomly generated number from sensitive value to reduce the probability of
        # generation of same number.
        sensitive_value -= u

    # At the end, for last u value for the last client will be updated sensitive value. But, we need to
    # check whether there is a duplicate before putting it to the array. If there is a duplicate, find the index of the
    # duplicates in the array and replace their values with another value which is not in the array previously.
    if u_array.count(sensitive_value) != 0:
        index_array = []
        u_array.append(sensitive_value)
        for index, u_number in enumerate(u_array):
            if u_number == sensitive_value:
                index_array.append(index)
        while u_array.count(u_array[index_array[0]]) == 1 and u_array.count(u_array[index_array[1]]) == 1:
            x = random.randint(0, u_array[index_array[0]])
            u_array[index_array[0]] += x
            u_array[index_array[1]] -= x
    # If sensitive value is not in the array already, just append it to the list.
    else:
        u_array.append(sensitive_value)

    return u_array


def generate_random_number():
    return random.randint(0, 100)
