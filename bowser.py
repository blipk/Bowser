"""
 * Bowser for linux. 
 * Uses XDG desktop entries to find installed web browsers and sets itself as the default,
 * allowing you to set up rules that will match a string against URLs and open them with a specific browser.
 *
 * Run ./install.sh' to begin.
 * See README.md for advanced options.
 *
 * This file is part of bowser linux application
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
import json
import tkinter
import subprocess
from tkinter import *
from tkinter import ttk, simpledialog, filedialog, messagebox
from os import listdir, path
from os.path import isfile, join, expanduser

homePath = expanduser("~")
appPath = '/usr/share/applications/'
configDir = homePath + '/.config/bowser/'
configFile = homePath + '/.config/bowser/bowser.conf'
if not (path.exists(appPath + '/bowser.desktop')): print("Please run the install script."); exit()
try: URI = sys.argv[1]
except: URI = '--settings'

#CONFIG
config = {}
browserApps = {}
uriPrefs = {}
defaultBrowser = subprocess.check_output(['xdg-mime', 'query', 'default', 'text/html']).decode('utf-8')

def saveConfig(cFile = configFile):
    global config, browserApps, defaultBrowser, uriPrefs, configFile
    if not bool(config): config = {'browserApps': browserApps, 'defaultBrowser': defaultBrowser, 'uriPrefs': uriPrefs}
    if not path.exists(configDir): os.mkdir(configDir)
    if not path.exists(cFile): os.mknod(cFile)
    with open(cFile, 'w+') as file: file.write(json.dumps(config)); file.close()
def readConfig(cFile = configFile):
    global config, browserApps, defaultBrowser, uriPrefs
    with open(cFile, 'r') as file: config = json.load(file); file.close()
    browserApps = config['browserApps']
    defaultBrowser = config['defaultBrowser']
    uriPrefs = config['uriPrefs']
#END config

#SETUP
def setup():
    global browserApps, defaultBrowser, uriPrefs
    installedApps = [f for f in listdir(appPath) if isfile(join(appPath, f))]
    for app in installedApps:
        if (app == 'bowser.desktop'): continue
        f = open(appPath+app,"r"); contents = f.read(); f.close()

        catLoc = contents.find("Categories=")
        if (catLoc > -1): 
            cats = contents[catLoc:contents.find("\n", catLoc)]
            if (cats.find("WebBrowser") > -1):
                nameLoc = contents.find("Name=")
                execLoc = contents.find("Exec=")
                mimesLoc = contents.find("MimeType=")
                browserApps.update({app: [  
                    contents[nameLoc+5:contents.find("\n", nameLoc)],
                    contents[execLoc+5:contents.find("\n", execLoc)],
                    list(filter(    lambda x: x != "", contents[mimesLoc+9:contents.find("\n", mimesLoc)].split(';') ))
                ]})

    if not bool(uriPrefs): uriPrefs = {'youtube.com': defaultBrowser, 'youtu.be': defaultBrowser}
    associateMimetypes();
    saveConfig()
    print('Setup completed and config saved');
    messagebox.showinfo(title=None, message="Your installed web browsers have been detected and Bowser has been enabled.")
def reset():
    associateMimetypes(defaultBrowser);
    print(defaultBrowser + ' is now the default browser'); 
    messagebox.showinfo(title=None, message="Bowser has been disabled and links will now open with " + browserApps[defaultBrowser][0] + ".")
def associateMimetypes(browser='bowser.desktop'):
    global browserApps
    allMimes = []
    for k in browserApps: allMimes.append(browserApps[k][2])
    allMimes = list(dict.fromkeys(allMimes[0])) #remove duplicates
    allMimes = list(filter(lambda x: x != "", allMimes)) #remove empties
    for mime in allMimes: os.system('xdg-mime default ' + browser + ' ' + mime) #silent
    #for mime in allMimes: os.system('gio mime ' + mime + ' ' + browser)
#END SETUP

#MAIN
def openBrowser():
    for k in config['uriPrefs']:
        if (URI.find(k) > -1):
            execCmd = browserApps.get(uriPrefs[k])[1].replace("%u", URI)
            os.system(execCmd)
            exit() #if a preference is found, don't continue to opening in default
    execCmd = browserApps.get(defaultBrowser)[1].replace("%u", URI)
    os.system(execCmd);

#SETTINGS GUI
lastSelected = ''
def settings():
    global config, browserApps, defaultBrowser, uriPrefs
    def lbSelected_update():
        lbSelected.delete(0, END)
        for uriPref in uriPrefs: lbSelected.insert(END, uriPref)
    def lbSelected_cb(event):
        global lastSelected
        try: lastSelected = lbSelected.get(lbSelected.curselection())
        except: print('None selected')
        if not (lastSelected == ''):
            cbBrowsers.current(  cbBrowsers['values'].index(browserApps[uriPrefs[lastSelected]][0])   )
    def cbBrowsers_cb(event):
        global lastSelected
        if (lastSelected == ''): return
        selectedApp = ''
        for browserApp in browserApps:
            if(browserApps[browserApp][0] == cbBrowsers['values'][cbBrowsers.current()]): selectedApp = browserApp
        uriPrefs[lastSelected] = selectedApp
        saveConfig()
    def btnDelete_cb():
        global lastSelected
        if (lastSelected == ''): return
        del uriPrefs[lbSelected.get(lbSelected.curselection())]
        lbSelected.delete(ANCHOR)
        saveConfig()
        lbSelected_update()
    def btnAdd_cb():
        out = ''
        out = simpledialog.askstring("New Rule", "Text/Domain to search for in URI passed to web browser:")
        uriPrefs.update({out: defaultBrowser})
        saveConfig()
        lbSelected_update()
    def exportConfig():
        global config
        outFile = filedialog.asksaveasfile()
        if (outFile == None): print('No file selected'); return
        outFile.write(json.dumps({'browserApps': browserApps, 'defaultBrowser': defaultBrowser, 'uriPrefs': uriPrefs})); 
        outFile.close()
    def importConfig():
        global config
        inFile = filedialog.askopenfile()
        if (inFile == None): print('No file selected'); return
        config = json.load(inFile); inFile.close()
        saveConfig(); readConfig()
        lbSelected_update()
    def openAppWebsite():
        global URI
        URI = 'https://github.com/blipk/Bowser'
        openBrowser()

    lastSelected = ''
    root = Tk()
    root.title("Bowser")
    root.iconphoto(False, PhotoImage(file='/usr/share/icons/hicolor/256x256/apps/bowser.png'))

    lbSelected = Listbox(root)
    lbSelected.grid(column=0, row=1, columnspan=2)
    lbSelected_update()
    lbSelected.bind("<<ListboxSelect>>", lbSelected_cb)

    btnAdd = Button(root, text = "Add Rule", command = btnAdd_cb)  
    btnAdd.grid(column=0, row=0)
    btnDelete = Button(root, text = "Delete Rule", command = btnDelete_cb)  
    btnDelete.grid(column=1, row=0)
    
    values = []
    for browserApp in browserApps: values.append(browserApps[browserApp][0])
    cbBrowsers = ttk.Combobox(root)
    cbBrowsers.grid(column=0, row=2, columnspan=2)
    cbBrowsers['values'] = values
    cbBrowsers.bind("<<ComboboxSelected>>", cbBrowsers_cb)

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Export Rules", command = exportConfig)
    filemenu.add_command(label="Import Rules", command = importConfig)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command = root.quit)
    menubar.add_cascade(label="File", menu = filemenu)

    settingsmenu = Menu(menubar, tearoff=0)
    #settingsmenu.add_command(label="Enable Bowser", command = associateMimetypes)
    settingsmenu.add_command(label="Enable Bowser and detect installed web browsers", command = setup)
    settingsmenu.add_command(label="Disable Bowser", command = reset)
    menubar.add_cascade(label="Settings", menu = settingsmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=openAppWebsite)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)
    root.mainloop()
    exit()
#END settings

#MAIN
if not (path.exists(configFile)): setup()
else: readConfig()
if (URI == '--settings'): settings()
if (URI == '--reset'): reset(); exit()
if (URI == '--setup'): setup(); settings();
openBrowser()

