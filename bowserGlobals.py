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