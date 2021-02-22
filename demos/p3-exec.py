#! /usr/bin/env python3
import os, sys, time, re
from os.path import isfile, join
prompt = "$ "

inp = input("please enter something before proceeding")
print(inp)
print(os.pipe())


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

    # ---- PIPELINING -----
    def pipe():
        print(os.pipe())
    
    # ---- lists files in CWD ----
    def list_files(command):
        if len(command) == 3:
            if command[1] == '>':
                os.close(1) #redirect child's stdout
                os.open(command[2], os.O_CREAT | os.O_WRONLY);
                os.set_inheritable(1, True)
                listoffiles = os.listdir('.')
                for file in listoffiles:
                    print(" ",file)
                return
            else:
                print("ls: No such file or directory, command not recognized.")
                return
            
        elif len(command) == 1:
            listoffiles = os.listdir('.')
            for file in listoffiles:
                print(" ",file)

        
        else:
            print("ls: No such file or directory, command not recognized.")
            return
        return
    
    # ---- prints CWD -----
    def getcwd():
        print(" ",os.getcwd())
        
    # ---- reads user input ----
    def readLine():
        comm = input()
        return comm

    # ---- prints out contents of a file ----
    def cat():
        print(os.cat(test3.txt))

    #----- prints word count of a file ----
    def wc(command):
        file = command[1]
        print(os.system("wc " + file))
        
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
    # will tokenize the command entered and the first word will be "ls", which will list
    #    all possible files
    def tokenize(command):
        tokenized_string = command.split()
        return tokenized_string
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

        #--------- PIPE -----------
        if command[0] == "pipe":
            pipe()

        #--------- CAT ------------
        elif command[0] == "wc":
            wc(command)
        
        #--------- LS -------------
        elif command[0] == 'ls': 
            list_files(command)

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
