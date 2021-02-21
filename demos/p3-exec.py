#! /usr/bin/env python3
import os, sys, time, re
from os.path import isfile, join
prompt = "$ "

pid = os.getpid() # setting the pid

os.write(1, ("About to fork (pid:%d)\n" % pid).encode()) # forks

rc = os.fork() # forks 

# handler if forking execution failed
if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

# if the forking was successful, it outputs both child's and parent's pid
elif rc == 0:                   # child
    # ---- lists files in CWD ----
    def list_files():
        listoffiles = os.listdir('.')
        for file in listoffiles:
            print(" ",file)
        return
    # ---- prints CWD -----
    def getcwd():
        print(" ",os.getcwd())
        
    # ---- reads user input ----
    def readLine():
        comm = input()
        return comm

    # ---- change directory ----
    def cd(command):
        new_dir = command[1]
            
        if command[1] == "..":
                os.chdir("..")
            
        else:
            try:
                os.chdir(new_dir)
            except OSError:
                print("")
                print("Can't change the Current Working Directory, dir does not exist!!!!")
                    
        getcwd()
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
        
        #--------- CD ------------
        elif tokenized_string[0] == "cd":
            cd(tokenized_string)
        #--------- CWD ------------
        elif tokenized_string[0] == "cwd":
            getcwd()
            
        else:
            print("Command: entered not recognized.")
            return
            

    #----------------------------------------------------------------------------------
    # will tokenize the command entered and the first word will be "ls", which will list
    #    all possible files
    def tokenize(command):
        tokenized_string = command.split()
        return tokenized_string
    #----------------------------------------------------------------------------------
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())
    #----------------------------------------------------------------------------------
    while 1:
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, prompt.encode())
            
        command = readLine()
        command = tokenize(command)

        #--------- CHECKS LENGTH OF INPUT -------
        if len(command) == 0: break #done if nothing read
        
        #--------- LS -------------
        if command[0] == 'ls':
            if len(command) > 1:
                print("ls: No such file or directory, command not recognized.")
            list_files()

        #--------- EXIT ----------
        elif command[0] == "exit": #My shell terminates
            print('Terminating MyShell...')
            print('Successfully terminated. Thank you for choosing MyShell.')
            break
        #--------- CD ------------
        elif command[0] == "cd":
            cd(command)
        #--------- CWD ------------
        elif command[0] == "cwd":
            getcwd()
            
        else:
            print("Command: entered not recognized.")
            
    
else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
