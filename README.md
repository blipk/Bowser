## Bowser for linux

Set up rules to open specific URLs in specific web browsers.

### Installation

Run the provided shell script to install Bowser

 ```./install.sh```

### General Usage
Bowser will open after running the installer script, from there you can set up rules. 

To open the rules settings again, open Bowser from your desktop environments application menus, or see the CLI options below.

![Bowser Settings GUI](SettingsGUI.png?raw=true "Screenshot of Bowser Settings GUI")

Select a rule and the web browser it opens with will show in the drop down box, 
choose another browser to make it the default for that rule.

Use Add/Delete to open a dialog to create a new rule, or delete the currently selected rule
Use the Import/Export buttons to save and load your rule configurations

All changes are saved as they are done.

### CLI Usage
Open the Bowser rules settings window:

 ```python3 ~/.config/bowser/bowser.py``` OR
 
 ```python3 ~/.config/bowser/bowser.py --settings```

Runs initial setup again - rescans installed browsers and set Bowser as the default:

 ```python3 ~/.config/bowser/bowser.py --setup```

Reset your default browser to handle all URLs:

 ```python3 ~/.config/bowser/bowser.py --reset```

### Support

This should work in most linux desktop environments.

There are some dependencies which the install script should cover.

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
