import os
import filevisitor

class FileChecker(filevisitor.CodeChecker):
    def __init__(self, string):
        filevisitor.CodeChecker.__init__(self)
        self.string = string
        self.files = []
    def visit(self, filepath):
        fp = open(filepath, 'r')
        hits = 0
        for line in fp:
            if line.lstrip().startswith('//'):
                continue
            if self.string in line:
                hits += 1
        #text = fp.read()
        #fp.close()
        #hits = text.count(self.string)
        if hits > 0:
            self.files.append(filepath)
        return hits

allnames = '''ShowFatalError
ShowSevereError
ShowSevereMessage
ShowContinueError
ShowContinueErrorTimeStamp
ShowMessage
ShowWarningError
ShowWarningMessage
ShowRecurringSevereErrorAtEnd
ShowRecurringWarningErrorAtEnd
ShowRecurringContinueErrorAtEnd
StoreRecurringErrorMessage
ShowErrorMessage
SummarizeErrors
ShowRecurringErrors'''

startnames = '''ShowFatalError
ShowSevereError
ShowSevereMessage
ShowMessage
ShowWarningError
ShowWarningMessage
ShowErrorMessage'''

continuenames = '''ShowContinueError
ShowContinueErrorTimeStamp'''

headercalls = '''ShowContinueError
ShowSevereError
ShowWarningError'''.splitlines()

lowcalls = '''ShowSevereMessage
ShowErrorMessage'''.splitlines()

path = '../../src/EnergyPlus/'

fp = open('results.csv','w')

for fcn in allnames.splitlines():
    checker = FileChecker(fcn)
    checker.execute(path)
    hh = 0
    for file in checker.files:
        if file.endswith('.hh'):
            hh += 1
    fp.write('%s,%d,%d,%d\n' % (fcn, checker.count, len(checker.files)-hh, hh))
    print('%s,%d,%d,%d' % (fcn, checker.count, len(checker.files)-hh, hh))
    if fcn in headercalls:
        for file in checker.files:
            if file.endswith('.hh'):
                print('\t',file)
    if fcn in lowcalls:
        for file in checker.files:
            print('\t',file)

fp.close()
