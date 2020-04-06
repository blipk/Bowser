## Bowser for linux

Set up rules to open specific URLs in specific web browsers.

### Installation

Run the provided shell script to install Bowser
 ```./install.sh```

### General Usage
Bowser will open after running the installer script, from there you can set up rules. To open the rules settings window again, just open Bowser from your desktop environments application menus, or see the CLI options below.

![Bowser Settings GUI](SettingsGUI.png?raw=true "Screenshot of Bowser Settings GUI")
Select a rule and the browser it opens with will show in the drop down box, 
choose another browser to make it the default for that rule.

Use Add/Delete to open a dialog to create a new rule, or delete the currently selected rule
Use the Import/Export buttons to save and load your rule configurations

### CLI Usage
To open the Bowser rules settings window.
 ```python3 ~/.config/bowser/bowser.py```
 ```python3 ~/.config/bowser/bowser.py --settings```

To rescan browsers and set Bowser as the default - this is done the first time the application runs
 ```python3 ~/.config/bowser/bowser.py --setup```

to reset your default browser to handle all URLs
 ```python3 ~/.config/bowser/bowser.py --reset```

### Support

This should work in most linux desktop environments.
Has some dependencies which the install script should cover.

### Licence
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
