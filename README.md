## Bowser for linux

Acts as the default web browser and allows you to set up rules to open specific URLs in specific web browsers.

### Installation

Run Bowser with python3 to install:

 ```python3 bowser.py```


### General Usage

Open Bowser from your desktop environments application menu to change the rules, or see the CLI options below.

![Bowser Settings GUI](BowserGUI.png?raw=true "Screenshot of Bowser Settings GUI")

Select a rule and the web browser it opens with will show in the drop down box.

Choose another browser to make it the default for the selected rule.

Use the buttons to create and delete rules.

All changes are saved as they are made.

Use the File menu to Export or Import your rules configuration from files for backup.

Use the Settings menu to enable/disable Bowser, to detect installed web browsers, or to set the default browser for links without rules.

Use the Help menu to find this readme.



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

May require dependencies
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
