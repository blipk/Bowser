#!/usr/bin/env python
"""
 * Bowser for linux. 
 * Uses XDG desktop entries to find installed web browsers and sets itself as the default,
 * allowing you to set up rules that will match a string against URLs and open them with a specific browser.
 *
 * Run 'python3 bowser.py' to begin.
 * See README.md for usage and advanced options.
 *
 * This file is part of the Bowser linux application
 * Copyright (C) 2020 A.D. - http://kronosoul.xyz
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope this it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import subprocess
import json
import re
import importlib
import ntpath
from os import listdir, path
from os.path import isfile, join
from multiprocessing import Process
import bowserGlobals as bowser

appPath = '/usr/share/applications/'
userAppPath = bowser.homePath+'/.local/share/applications/'
configDir = bowser.homePath + '/.config/bowser/'
configFile = bowser.homePath + '/.config/bowser/bowser.conf'
uriFile = bowser.homePath + '/.config/bowser/.openuri'
try: bowser.URI = sys.argv[1]
except: bowser.URI = '--settings'
if (bowser.URI == "''" or bowser.URI == ''): bowser.URI = '--settings'
bowser.URI = bowser.URI.strip("'")

#CONTROL CHECK
def isRunning(count = 0):
    cmd = ['pgrep -f .*python.*bowser.py']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    my_pid, err = process.communicate()

    print (my_pid.splitlines())
    if len(my_pid.splitlines()) > count: return True
    else: return False
def passURI():
    if (bowser.URI.find('--settings') > -1): return
    with open(uriFile, 'w+') as file: file.write(bowser.URI); file.close()
def checkURI():
    bowser.bowserSettings.root.after(1000, checkURI)
    if (not os.path.isfile(uriFile)):  return
    print('found uri file')
    with open(uriFile, 'r') as file: bowser.URI = file.read(); file.close()
    os.remove(uriFile)
    bowser.openBrowser()
if (isRunning(2)): #Shouldn't be more than 2 instances running
    print('To do')#TO DO kill the others, application logic SHOULD prevent this from happening for now
    
if (isRunning(1)):
    #TO DO check which dialog is open and open settings if its the unmatched one and we want settings
    #or create a log of URIs in passURI() to be opened as sequential dialogs
    passURI()
    exit()

#CONFIG
def cleanConfig():
    for browserApp in bowser.browserApps: 
        try: del bowser.browserApps[browserApp][4]   #Remove Tk.BooleanVar which is used for GUI state
        except: print('No var to clean')
def saveConfig(cFile = configFile):
    cleanConfig()
    bowser.Config = {'browserApps': bowser.browserApps, 'defaultBrowser': bowser.defaultBrowser, 'uriPrefs': bowser.uriPrefs, 'askOnUnmatchedURI': bowser.askOnUnmatchedURI}
    if not path.exists(configDir): os.makedirs(configDir)
    if not path.exists(cFile): os.mknod(cFile)
    with open(cFile, 'w+') as file: file.write(json.dumps(bowser.Config)); file.close()
    print("Config saved.")
def readConfig(cFile = configFile):
    with open(cFile, 'r') as file: bowser.Config = json.load(file); file.close()
    bowser.browserApps = bowser.Config['browserApps']
    bowser.defaultBrowser = bowser.Config['defaultBrowser']
    bowser.uriPrefs = bowser.Config['uriPrefs']
    bowser.askOnUnmatchedURI = bowser.Config['askOnUnmatchedURI']
    print("Config read.")

#SETUP
def setup(init = False):
    os.system("mkdir ~/.config/bowser/")
    os.system("cp bowser.py ~/.config/bowser/ && chmod +777 ~/.config/bowser/bowser.py")
    os.system("cp bowserSettings.py ~/.config/bowser/ && chmod +777 ~/.config/bowser/bowserSettings.py")
    os.system("cp bowserGlobals.py ~/.config/bowser/")
    os.system("cp bowser.png ~/.config/bowser/")
    os.system("xdg-desktop-menu install bowser.desktop --novendor")
    if not path.exists(bowser.homePath+'/.local/share/icons/hicolor/256x256/apps/'): os.makedirs(bowser.homePath+'/.local/share/icons/hicolor/256x256/apps/')
    if not path.exists(bowser.homePath+'/.local/share/icons/hicolor/scalable/apps/'): os.makedirs(bowser.homePath+'/.local/share/icons/hicolor/scalable/apps/')
    os.system("cp bowser.svg ~/.local/share/icons/hicolor/scalable/apps && xdg-icon-resource install --novendor --context apps --size 256 bowser.png bowser")
    
    bowser.browserApps = {}
    installedApps = [appPath+f for f in listdir(appPath) if isfile(join(appPath, f))]
    installedApps += [userAppPath+f for f in listdir(userAppPath) if isfile(join(userAppPath, f))]
    currentBrowser = getxdgDefaultWebBrowser()
    for app in installedApps:
        if (app.find('bowser.desktop') > -1): continue
        f = open(app, "r"); contents = f.read(); f.close()

        catLoc = contents.find("Categories=")
        if (catLoc > -1): 
            cats = contents[catLoc:contents.find("\n", catLoc)]
            if (cats.find("WebBrowser") > -1):
                print('Adding ' + app)
                nameLoc = contents.find("Name=")
                execLoc = contents.find("Exec=")
                mimesLoc = contents.find("MimeType=")
                iconLoc = contents.find("Icon=")
                bowser.browserApps.update({app: [  
                    contents[nameLoc+5:contents.find("\n", nameLoc)],
                    contents[execLoc+5:contents.find("\n", execLoc)],
                    list(filter(    lambda x: x != "", contents[mimesLoc+9:contents.find("\n", mimesLoc)].split(';') )),
                    contents[iconLoc+5:contents.find("\n", iconLoc)],
                ]})

                if(app.find(currentBrowser) > -1): currentBrowser = app

    bowser.defaultBrowser = currentBrowser
    if (init): bowser.askOnUnmatchedURI = True
    if (init and not currentBrowser.find('bowser.desktop') > -1): setxdgDefaultWebBrowser();
    if (bowser.defaultBrowser.find('bowser.desktop') > -1 or bowser.defaultBrowser == ''):  bowser.defaultBrowser = list(bowser.browserApps)[0]
    tmp = {'scheme': True, 'authority': True, 'path': True, 'query': True, 'fragment': True}
    
    if not bool(bowser.uriPrefs): bowser.uriPrefs = {'youtube.com': {'defaultBrowser': bowser.defaultBrowser, 'uriOptions': tmp}, 'youtu.be': {'defaultBrowser': bowser.defaultBrowser, 'uriOptions': tmp}}
    saveConfig()
    print('Setup completed and config saved');
def getxdgDefaultWebBrowser():
    currentBrowser = subprocess.check_output(['xdg-settings', 'get', 'default-web-browser']).decode('utf-8').replace('\n', '')
    return currentBrowser
def setxdgDefaultWebBrowser(browser='bowser.desktop'):
    pathName, fileName = ntpath.split(browser)
    os.system('xdg-settings set default-web-browser ' + fileName)
    print(browser + ' is now the default browser');
def openBrowser(overrideBrowser = False):
    print(bowser.URI)
    browser = bowser.defaultBrowser
    if (bool(overrideBrowser)): 
        pathName, fileName = ntpath.split(overrideBrowser)
    
    splitURI = bowser.splitURI(bowser.URI)    
    matchFound = False
    for pref in bowser.Config['uriPrefs']:
        compareURI = ''
        #print('!!!!!!Searching pref', pref, ' against ', bowser.URI)
        for x in bowser.Config['uriPrefs'][pref]['uriOptions']:
            if (bowser.Config['uriPrefs'][pref]['uriOptions'][x] == False): continue;
            if (bool(splitURI[x]) and x != 'scheme'): compareURI += str(splitURI[x])
            
            #print('compare', compareURI, pref)
            if (matchFound): continue
            if (str(splitURI[x]).find(pref) > -1 or compareURI.find(pref) > -1 and bool(compareURI)):
                matchFound = True
                print('---Match found') 
                execCmd = bowser.browserApps.get(bowser.uriPrefs[pref]['defaultBrowser'])[1].replace("%u", "").replace("%U", "").strip()
                process = subprocess.Popen([execCmd, bowser.URI], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if (matchFound and bowser.bowserSettings == None): exit()
    
    if (bowser.askOnUnmatchedURI and not matchFound):
        bowser.bowserSettings.openUnmatchedURIDialog()
    elif (not matchFound):
        execCmd = bowser.browserApps.get(bowser.uriPrefs[pref]['defaultBrowser'])[1].replace("%u", "").replace("%U", "").strip()
        process = subprocess.Popen([execCmd, bowser.URI], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if (bowser.bowserSettings == None): exit()

#MAIN
if not (path.exists(configFile)): setup()
else: readConfig(); 
def settingsVars():
    bowser.cleanConfig = cleanConfig
    bowser.saveConfig = saveConfig
    bowser.readConfig = readConfig
    bowser.getxdgDefaultWebBrowser = getxdgDefaultWebBrowser
    bowser.setxdgDefaultWebBrowser = setxdgDefaultWebBrowser
    bowser.setup = setup
    bowser.openBrowser = openBrowser
    bowser.checkURI = checkURI
def settings():
    if (bool(bowser.bowserSettings)): 
        if (callable(bowser.bowserSettings)):
            settingsVars()
            bowser.bowserSettings()
        else: bowser.bowserSettings.start()
if __name__ == "__main__": 
    settingsVars()
    bowser.bowserSettings = importlib.import_module('bowserSettings')

if (bowser.URI == '--enable'): setxdgDefaultWebBrowser();
elif (bowser.URI == '--disable'): setxdgDefaultWebBrowser(bowser.defaultBrowser)
elif (bowser.URI == '--settings'): print(bowser.URI); settings()
elif (bowser.URI == '--setup'): setup(True); settings()
else: openBrowser()
