#! /usr/bin/env python3
import os, sys, time, re
from os.path import isfile, join
prompt = "$ "

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
    def pipe(untokenized):
        left = untokenized[0:untokenized.index("|")] #saves everything before |
        right = untokenized[len(left)+1:] # saves everything after |
        pr, pw = os.pipe() # saving tuple of read and write

        rc = os.fork() # creates a child process
        if rc < 0: #if it returns a 0 the fork failed
            os.write(2, ("Forking has failed!!!! Sorry! %d\n" %rc).encode())
            sys.exit(1) # exits
            
        elif rc == 0: #if a zero is returned, it means it's good to go
            os.close(4) #close file descriptor 4
            os.dup(pw) #copies fd of child and saved into pw
            os.set_inheritable(4, True) #inheritable is set to true

            # closing all fd
            for fd in (pr, pw):
                os.close(fd) 

            # tokenizing command so I can execute them
            tokenized_command = tokenize(left)
            comm(tokenized_command) #inputs the left argument into commands
        else:
            os.close(3) #closes file descriptor 3
            os.dup(pr) #copies fd of child
            os.set_inheritable(3, True)

            #close both pw and pr
            for fd in (pw, pr):
                os.close(fd)

            #if another pipe is found, it will pipe again
            if "|" in right:
                pipe(right)
            tokenized_right = tokenize(right)
            comm(tokenized_right) #inputs the right argument into commands

    # ---- checks what command was entered ----
    def comm(command):
        if len(command) == 0: return #done if nothing read

        #--------- PIPE -----------
        if "|" in command:
            pipe(copied_command)

        #---------GOES INTO -------
        elif command[0] == ">":
            into(command)

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
            return
        #--------- CD ------------
        elif command[0] == "cd":
            cd(command)
        #--------- CWD ------------
        elif command[0] == "cwd":
            getcwd()
            
        else:
            print("Command: entered not recognized.")
    
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

    # ---- > ------
    def into(command):
        os.close(1) #redirect child's stdout
        os.open(command[1], os.O_CREAT | os.O_WRONLY);
        os.set_inheritable(1, True)
        listoffiles = os.listdir('.')
    
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
        copied_command = command # saved a copy of original command entered by user
        command = tokenize(command)
        
        #--------- CHECKS LENGTH OF INPUT -------
        if len(command) == 0: break #done if nothing read
        #--------- EXIT ----------
        elif command[0] == "exit": #My shell terminates
            print('Terminating MyShell...')
            print('Successfully terminated. Thank you for choosing MyShell.')
            break
        #--------- NOT RECOGNIZED -----
        else:
            comm(command)
            
    
else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())

