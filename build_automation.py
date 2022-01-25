import os
import git
import datetime
try:
    #os.chdir("E://sample")
    os.chdir("//home//centos//RMG//python_angular")
    #print("Current Working Directory " , os.getcwd())
    repo = git.Repo()
    origin = repo.remote(name='origin')
    
    origin.pull()
    f = open("logfile.txt", "a")
    f.writelines("Git pull done @ {timepull}\n".format(timepull = datetime.datetime.now()))
    f.close()
except Exception as e:
    print(e)
    f = open("logfile.txt", "a")
    f.writelines("some error {error}\n".format(error = e))
    f.close()
