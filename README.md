## Bowser for linux

Acts as the default web browser and allows you to set up rules to open specific URLs in specific web browsers.

### Installation

Run Bowser with python3 or bash to install:

 ```python3 bowser.py```

 ```./bowser.py```


### General Usage

Open Bowser from your desktop environments application menu, here you can create and manage rules.<br/>

Use the Settings menu to: enable/disable Bowser, set the default browser for links without rules or rescan for installed web browsers.<br/>

Use the File menu to export or import your rules and configuration from files for backup. Use the Help menu to find this readme.<br/>


![Bowser Settings GUI](doc/BowserGUI.png?raw=true "Screenshot of Bowser Settings GUI")

Select a rule and the web browser it opens with will show in the drop down box.<br/>
Choose another browser to make it the default for the selected rule.<br/>
Double click a rule to edit it. Use the Delete button to delete the selected rule<br/>
All changes are saved as they are made.<br/>


![Bowser Add Rule Dialog](doc/BowserAddRuleGUI.png?raw=true "Screenshot of Bowser Add Rule Dialog")

Use New Rule to create a rule, enter the text to search for and select which parts of the URL you would like for it to be searched in, default is the whole URL.


![Bowser Ask Rule Dialog](doc/BowserAskRuleGUI.png?raw=true "Screenshot of Bowser Add Rule Dialog")

If you enable 'Always ask' under the defaul browser menu, a popup with a list of browsers will show when opening a link without a rule.

A rule will be created for that domain for the browser you select. Select other parts of the URL to include them as well as the domain.

### CLI Usage
Open the Bowser rules settings window:

 ```python3 ~/.config/bowser/bowser.py``` OR
 
 ```python3 ~/.config/bowser/bowser.py --settings```

Runs initial setup again - rescans installed browsers and sets Bowser as the default:

 ```python3 ~/.config/bowser/bowser.py --setup```

Reset your default browser to handle all URLs:

 ```python3 ~/.config/bowser/bowser.py --disable```

Enable Bowser and sets rules to active:

 ```python3 ~/.config/bowser/bowser.py --enable```

### Support

This should work in most linux desktop environments.

May require dependencies:
```
sudo apt install python3 python3-tk
sudo yum install python3 python3-tkinter
```

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
