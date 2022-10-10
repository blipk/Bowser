# Bowser for linux

Create rules to open specific websites in specific web browsers for links clicked in any application on your computer.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/deltadevelopments)
[![Website](https://img.shields.io/badge/Bowser-Homepage-blue)](https://github.com/blipk/Bowser)


### Installation

###### Desktop
Double Click the 'Install Bowser' desktop file.

###### Command Line
Run Bowser with python3 or bash to install:<br/>
 ```./bowser.py``` &nbsp;```OR```<br/>
 ```python3 bowser.py```  

### General Usage

To manage rules and settings, open Bowser from your desktop application menu or with the Bowser icon in the new link menu.<br/>

Bowser will create new rules for you as you open links.<br/>
This can be disabled in:```Settings Menu -> Create rules on new links```<br/>

##### When you open a link

![Bowser Ask Rule Dialog](doc/BowserAskRuleGUI.png?raw=true "Screenshot of Bowser Add Rule Dialog")
<br/>
A list of your web browsers will show, choose which browser you want the website to open with from now on.<br>
You can also choose which parts of the web address to include, the default is only the website name.<br/>

##### Managing Rules

![Bowser Settings GUI](doc/BowserGUI.png?raw=true "Screenshot of Bowser Settings GUI")
![Bowser Settings GUI](doc/BowserGUI2.png?raw=true "Screenshot of Bowser Settings GUI")
<br/>
 Select a rule and the web browser it opens with will show in the drop down box, changing it will apply it to that rule.<br/>
 Double click a rule to edit it. ```Delete Rule``` will delete the selected rule. ```New Rule``` will let you create a rule.<br/>


##### Creating/Editing Rules

![Bowser Add Rule Dialog](doc/BowserAddRuleGUI.png?raw=true "Screenshot of Bowser Add Rule Dialog")
<br/>

Enter the text to search for and select which parts of the URL you would like for it to be searched in.

##### Menu Options
```File Menu -> Export Configuration```&nbsp; Save your rules and settings for later<br/>
```File Menu -> Import Configuration```&nbsp; Load rules and settings from before<br/>
```Settings Menu -> Bowser is Enabled/Disabled```&nbsp; Turn Bowser on/off: <br/>
```Settings Menu -> Create rules on new links```&nbsp; Turn the popup menu for new links on/off<br/>
```Settings Menu -> Default Web Browser -> [Web Browser]```&nbsp; Open unmatched links with this browser when popup is disabled<br/>
```Settings Menu -> Detect installed web browsers```&nbsp; Update which web browsers Bowser knows:<br/>
```Help Menu -> About```&nbsp; Find this page<br/>

### CLI Usage 

Open the Bowser rules settings window:<br/>
 ```python3 ~/.config/bowser/bowser.py``` &emsp; ```OR```<br/>
 ```python3 ~/.config/bowser/bowser.py --settings```

Runs initial setup again - rescans installed browsers and sets Bowser as the default:<br/>
 ```python3 ~/.config/bowser/bowser.py --setup```

Reset your default browser to handle all URLs:<br/>
 ```python3 ~/.config/bowser/bowser.py --disable```

Enable Bowser and sets rules to active:<br/>
 ```python3 ~/.config/bowser/bowser.py --enable```

### Support

This should work in most linux desktop environments.<br/>
May require these dependencies in some environments.<br/>
```sudo apt install python3 python3-tk ``` ```or``` <br/>
```sudo yum install python3 python3-tkinter```

### Licence

```
This file is part of the Bowser linux application
Copyright (C) 2020 A.D.
```

```
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
