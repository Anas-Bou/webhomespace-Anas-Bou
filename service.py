import os 
from passlib.hash import sha512_crypt
from passlib.apps import custom_app_context as pwd_context
import spwd
import subprocess
import crypt


class WebService:
    def __init__(self) -> None:
        pass
    def loggin(self,user:str,password:str):
        output = subprocess.check_output(f'cat /etc/shadow | grep "{user}"', shell=True, universal_newlines=True).split(':')[1]
        hash=crypt.crypt(password, output)
        if hash == output:
            return True
        else:
            return "Please Check your informations"
    def homepage(self,user:str):
        home_dir = os.path.expanduser("~" + user)
        files = os.listdir(home_dir)
        return files
    
    def getuser(self,user:str):
        return os.path.expanduser("~" + user)
    
    def file_nbr(self,user:str):
        nbr=subprocess.check_output(f'find /home/{user} -type f | wc -l',shell=True,universal_newlines=True)
        return nbr
    def stockage(self,user:str):
        space=subprocess.check_output(f'du -sh /home/{user}',shell=True,universal_newlines=True)
        return space
    def dir_nbr(self,user:str):
        dirs=subprocess.check_output(f'find /home/{user} -type d | wc -l',shell=True,universal_newlines=True)
        return dirs
    def create_zip_archive(self,user:str):
        home_dir = f"/home/{user}"
        zip_filename = f"{user}_home.zip"
        downloads=subprocess.run(["zip", "-r", zip_filename, home_dir])
        return downloads