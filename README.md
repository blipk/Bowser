# Bowser for linux

Create rules to open specific websites in specific web browsers for links clicked in any application on your computer.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/deltadevelopments)
[![Website](https://img.shields.io/badge/Bowser-Homepage-blue)](https://github.com/blipk/Bowser)


### Installation

###### Desktop
Double Click the 'Install Bowser' desktop file.

###### Command Line
Run Bowser with python3 or bash to install:<br/>
 ```./bowser.py``` &nbsp;&nbsp; ```OR```<br/>
 ```python3 bowser.py```  

### General Usage

To manage rules and settings, open Bowser from your desktop application menu or with the Bowser icon in the new link menu.<br/>

Bowser will create new rules for you as you open links.<br/>
This can be disabled in:&nbsp; ```Settings Menu -> Create rules on new links```<br/>

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
Save your rules and settings for later:&nbsp; ```File Menu -> Export Configuration```<br/>
Load rules and settings from a file:&nbsp; ```File Menu -> Import Configuration```<br/>
Turn Bowser on/off: &nbsp; ```Settings Menu -> Bowser is Enabled/Disabled```<br/>
Turn the popup menu for new links on/off:&nbsp; ```Settings Menu -> Create rules on new links```<br/>
Open unmatched links with this browser when popup is disabled:&nbsp; ```Settings Menu -> Default Web Browser -> [Web Browser]```<br/>
Update which web browsers Bowser knows:&nbsp; ```Settings Menu -> Detect installed web browsers```<br/>
Find this page:&nbsp; ```Help Menu -> About```<br/>

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
```sudo apt install python3 python3-tk ``` &nbsp; ```or``` <br/>
```sudo yum install python3 python3-tkinter```

### Licence

```
This file is part of the Bowser linux application
Copyright (C) 2020 A.D. - http://kronosoul.xyz
```

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope this it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```
