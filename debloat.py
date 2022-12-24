#!/usr/bin/python3


import os
import time
import random
import urllib.request


R = '\033[1;31m' #red
G = '\033[1;32m' #green
C = '\033[1;36m' #cyan
Y = '\033[1;33m' #yellow

print('Checking network connection...')
def connection(host):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

if connection('http://google.com'):
    print('Connected..')
    time.sleep(0.7)
else:
    exit(print('Script cannot continue without an internet connection!'))




app_id = ''

def cls():
    os.system('clear')
def delay(duration):
    time.sleep(duration)

cls()

#check if adb is installed
try:
    adb_available = os.system('adb')
    exception = 'sh: 1: papslpasl: not found'
except exception:
    qwery = input('adb is not installed! Install adb? (y/n) ')
    condition = True
    while condition:
        if qwery == 'y':
            print('Installing adb..')
            os.system('sudo apt-get install adb')
            condition = False
        elif qwery == 'n':
            print('Cannot run script without Installing adb!')
            exit()


cls()
print()
print(f'{R}   Starting script...')
time.sleep(0.7)
cls()
print()
print(f'{R}   Loading adb...')
time.sleep(0.7)

def banner():
    print(C)
    ban = open('banner.txt','r')
    baner = ban.read()
    print(baner)
    ban.close()
    print(Y)

def fetch_id(alias):
    global app_id
    file = open("app_id.txt", 'w')
    file.write(str(alias))
    file.close()

    os.system('./fetch_id.sh')

    file = open('app_id.txt', 'r')
    app_id = file.read()
    
    app_id = app_id.split('=')
    app_id = app_id[1]

    app_id = app_id.split('"')
    app_id = app_id[0]

    return app_id
        
def he1p():
    print('''
    Help menu:

    script commands:
        help                -show help manu
        show                -shows connected devices
        connect [ip]        -connect to a device IP
        disconnect          -disconnect from a device
        shell               -open device shell
        shell_cmd           -print shell commands
        search*             -search an application -- in development
        backup*             -buckup an application -- in development
        apps                -list installed packages
        manual [app_id]     -manually uninstall an app
        uninstall [app_nme] -unistall an application
        clear               -clear the screen
        exit                -exit script''')

def manual_un(app_id):
    verify = input(f'Do you wish to uninstall? [{app_id}]: Y/n ')
    if verify == 'Y':
        os.system(f'adb shell pm uninstall -k --user 0 {app_id}')
    else:
        print('Operation cancelled!')


try:
    cls()
    delay(0.7)
    banner()
    while True:
        time.sleep(0.7)
        cmmd = input(f'{Y}\n[v2.0]>>> ')
        cmd = cmmd.split()

        if cmd[0] == 'help':
            he1p()

        elif cmd[0] == 'show':
            os.system('adb devices -l')

        elif cmd[0] == 'connect':
            os.system('adb start-server')
            name = input('Enter device IP: ')
            port = input('Enter device port: ')
            os.system(f'adb connect {name}:{port}')

        elif cmd[0] == 'apps':
            os.system('adb shell pm list packages')           

        elif cmd[0] == 'clear':
            cls()
            banner()

        elif cmd[0] == 'manual':
            manual_un(cmd[1])

        elif cmd[0] == 'shell':
            print(G)
            os.system('adb shell')
            print(R)        

        elif cmd[0] == 'shell_cmd':
            file = open('adb_cmds.txt', 'r')
            adb_cmds = file.read()
            print(adb_cmds)
            file.close()
        
        elif cmd[0] == 'disconnect':
            os.system('adb disconnect')

        elif cmd[0] == "uninstall" or cmd[0] == 'remove' or cmd[0] == 'rm':
            if cmd[1] == '':
                nme = input('Specify app name! : ')
                fetch_id(nme)
            else:
                fetch_id(cmd[1])
            while True:
                if app_id == '':
                    print('An error occured pls try again!')
                else:
                    available_online = os.system(f'adb shell pm list packages | grep -Eo "{app_id}"')
                    if  available_online == 0:
                        verify = input(f'Do you wish to uninstall [{app_id}]?: Y/n ')
                        if verify == 'Y':
                            os.system(f'adb shell pm uninstall -k --user 0 {app_id}')
                            # os.system(f'adb shell cmd {app_id} uninstall -k')
                            break
                        else:
                            print('Operation cancelled!')
                            break
                    else:
                        print(f'Err [{app_id}] not found in local library!')
                        print('')
                        print('Attemping to locate alias locally..')
                        available_local = os.system(f'adb shell pm list packages | grep -e "{cmd[1]}"')
                        if available_local == 0:
                            print('')
                            delay(0.7)
                            os.system(f'adb shell pm list packages | grep -e "{cmd[1]}" > app_id.txt')
                            file = open('app_id.txt','r')
                            app_id = file.read()
                            file.close()
                            app_id = app_id.split(':')
                            app_id = app_id[1]
                            app_id = app_id.split('\n')
                            app_id = app_id[0]
                            verify = input(f'Do you wish to uninstall? [{app_id}]: Y/n ')
                            if verify == 'Y':
                                os.system(f'adb shell pm uninstall -k --user 0 {app_id}')
                                # os.system(f'adb shell cmd {app_id} uninstall -k')
                                break
                            else:
                                print('Operation cancelled!')
                                break

                        else:
                            delay(0.7)
                            print('App unavailable locally. PLs try again')
                            break

        elif cmd[0] == 'exit':
            exit(os.system('adb disconnect\n'))

except KeyboardInterrupt:
    exit(print(G,' exiting..\n'))

#