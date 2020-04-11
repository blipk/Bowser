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

#GLOBALS
from os.path import expanduser
homePath = expanduser("~")
config = {}
browserApps = {}
uriPrefs = {}
defaultBrowser = ''
askOnUnmatchedURI = bool()
openAskBrowser = False
URI = ''
bowserSettings = None

import re
def splitURI(inURI):
    regexPattern = ("^(?P<s1>(?P<s0>[^:/\?#]+):)?(?P<a1>" 
                    "//(?P<a0>[^/\?#]*))?(?P<p0>[^\?#]*)" 
                    "(?P<q1>\?(?P<q0>[^#]*))?" 
                    "(?P<f1>#(?P<f0>.*))?")
    regex = re.compile(regexPattern)
    output = regex.match(inURI)

    if (output.group('a1') == None):     #Regex isn't perfect if there's no scheme
        inURI = 'foo://' + inURI
        output = regex.match(inURI)
        
    splitURI = {'scheme': output.group('s1'), 'schemeNoTrim': output.group('s0'), 
                'authority': output.group('a1'), 'authorityNoTrim': output.group('a0'), 
                'path': output.group('p0'), 
                'query': output.group('q1'), 'queryNoTrim': output.group('q0'), 
                'fragment': output.group('f1'), 'fragmentNoTrim': output.group('f1')}
    
    if (splitURI['scheme'] == 'foo:'):
        splitURI['scheme'] = ''
        inURI = inURI[6:len(inURI)]
    
    return splitURI