#! /usr/bin/env python3

import os, sys, re

#need:
#str = myReadline()

# my_getchar should call os.read()
def my_getchar():
    print("Hello from my_getchar()")

    #can cal my_getchar()
def my_getline():
    print("Hello from my_getline()")


print("-----Hello from reader.py-----")
while 1:
    print("Taking user input: ");
    user_input = input("Enter your value: ")
    print("Your input: ", user_input)
    
