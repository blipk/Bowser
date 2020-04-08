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
import re
from tkinter import *
from tkinter import ttk, simpledialog, filedialog, messagebox
from os import listdir, path
from os.path import isfile, join, expanduser
from functools import partial

homePath = expanduser("~")
appPath = '/usr/share/applications/'
userAppPath = homePath+'/.local/share/applications/'
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
def setup(init = False):
    os.system("mkdir ~/.config/bowser/")
    os.system("cp bowser.py ~/.config/bowser/ && chmod +777 ~/.config/bowser/bowser.py")
    os.system("cp bowser.png ~/.config/bowser/")
    os.system("xdg-desktop-menu install bowser.desktop --novendor")
    
    global browserApps, defaultBrowser, uriPrefs
    installedApps = [appPath+f for f in listdir(appPath) if isfile(join(appPath, f))]
    installedApps += [userAppPath+f for f in listdir(userAppPath) if isfile(join(userAppPath, f))]
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
                browserApps.update({app: [  
                    contents[nameLoc+5:contents.find("\n", nameLoc)],
                    contents[execLoc+5:contents.find("\n", execLoc)],
                    list(filter(    lambda x: x != "", contents[mimesLoc+9:contents.find("\n", mimesLoc)].split(';') ))
                ]})

    currentBrowser = subprocess.check_output(['xdg-settings', 'get', 'default-web-browser']).decode('utf-8').replace('\n', '');
    if (not currentBrowser == 'bowser.desktop' and init == True): defaultBrowser = currentBrowser; setxdgDefaultWebBrowser();
    if (defaultBrowser == 'bowser.desktop' or defaultBrowser == ''): defaultBrowser = list(browserApps)[0]
    tmp = {'scheme': True, 'authority': True, 'path': True, 'query': True, 'fragment': True}
    if not bool(uriPrefs): uriPrefs = {'youtube.com': {'defaultBrowser': defaultBrowser, 'uriOptions': tmp}, 'youtu.be': {'defaultBrowser': defaultBrowser, 'uriOptions': tmp}}
    saveConfig()
    print('Setup completed and config saved');
def setxdgDefaultWebBrowser(browser='bowser.desktop'):
    os.system('xdg-settings set default-web-browser ' + browser)
    print(browser + ' is now the default browser');
def detectWebBrowsers():
    setup(False)
    messagebox.showinfo(title=None, message="Your installed web browsers have been scanned and updated.")
def disableBowser():
    setxdgDefaultWebBrowser(defaultBrowser);
    messagebox.showinfo(title=None, message="Bowser has been disabled and links will now open with " + browserApps[defaultBrowser][0] + ".")
def enableBowser():
    setxdgDefaultWebBrowser()
    messagebox.showinfo(title=None, message="Bowser has been enabled, rules are active.")
#END SETUP

#MAIN
def openBrowser():
    global URI
    regexPattern = ("^(?P<s1>(?P<s0>[^:/\?#]+):)?(?P<a1>" 
                    "//(?P<a0>[^/\?#]*))?(?P<p0>[^\?#]*)" 
                    "(?P<q1>\?(?P<q0>[^#]*))?" 
                    "(?P<f1>#(?P<f0>.*))?")
    regex = re.compile(regexPattern)
    output = regex.match(URI)
    
    if (output.group('a1') == None):     #Regex isn't perfect if there's no scheme
        URI = 'https://' + URI
        output = regex.match(URI)

    splitURI = {'scheme': output.group('s1'), 'authority': output.group('a0'), 'path': output.group('p0'), 'query': output.group('q1'), 'fragment': output.group('f1')}


    matchFound = False
    for pref in config['uriPrefs']:
        for x in config['uriPrefs'][pref]['uriOptions']:
            if (config['uriPrefs'][pref]['uriOptions'][x] == False): continue;
            if (str(splitURI[x]).find(pref) > -1):
                matchFound = True
                execCmd = browserApps.get(uriPrefs[pref]['defaultBrowser'])[1].replace("%u", URI).replace("%U", URI)
                os.system(execCmd)
    if (matchFound): exit()
    execCmd = browserApps.get(defaultBrowser)[1].replace("%u", URI).replace("%U", URI)
    os.system(execCmd);

#SETTINGS GUI
lastSelected = ''
lastSelectedIndex = 0
def settings():
    class AddDialog(simpledialog.Dialog):
        def body(self, master):
            self.iconphoto(False, PhotoImage(file='/home/kronosoul/.config/bowser/bowser.png'))
            Label(master, text="Text to search for:   ").grid(row=0, column=0, columnspan=1, sticky=E)
            self.input = Entry(master)
            self.input.grid(row=0, column=1, columnspan=5, sticky=W+E+N+S)
            Label(master, text="Parts of the link to search in:").grid(row=2, column=0, columnspan=5, sticky=W)
            Label(master, text="http://", fg="green").grid(row=3, column=0, sticky=E)
            Label(master, text="example.com:8023").grid(row=3, column=1, sticky=W)
            Label(master, text="/directions/here", fg="green").grid(row=3, column=2, sticky=W)
            Label(master, text="?name=value").grid(row=3, column=3, sticky=W)
            Label(master, text="#bookmark", fg="green").grid(row=3, column=4, sticky=W)
            
            def checkAll():
                for v in self.uriParts_cbs: self.uriParts_cbs[v].var.set(True)
            self.all = Button(master, text="All", command=checkAll)
            self.all.grid(row=4, column=0, sticky=W)
            self.uriParts = {'scheme': False, 'authority': False, 'path': False, 'query': False, 'fragment': False}
            self.uriParts_cbs = dict()
            for checkbox in self.uriParts:
                self.uriParts_cbs[checkbox] = Checkbutton(master, text="", onvalue=True, offvalue=False);
                self.uriParts_cbs[checkbox].var = BooleanVar(); self.uriParts_cbs[checkbox].var.set(True)
                self.uriParts_cbs[checkbox]['variable'] = self.uriParts_cbs[checkbox].var
            self.uriParts_cbs['scheme'].grid(row=4, column=0, sticky=E)
            self.uriParts_cbs['authority'].grid(row=4, column=1)
            self.uriParts_cbs['path'].grid(row=4, column=2)
            self.uriParts_cbs['query'].grid(row=4, column=3)
            self.uriParts_cbs['fragment'].grid(row=4, column=4  )

            return self.input #initial focus
        def apply(self):
            name = self.input.get()
            for option in self.uriParts:
                self.uriParts[option] = self.uriParts_cbs[option].var.get();
            self.result = {'name': name, 'uriOptions': self.uriParts}

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
        b = uriPrefs[lastSelected]['defaultBrowser']
        dbBrowsers.current(  dbBrowsers['values'].index(browserApps[b][0])   )
    def dbBrowsers_cbSelected(event):
        global lastSelected
        if (lastSelected == ''): return
        selectedApp = ''
        for browserApp in browserApps:
            if(browserApps[browserApp][0] == dbBrowsers['values'][dbBrowsers.current()]): selectedApp = browserApp
        uriPrefs[lastSelected]['defaultBrowser'] = selectedApp
        ui_update()
    def btnDelete_cb():
        global lastSelected
        if (lastSelected == ''): return
        del uriPrefs[lbPrefs.get(lbPrefs.curselection())]
        lbPrefs.delete(ANCHOR)
        ui_update()
    def btnAdd_cb():
        out = ''
        addDialog = AddDialog(root, "New Rule")
        if (addDialog.result == None or not bool(addDialog.result['uriOptions']) or addDialog.result['name'] == None or addDialog.result['name'] == ''): return;
        out = {addDialog.result['name']: {'defaultBrowser': defaultBrowser, 'uriOptions': addDialog.result['uriOptions']}}
        uriPrefs.update(out)
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

    root = Tk()
    root.title("Bowser")
    root.iconphoto(False, PhotoImage(file='/home/kronosoul/.config/bowser/bowser.png'))

    lbPrefs = Listbox(root)
    lbPrefs.grid(column=0, row=1, columnspan=2)
    lbPrefs_update()
    lbPrefs.bind("<<ListboxSelect>>", lbPrefs_cbSelected)

    btnAdd = Button(root, text = "Add Rule", command = btnAdd_cb)  
    btnAdd.grid(column=0, row=0)
    btnDelete = Button(root, text = "Delete Rule", command = btnDelete_cb)  
    btnDelete.grid(column=1, row=0)
    
    dbBrowsers = ttk.Combobox(root)
    dbBrowsers.grid(column=0, row=2, columnspan=2)    
    dbBrowsers.bind("<<ComboboxSelected>>", dbBrowsers_cbSelected)
    values = []
    for browserApp in browserApps: values.append(browserApps[browserApp][0])
    dbBrowsers['values'] = values

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
    browsermenu_update()
    settingsmenu.add_command(label="Enable Bowser", command = enableBowser)
    settingsmenu.add_command(label="Disable Bowser", command = disableBowser)
    settingsmenu.add_command(label="Detect installed web browsers", command = lambda:[detectWebBrowsers(), ui_update()])
    menubar.add_cascade(label="Settings", menu = settingsmenu)


    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command = openAppWebsite)
    menubar.add_cascade(label="Help", menu = helpmenu)

    root.config(menu=menubar)
    root.mainloop()
    exit()
#END settings

#MAIN
if not (path.exists(configFile)): setup()
else: readConfig()
if (URI == '--enable'): setxdgDefaultWebBrowser(); exit()
if (URI == '--disable'): setxdgDefaultWebBrowser(defaultBrowser); exit()
if (URI == '--settings'): settings(); 
if (URI == '--setup'): setup(); settings();
openBrowser()
