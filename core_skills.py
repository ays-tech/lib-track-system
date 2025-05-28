import random

rand_list = [random.randint(1,20) for x in range(20)]


list_comprehension_below_10 = [x for x in rand_list if x < 10]

list_comprehension_below_10 = rand_list.flter()