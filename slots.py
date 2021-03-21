"""
Testing the memory usage of a simple class with/without __slots__. 
To test: run python -m memory_profiler slots.py 

My output: Notice slots uses 1/4 as much memory. 

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    22     39.3 MiB     39.3 MiB           1   @profile
    23                                         def people():
    24     55.5 MiB     16.3 MiB      100003       ps = [Person("Warren", "Alphonso") for _ in range(100000)]
    25     55.5 MiB      0.0 MiB           1       return ps


Filename: slots.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    28     41.0 MiB     41.0 MiB           1   @profile
    29                                         def people_slots():
    30     45.5 MiB      4.4 MiB      100003       ps = [PersonSlots("Warren", "Alphonso") for _ in range(100000)]
    31     45.5 MiB      0.0 MiB           1       return ps
"""
from memory_profiler import profile


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class PersonSlots:
    __slots__ = 'first_name', 'last_name'

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


@profile
def people():
    ps = [Person("Warren", "Alphonso") for _ in range(100000)]
    return ps


@profile
def people_slots():
    ps = [PersonSlots("Warren", "Alphonso") for _ in range(100000)]
    return ps


if __name__ == '__main__':
    people()
    people_slots()
