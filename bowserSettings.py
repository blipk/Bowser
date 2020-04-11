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
import functools
import json
import tkinter as tk
from tkinter import ttk, simpledialog, commondialog, filedialog, messagebox
from os import path
import bowserGlobals as bowser

#CLASSES
class tkAddEditDialog(simpledialog.Dialog):
    def __init__(self, master, title, pref = False):
        self.pref = pref
        super().__init__(master, title = title)
    def body(self, selfFrame):
        master = self.parent
        
        if (bool(self.pref)): prefName = list(self.pref.keys())[0]

        self.iconphoto(False, tk.PhotoImage(file=bowser.homePath+'/.config/bowser/bowser.png'))
        tk.Label(selfFrame, text="Search for:   ").grid(row=0, column=0, columnspan=1, sticky=tk.E)
        self.input = tk.Entry(selfFrame)
        if (bool(self.pref)):
            self.input.delete(0, tk.END)
            self.input.insert(0, prefName)
        self.input.grid(row=0, column=1, columnspan=5, sticky=tk.W+tk.E+tk.N+tk.S)
        tk.Label(selfFrame, text="In these sections:").grid(row=2, column=0, columnspan=5, sticky=tk.W)
        

        if (bool(self.pref)): self.uriParts = self.pref[prefName]['uriOptions']
        else: self.uriParts = {'scheme': False, 'authority': True, 'path': True, 'query': False, 'fragment': False}
        splitURI = bowser.splitURI("http://example.com:8023/directions/here?name=value#bookmark")
        self.uriParts_cbs = dict()
        self.urlLabels = list()

        i = 0
        stick = tk.E
        state = 'disabled'
        for element in splitURI:
            if ((element.find('NoTrim') > -1) or splitURI[element] == None or splitURI[element] == ''): continue
            if (self.uriParts[element]): state = 'normal'
            self.urlLabels.append(tk.Label(selfFrame, text=splitURI[element], bd = 0, padx = 0, fg = 'green', disabledforeground = 'red', state = state))
            self.urlLabels[i].grid(row=3, column=i, sticky=stick)
            self.urlLabels[i].bind("<Button-1>", functools.partial(self.toggleURIOptions, i))
            stick = tk.W 
            state = 'disabled'
            i += 1
        def checkAll():
            for v in self.uriParts_cbs: self.uriParts_cbs[v].var.set(True)
            self.updateURILabels();
        self.all = tk.Button(selfFrame, text="All", command=checkAll)
        self.all.grid(row=4, column=0, sticky=tk.W)

        i = 0
        for checkbox in self.uriParts:
            self.uriParts_cbs[checkbox] = tk.Checkbutton(selfFrame, text="", onvalue=True, offvalue=False, command=functools.partial(self.updateURILabels, i));
            self.uriParts_cbs[checkbox].var = tk.BooleanVar(); self.uriParts_cbs[checkbox].var.set(self.uriParts[checkbox])
            self.uriParts_cbs[checkbox]['variable'] = self.uriParts_cbs[checkbox].var
            i += 1
        self.uriParts_cbs['scheme'].grid(row=4, column=0, sticky=tk.E)
        self.uriParts_cbs['authority'].grid(row=4, column=1)
        self.uriParts_cbs['path'].grid(row=4, column=2)
        self.uriParts_cbs['query'].grid(row=4, column=3)
        self.uriParts_cbs['fragment'].grid(row=4, column=4  )

        return self.input #Initial focus
    def apply(self):
        name = self.input.get()
        for option in self.uriParts:
            self.uriParts[option] = self.uriParts_cbs[option].var.get();
        self.result = {'name': name, 'uriOptions': self.uriParts}
    def updateURILabels(self, event = None):
        i = 0
        for label in self.urlLabels:
            if (self.uriParts_cbs[list(self.uriParts)[i]].var.get()):
                self.urlLabels[i].config(state = 'normal')
            else: self.urlLabels[i].config(state = 'disabled')
            i += 1
    def toggleURIOptions(self, i = 0, event = None):
        print(self.uriParts_cbs[list(self.uriParts)[i]], list(self.uriParts)[i])
        if (event.widget.cget('state') == 'normal'): 
            event.widget.config(state = 'disabled')
            self.uriParts_cbs[list(self.uriParts)[i]].var.set(False)
        else: 
            event.widget.config(state = 'normal')
            self.uriParts_cbs[list(self.uriParts)[i]].var.set(True)

class tkUnmatchedURIDialog(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        splitURI = bowser.splitURI(bowser.URI)

        self.urlLabels = list()
        i = 0
        stick = tk.E
        state = 'normal'
        for element in splitURI:
            if ((element.find('NoTrim') > -1 and element != 'authorityNoTrim') or element == 'scheme' or element == 'authority' or splitURI[element] == None or splitURI[element] == ''): continue
            if (i > 0): state = 'disabled'
            maxLength = 7
            if (i == 0): maxLength = 40
            if (i == 1): maxLength = 15
            self.urlLabels.append(tk.Label(master, bd = 0, padx = 0, fg = 'green', disabledforeground = 'red', state = state))
            self.urlLabels[i].fullText = splitURI[element]
            self.urlLabels[i].elementName = element
            labelText = (splitURI[element][:maxLength] + '..') if len(splitURI[element]) > maxLength else splitURI[element]
            self.urlLabels[i].config(text = labelText)

            self.urlLabels[i].grid(row=0, column=i, sticky=stick)
            self.urlLabels[i].bind("<Button-1>", functools.partial(self.togglePref, i))
            stick = tk.W 
            i += 1

        if (i == 1): 
            #self.urlLabels[0].grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S) #Centre if only domain
            tk.Label(master, text="", bd = 0, padx = 0, state = 'disabled').grid(row=0, column=1); i+=1 #padding for formatting
            
        self.i = 0
        self.images = list()
        self.browserButtons = list()
        for browserApp in bowser.browserApps: 
            self.browserButtons.append(tk.Button(master, text = bowser.browserApps[browserApp][0]))
            self.browserButtons[self.i].config(compound="left", anchor=tk.W, borderwidth = 0, command = functools.partial(self.addPrefAndOpen, browserApp))
            appIcon = '/usr/share/icons/hicolor/256x256/apps/' + bowser.browserApps[browserApp][3] + '.png'
            if (path.exists(appIcon)):
                img = tk.PhotoImage(file=appIcon).subsample(5)
                self.images.append(img)
                self.browserButtons[self.i].config(image = self.images[self.i])
            else: self.images.append(0)
            self.browserButtons[self.i].grid(row=self.i+1, column=0, sticky=tk.W+tk.E, columnspan=i)
            self.browserButtons[self.i].grid_columnconfigure(0, weight=1)
            self.browserButtons[self.i].grid_rowconfigure(0, weight=1)
            self.i += 1
            
        
        #span = (i + 2 // 2) // 2
        self.settingsImage = tk.PhotoImage(file=bowser.homePath+'/.config/bowser/bowser.png').subsample(8)
        self.btnSettings = tk.Button(master, image = self.settingsImage, command = self.openSettings, borderwidth = 0, anchor = tk.CENTER, padx = 50, width = 70)  
        self.btnSettings.grid(column=0, row=self.i+1, columnspan=1, sticky=tk.W)
        self.btnQuit = tk.Button(master, text = "Cancel", command = self.cancel, borderwidth = 0, anchor = tk.CENTER)
        self.btnQuit.grid(column=i-1, row=self.i+1, columnspan=i-1, sticky=tk.W+tk.E+tk.N+tk.S)
        

    def openSettings(self):
        global slave, root, settingsApp, unmatchedApp
        if (settingsApp == None): #Rebuild
            root.attributes('-type', 'normal')
            root.attributes('-alpha', '1.0')
            root.attributes("-topmost", 1)
            for rootWidget in root.grid_slaves(): rootWidget.grid_forget()
            unmatchedApp = None
            settingsApp = tkBowserSettings(root)
            settingsApp.grid()
        else: self.cancel()
    def togglePref(self, i = 0, event = None):
        if (self.urlLabels[i].cget('state') == 'normal'): 
            allowed = True
            try:
                if(self.urlLabels[i+1].cget('state') == 'normal' and self.urlLabels[i-1].cget('state') == 'normal'):
                     allowed = False
            except: allowed = True

            states = list() #Never allow if only one is on
            for x in self.urlLabels: 
                if (x.cget('state') == 'disabled'): states.append(False)
                else: states.append(True)
                
            if (states.count(True) <= 1): allowed = False
            if all(states): 
                if (i == 2): 
                    try: self.urlLabels[i+1].config(state = 'disabled')
                    except: pass
                if (i == 1): 
                    try: 
                        self.urlLabels[i+1].cget('state')   # Exception won't go to next line if doesn't exist
                        self.urlLabels[i-1].config(state = 'disabled')
                    except: pass
                        
                if (len(states) > 1): allowed = True

            if (allowed): self.urlLabels[i].config(state = 'disabled')
        else:
            allowed = True
            try:
                if(self.urlLabels[i+1].cget('state') == 'disabled' and self.urlLabels[i-1].cget('state') == 'disabled'):
                    allowed = False
            except:
                if (i+1 == len(self.urlLabels) and (self.urlLabels[i-1].cget('state') == 'disabled')): 
                    allowed = False

            states = list() #Always allow if they've all been turned off
            for x in self.urlLabels: 
                if (x.cget('state') == 'disabled'): states.append(False)
                else: states.append(True)
            if not any(states): allowed = True
            if (allowed): self.urlLabels[i].config(state = 'normal')
    def cancel(self):
        global unmatchedApp
        bowser.openAskBrowser = False
        bowser.URI = ''
        unmatchedApp = None
        self.master.destroy()
    def addPrefAndOpen(self, browserApp):
        outURI = ''
        first = True

        uriOptions = {'scheme': False, 'authority': False, 'path': False, 'query': False, 'fragment': False}

        for label in self.urlLabels:
            if (label.cget('state') != 'disabled'): 
                outURI += label.fullText
                uriOptions[label.elementName.replace("NoTrim", "")] = True
            if (first):     #Drop the www. in the domain for the pref
                if (outURI[:4] == 'www.'): outURI = outURI[4:]
                first = False

        out = {outURI: {'defaultBrowser': browserApp, 'uriOptions': uriOptions}}

        bowser.uriPrefs.update(out)
        bowser.saveConfig()
        bowser.openAskBrowser = False
        bowser.openBrowser()
        if (settingsApp != None): settingsApp.ui_update()
        self.cancel()

class tkBowserSettings(tk.Frame):   
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        
        self.lastSelected = ''
        self.lastSelectedIndex = 0

        self.btnNewRule = tk.Button(self, text = "New Rule", command = self.btnNewRule_cb, bd = 0)  
        self.btnNewRule.grid(column=0, row=0)
        self.btnDeleteRule = tk.Button(self, text = "Delete Rule", command = self.btnDeleteRule_cb, bd = 0)  
        self.btnDeleteRule.grid(column=1, row=0)
        
        self.lbPrefs = tk.Listbox(self, borderwidth = 0)
        self.lbPrefs.grid(column=0, row=1, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)
        self.lbPrefs_update()
        self.lbPrefs.bind("<<ListboxSelect>>", self.lbPrefs_cbSelected)
        self.lbPrefs.bind("<Double-Button-1>", self.editRule_cb)
        
        self.dbBrowsers = ttk.Combobox(self, state="readonly", justify = tk.CENTER)
        self.dbBrowsers.grid(column=0, row=2, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)    
        self.dbBrowsers.bind("<<ComboboxSelected>>", self.dbBrowsers_cbSelected)
        self.values = []
        for browserApp in bowser.browserApps: self.values.append(bowser.browserApps[browserApp][0])
        self.dbBrowsers['values'] = self.values

        style = ttk.Style()
        style.map('TCombobox', fieldbackground=[('readonly', 'white')], borderwidth=[('readonly', '0')], arrowsize=[('readonly', '0')])

        self.menubar = tk.Menu(self)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Export Configuration", command = self.exportConfig)
        self.filemenu.add_command(label="Import Configuration", command = self.importConfig)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command = root.quit)
        self.menubar.add_cascade(label="File", menu = self.filemenu)

        self.settingsmenu = tk.Menu(self.menubar, tearoff=0)
        self.bowserEnabled = tk.BooleanVar()
        if (bowser.getxdgDefaultWebBrowser() == 'bowser.desktop'): self.bowserEnabled.set(True)
        self.settingsmenu.add_checkbutton(label="Toggle Bowser", onvalue=1, offvalue=0, variable = self.bowserEnabled, command = self.toggleBowser)

        self.askOnUnmatchedURI = tk.BooleanVar()
        
        if (bowser.askOnUnmatchedURI == True): self.askOnUnmatchedURI.set(True)
        
        self.browsermenu = tk.Menu(self.settingsmenu, tearoff=0)
        self.settingsmenu.add_cascade(label="Default Web Browser", menu = self.browsermenu)
        self.browsermenu.add_checkbutton(label="Ask on unmatched links", onvalue=1, offvalue=0, variable = self.askOnUnmatchedURI, command = self.toggleAskOnUmatchedURI)
        self.settingsmenu.add_command(label="Detect installed web browsers", command = lambda:[self.detectWebBrowsers(), self.ui_update()])
        self.menubar.add_cascade(label="Settings", menu = self.settingsmenu)
        self.settingsmenu.bind("<<MenuSelect>>", self.settingsmenu_update)
        self.settingsmenu_update()
        self.browsermenu_update()

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label = "About...", command = self.openAppWebsite)
        self.menubar.add_cascade(label = "Help", menu = self.helpmenu)

        master.config(menu = self.menubar)

    def ui_update(self, event = None):
        self.lbPrefs_update()
        self.browsermenu_update()
        bowser.saveConfig(); bowser.readConfig()
        self.lbPrefs_update()
        self.browsermenu_update()
    def settingsmenu_update(self, event = None):
        if (self.bowserEnabled.get() == True):
            self.settingsmenu.entryconfigure(0, label="Bowser is Enabled")
        else:
            self.settingsmenu.entryconfigure(0, label="Enable Bowser")
    def browsermenu_update(self, event = None):
        self.browsermenu.delete(0, tk.END)
        self.browsermenu.add_checkbutton(label="Always ask", onvalue=1, offvalue=0, variable = self.askOnUnmatchedURI, command = self.toggleAskOnUmatchedURI)
        self.browsermenu.add_separator()
        for browserApp in bowser.browserApps:
            try: bowser.browserApps[browserApp][4]
            except IndexError: bowser.browserApps[browserApp].append(tk.BooleanVar())
            if (bowser.defaultBrowser == browserApp): bowser.browserApps[browserApp][4].set(True)
            else: bowser.browserApps[browserApp][4].set(False)
            self.browsermenu.add_checkbutton(label = bowser.browserApps[browserApp][0], onvalue=1, offvalue=0, 
                                                                            variable = bowser.browserApps[browserApp][4], 
                                                                            command = functools.partial(self.updateDefaultBrowser, browserApp))
    def lbPrefs_update(self):
        self.lbPrefs.delete(0, tk.END)
        for uriPref in bowser.uriPrefs: self.lbPrefs.insert(tk.END, uriPref)
    def lbPrefs_cbSelected(self, event):
        try: self.lastSelected = self.lbPrefs.get(self.lbPrefs.curselection()); self.lastSelectedIndex = self.lbPrefs.nearest(event.y)
        except: print('None selected')
        if (self.lastSelected == ''): return
        try: b = bowser.uriPrefs[self.lastSelected]['defaultBrowser']
        except KeyError: print('KeyError: List may not have updated to another selected item since deleting an item'); return;
        self.dbBrowsers.current(  self.dbBrowsers['values'].index(bowser.browserApps[b][0])   )
    def dbBrowsers_cbSelected(self, event):
        if (self.lastSelected == ''): return
        selectedApp = ''
        for browserApp in bowser.browserApps:
            if(bowser.browserApps[browserApp][0] == self.dbBrowsers['values'][self.dbBrowsers.current()]): selectedApp = browserApp
        try: bowser.uriPrefs[self.lastSelected]['defaultBrowser'] = selectedApp
        except KeyError: print('KeyError: List may not have updated to another selected item since deleting an item'); return;
        self.ui_update(self)
        
        self.lbPrefs.select_set(self.lbPrefs.get(0, tk.END).index(self.lastSelected))
        self.lbPrefs.activate(self.lbPrefs.get(0, tk.END).index(self.lastSelected))
        self.lbPrefs.focus_set()
    def btnDeleteRule_cb(self):
        try: del bowser.uriPrefs[self.lbPrefs.get(self.lbPrefs.curselection())]
        except: print('None selected to delete'); return
        self.lbPrefs.delete(tk.ANCHOR)
        self.ui_update(self)
    def btnNewRule_cb(self):
        out = ''
        addRuleDialog = tkAddEditDialog(self, title = "New Rule")
        if (addRuleDialog.result == None or not bool(addRuleDialog.result['uriOptions']) or addRuleDialog.result['name'] == None or addRuleDialog.result['name'] == ''): return;
        out = {addRuleDialog.result['name']: {'defaultBrowser': bowser.defaultBrowser, 'uriOptions': addRuleDialog.result['uriOptions']}}
        bowser.uriPrefs.update(out)
        self.ui_update(self)
    def editRule_cb(self, event = None):
        if (self.lastSelected == ''): return   
        out = ''
        pref = {self.lastSelected: bowser.uriPrefs[self.lastSelected]}
        editRuleDialog = tkAddEditDialog(self, title = "Edit Rule", pref = pref)
        if (editRuleDialog.result == None or not bool(editRuleDialog.result['uriOptions']) or editRuleDialog.result['name'] == None or editRuleDialog.result['name'] == ''): return;
        out = {editRuleDialog.result['name']: {'defaultBrowser': bowser.uriPrefs[self.lastSelected]['defaultBrowser'], 'uriOptions': editRuleDialog.result['uriOptions']}}
        if (editRuleDialog.result['name'] != list(pref.keys())[0]):
            del bowser.uriPrefs[list(pref.keys())[0]]
        bowser.uriPrefs.update(out)
        self.ui_update(self)
    def importConfig(self):
        print('Importing Config')
        inFile = filedialog.askopenfile()
        if (inFile == None): print('No file selected'); return
        bowser.config = json.load(inFile); inFile.close()
        bowser.browserApps = bowser.config['browserApps']
        bowser.defaultBrowser = bowser.config['defaultBrowser']
        bowser.uriPrefs = bowser.config['uriPrefs']
        self.ui_update(self)
    def exportConfig(self):
        outFile = filedialog.asksaveasfile()
        if (outFile == None): print('No file selected'); return
        bowser.cleanConfig()
        outFile.write(json.dumps({'browserApps': bowser.browserApps, 'defaultBrowser': bowser.defaultBrowser, 'uriPrefs': bowser.uriPrefs})); 
        outFile.close()
    def openAppWebsite(self):
        bowser.URI = 'https://github.com/blipk/Bowser'
        bowser.openBrowser()
    def updateDefaultBrowser(self, newDefault):
        for browserApp in bowser.browserApps:
            try: bowser.browserApps[browserApp][4]
            except IndexError: bowser.browserApps[browserApp].append(tk.BooleanVar())
            bowser.browserApps[browserApp][4].set(False)
            if (browserApp == newDefault): 
                bowser.browserApps[browserApp][4].set(True)
                bowser.defaultBrowser = browserApp
        print(bowser.browserApps[bowser.defaultBrowser][0] + ' is now the default browser')
        self.ui_update(self)
    def detectWebBrowsers(self):
        bowser.setup(False)
        messagebox.showinfo(title=None, message="Your installed web browsers have been scanned and updated.")
    def toggleBowser(self):
        if (self.bowserEnabled.get() == False): self.disableBowser() #After click so bool has already been inverted by checkbutton variable
        else: self.enableBowser()
    def disableBowser(self):
        bowser.setxdgDefaultWebBrowser(bowser.defaultBrowser)
        self.bowserEnabled.set(False)
        messagebox.showinfo(title=None, message="Bowser has been disabled and links will now open with " + bowser.browserApps[bowser.defaultBrowser][0] + ".")
    def enableBowser(self):
        bowser.setxdgDefaultWebBrowser()
        self.bowserEnabled.set(True)
        messagebox.showinfo(title=None, message="Bowser has been enabled, rules are active.")
    def toggleAskOnUmatchedURI(self):
        if (self.askOnUnmatchedURI.get() == False): #After click so bool has already been inverted by checkbutton variable
            bowser.askOnUnmatchedURI = False
        else:
            bowser.askOnUnmatchedURI = True
        bowser.saveConfig()

#MAIN
settingsApp = None
unmatchedApp = None
root = tk.Tk()
slave = None
def openUnmatchedURIDialog():
    global unmatchedApp, settingsApp, slave, root
    
    if (settingsApp != None):
        slave = tk.Toplevel(root)
        slave.attributes('-type', 'splash')
        slave.attributes('-alpha', '0.9')
        slave.attributes("-topmost", 1)
        #slave.attributes('-alpha', '0.7')
        slave.title('Bowser')
        slave.grid()
        unmatchedApp = tkUnmatchedURIDialog(slave)
    else:
        root.iconphoto(False, tk.PhotoImage(file=bowser.homePath+'/.config/bowser/bowser.png'))
        root.resizable(width=False, height=False)
        root.title('Bowser')
        root.attributes('-type', 'splash')
        root.attributes('-alpha', '0.9')
        root.attributes("-topmost", 1)
        unmatchedApp = tkUnmatchedURIDialog(root)
        unmatchedApp.grid()
        root.iconify()
        root.mainloop()


def start():
    global root, settingsApp, unmatchedApp
    root.iconphoto(False, tk.PhotoImage(file=bowser.homePath+'/.config/bowser/bowser.png'))
    root.resizable(width=False, height=False)
    root.title('Bowser')
    settingsApp = tkBowserSettings(root)
    settingsApp.grid()
    root.after(1000, bowser.checkURI)
    root.mainloop()
    
if __name__ == "__main__":
    print('Running bowser settings as main')
    bowser.bowserSettings = start
    import bowser as b

if __name__ == "bowserSettings":
    print('Settings module imported')
