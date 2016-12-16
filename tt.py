#!/usr/bin/python

import re
def fun(a):
    a = 2

def mul():
    return [lambda x : i*x for i in range(4)]
print [m(2) for m in mul()]

print re.findall("foo.$","foo1\nfoo2\n")
a = 1
fun(2)
print a
