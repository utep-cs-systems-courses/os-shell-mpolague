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
# replacement = os.environ['PS1']

def list_files():
    files = os.listdir()
    for file in range(len(files)): # will iterate through all files encountered
        if file == 0:
            print('   ')
        else:
            print('   ',files[file])

#----------------------------------------------------------------------------------
# Helper to recognize if the command entered by the user is legal or illegal
# -- if returns 0 = keep askig for user input
# -- if returns 1 = exit program
def recognize_command(tokenized_string):
    # recognizes commands such as 'ls', 'cd', 'exit'
    if tokenized_string[0] == 'ls':
        if len(tokenized_string) > 1:
            print("ls: No such file or directory, command not recognized.")
            return
        list_files()
        return 0
        
    elif tokenized_string[0] == "exit": #My shell terminates
        return 1
    
#----------------------------------------------------------------------------------
# will tokenize the command entered and the first word will be "ls", which will list
#    all possible files
def tokenize(command):
    tokenized_string = command.split()
    return tokenized_string

#-------------------------------------------------------------------------------------        
# will continue to ask the user for input until user wants to exit the program.        
while 1:
    command = input("Please enter the command: \n$ ")
    tokenized_string = tokenize(command)
    was_recognized = recognize_command(tokenized_string)

    # user wants to exit program, program terminates
    if was_recognized == 1:
        print('Terminating MyShell...')
        print('Successfully terminated. Thank you for choosing MyShell.')
        break
