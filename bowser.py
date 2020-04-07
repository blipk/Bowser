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
import json
import tkinter
import subprocess
import functools
from tkinter import *
from tkinter import ttk, simpledialog, filedialog, messagebox
from os import listdir, path
from os.path import isfile, join, expanduser
from functools import partial

homePath = expanduser("~")
appPath = '/usr/share/applications/'
configDir = homePath + '/.config/bowser/'
configFile = homePath + '/.config/bowser/bowser.conf'
try: URI = sys.argv[1]
except: URI = '--settings'

#CONFIG
config = {}
browserApps = {}
uriPrefs = {}
defaultBrowser = ''
def cleanConfig():
    global browserApps
    for browserApp in browserApps: 
        try: del browserApps[browserApp][3]   #Remove Tk.BooleanVar which is used for GUI state
        except: print('Unused')
def saveConfig(cFile = configFile):
    global config, browserApps, defaultBrowser, uriPrefs, configFile
    cleanConfig()
    config = {'browserApps': browserApps, 'defaultBrowser': defaultBrowser, 'uriPrefs': uriPrefs}
    if not path.exists(configDir): os.makedirs(configDir)
    if not path.exists(cFile): os.mknod(cFile)
    with open(cFile, 'w+') as file: file.write(json.dumps(config)); file.close()
    print("Config saved.")
def readConfig(cFile = configFile):
    global config, browserApps, defaultBrowser, uriPrefs
    with open(cFile, 'r') as file: config = json.load(file); file.close()
    browserApps = config['browserApps']
    defaultBrowser = config['defaultBrowser']
    uriPrefs = config['uriPrefs']
    print("Config read.")
#END config

#SETUP
if not path.exists(homePath+'/.local/share/icons/hicolor/256x256/apps/'): os.makedirs(homePath+'/.local/share/icons/hicolor/256x256/apps/')
if not path.exists(homePath+'/.local/share/icons/hicolor/scalable/apps/'): os.makedirs(homePath+'/.local/share/icons/hicolor/scalable/apps/')
os.system("cp bowser.svg ~/.local/share/icons/hicolor/scalable/apps && xdg-icon-resource install --novendor --context apps --size 256 bowser.png bowser")
def setup():
    os.system("mkdir ~/.config/bowser/")
    os.system("cp bowser.py ~/.config/bowser/ && chmod +777 ~/.config/bowser/bowser.py")
    os.system("xdg-desktop-menu install bowser.desktop --novendor")

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

    #currentBrowser = subprocess.check_output(['xdg-mime', 'query', 'default', 'text/html']).decode('utf-8').replace('\n', '');
    currentBrowser = subprocess.check_output(['xdg-settings', 'get', 'default-web-browser']).decode('utf-8').replace('\n', '');
    if not (currentBrowser == 'bowser.desktop'): defaultBrowser = currentBrowser; associateMimetypes();
    if (defaultBrowser == 'bowser.desktop' or defaultBrowser == ''): defaultBrowser = list(browserApps)[0]
    if not bool(uriPrefs): uriPrefs = {'youtube.com': defaultBrowser, 'youtu.be': defaultBrowser}
    saveConfig()
    print('Setup completed and config saved');
    messagebox.showinfo(title=None, message="Your installed web browsers have been detected and Bowser has been enabled.")
def reset():
    associateMimetypes(defaultBrowser);
    print(defaultBrowser + ' is now the default browser'); 
    messagebox.showinfo(title=None, message="Bowser has been disabled and links will now open with " + browserApps[defaultBrowser][0] + ".")
def associateMimetypes(browser='bowser.desktop'):
    '''
    global browserApps
    allMimes = []
    for k in browserApps: allMimes.append(browserApps[k][2])
    allMimes = list(dict.fromkeys(allMimes[0])) #remove duplicates
    allMimes = list(filter(lambda x: x != "", allMimes)) #remove empties
    #for mime in allMimes: os.system('xdg-mime default ' + browser + ' ' + mime) #silent
    #for mime in allMimes: os.system('gio mime ' + mime + ' ' + browser)
    '''
    os.system('xdg-settings set default-web-browser ' + browser)

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
lastSelectedIndex = 0
def settings():
    global config, browserApps, defaultBrowser, uriPrefs
    def ui_update():
        lbPrefs_update()
        browsermenu_update()
        saveConfig(); readConfig()
        browsermenu_update()
    def browsermenu_update(event = None):
        global defaultBrowser
        browsermenu.delete(0, END)
        for browserApp in browserApps:
            try: browserApps[browserApp][3]
            except IndexError: browserApps[browserApp].append(BooleanVar())
            if (defaultBrowser == browserApp): browserApps[browserApp][3].set(True)
            else: browserApps[browserApp][3].set(False)
            browsermenu.add_checkbutton(label = browserApps[browserApp][0], onvalue=1, offvalue=0, 
                                                                            variable = browserApps[browserApp][3], 
                                                                            command = functools.partial(updateDefaultBrowser, browserApp))
    def lbPrefs_update():
        global uriPrefs
        lbPrefs.delete(0, END)
        for uriPref in uriPrefs: lbPrefs.insert(END, uriPref)
    def lbPrefs_cbSelected(event):
        global lastSelected, uriPrefs
        try: lastSelected = lbPrefs.get(lbPrefs.curselection()); lastSelectedIndex = lbPrefs.nearest(event.y)
        except: print('None selected')
        if (lastSelected == ''): return
        dbBrowsers.current(  dbBrowsers['values'].index(browserApps[uriPrefs[lastSelected]][0])   )
    def lbPrefs_cbMove(event):
        global lastSelectedIndex, uriPrefs
        i = lbPrefs.nearest(event.y)
        if i < lastSelectedIndex:
            x = lbPrefs.get(i)
            lbPrefs.delete(i); lbPrefs.insert(i+1, x)
            lastSelectedIndex = i
        elif i > lastSelectedIndex:
            x = lbPrefs.get(i)
            lbPrefs.delete(i); lbPrefs.insert(i-1, x)
            lastSelectedIndex = i
        values = lbPrefs.get(0, END)
        tmp = {}
        for value in values:
            for uriPref in uriPrefs:
                if (uriPref == value):
                    tmp.update({uriPref: uriPrefs[uriPref]})
        uriPrefs = tmp
        ui_update()
    def dbBrowsers_cbSelected(event):
        global lastSelected
        if (lastSelected == ''): return
        selectedApp = ''
        for browserApp in browserApps:
            if(browserApps[browserApp][0] == dbBrowsers['values'][dbBrowsers.current()]): selectedApp = browserApp
        uriPrefs[lastSelected] = selectedApp
        ui_update()
    def btnDelete_cb():
        global lastSelected
        if (lastSelected == ''): return
        del uriPrefs[lbPrefs.get(lbPrefs.curselection())]
        lbPrefs.delete(ANCHOR)
        ui_update()
    def btnAdd_cb():
        out = ''
        out = simpledialog.askstring("New Rule", "Text/Domain to search for in URI passed to web browser:")
        uriPrefs.update({out: defaultBrowser})
        ui_update()
    def importConfig():
        print('Importing Config')
        global config, browserApps, uriPrefs, defaultBrowser
        inFile = filedialog.askopenfile()
        if (inFile == None): print('No file selected'); return
        config = json.load(inFile); inFile.close()
        browserApps = config['browserApps']
        defaultBrowser = config['defaultBrowser']
        print(defaultBrowser)
        uriPrefs = config['uriPrefs']
        ui_update()
    def exportConfig():
        global config
        outFile = filedialog.asksaveasfile()
        if (outFile == None): print('No file selected'); return
        cleanConfig()
        outFile.write(json.dumps({'browserApps': browserApps, 'defaultBrowser': defaultBrowser, 'uriPrefs': uriPrefs})); 
        outFile.close()
    def openAppWebsite():
        global URI
        URI = 'https://github.com/blipk/Bowser'
        openBrowser()
    def updateDefaultBrowser(newDefault):
        global defaultBrowser, browserApps
        for browserApp in browserApps:
            try: browserApps[browserApp][3]
            except IndexError: browserApps[browserApp].append(BooleanVar())
            browserApps[browserApp][3].set(False)
            if (browserApp == newDefault): 
                browserApps[browserApp][3].set(True)
                defaultBrowser = browserApp
        print(browserApps[defaultBrowser][0] + ' is now the default browser')
        ui_update()

    lastSelected = ''
    root = Tk()
    root.title("Bowser")
    #root.iconphoto(False, PhotoImage(file='/usr/share/icons/hicolor/256x256/apps/bowser.png'))

    lbPrefs = Listbox(root)
    lbPrefs.grid(column=0, row=1, columnspan=2)
    lbPrefs_update()
    lbPrefs.bind("<<ListboxSelect>>", lbPrefs_cbSelected)
    #lbPrefs.bind('<B1-Motion>', lbPrefs_cbMove) #buggy

    btnAdd = Button(root, text = "Add Rule", command = btnAdd_cb)  
    btnAdd.grid(column=0, row=0)
    btnDelete = Button(root, text = "Delete Rule", command = btnDelete_cb)  
    btnDelete.grid(column=1, row=0)
    
    values = []
    for browserApp in browserApps: values.append(browserApps[browserApp][0])
    dbBrowsers = ttk.Combobox(root)
    dbBrowsers.grid(column=0, row=2, columnspan=2)
    dbBrowsers['values'] = values
    dbBrowsers.bind("<<ComboboxSelected>>", dbBrowsers_cbSelected)

    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Export Rules", command = exportConfig)
    filemenu.add_command(label="Import Rules", command = importConfig)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command = root.quit)
    menubar.add_cascade(label="File", menu = filemenu)


    settingsmenu = Menu(menubar, tearoff=0)
    browsermenu = Menu(settingsmenu, tearoff=0)
    settingsmenu.add_cascade(label="Default Web Browser", menu = browsermenu)
    browsermenu_update() #settingsmenu.bind( '<<MenuSelect>>', browsermenu_update)
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
nt(browserApp)
