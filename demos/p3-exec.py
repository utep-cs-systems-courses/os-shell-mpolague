#! /usr/bin/env python3
import os, sys, time, re
from os.path import isfile, join

pid = os.getpid() # setting the pid

os.write(1, ("About to fork (pid:%d)\n" % pid).encode()) # forks

rc = os.fork() # forks 

# handler if forking execution failed
if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

# if the forking was successful, it outputs both child's and parent's pid
elif rc == 0:                   # child
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())
    args = ["wc", "p3-exec.py"]
    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

    os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
#---------------------------------------------------------------------
#---------------------------------------------------------------------
print("Terminated p3-exec.py")
print("My part: ")

def list_files():
    files = os.listdir()
    print(files)

# will tokenize the command entered and the first word will be "ls", which will list
#    all possible files
def tokenize(command):
    tokenized_string = command.split()
    print(tokenized_string)

    if tokenized_string[0] == 'ls':
        list_files()

command = input("Please enter the command: \n$ ")
tokenize(command)
