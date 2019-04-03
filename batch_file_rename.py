import os
import re

import PySimpleGUI as sg

    
layout = [      

    [sg.Text('File name text to replace'),
        sg.Checkbox('Ignore case', key='ignoreCase'),
        sg.Checkbox('Regex', key='regex')],      
    [sg.InputText(key='findText', tooltip='Use START | END for prefix | suffix')],

    [sg.Text('Replacement text')],
    [sg.InputText(key='replaceText')],
    
    [sg.Text('Directory of files to be renamed'), 
        sg.Checkbox('Recurse directory', key='recurse'),],
    [sg.InputText(key='directory'), sg.FolderBrowse()],

    [sg.Submit(), sg.Cancel()],
    ] 

window = sg.Window('Batch File Rename', default_element_size=(60, 1), grab_anywhere=False).Layout(layout)      

event, values = window.Read()

print(event, values)

if event in (None, 'Cancel'):
    raise Exception('Operation cancelled by user')

findText = values['findText']
ignoreCase = values['ignoreCase']
regex= values['regex']
replaceText = values['replaceText']
directory = values['directory']
recurse = values['recurse']


def validRegexString(regexString):
    try:
        re.compile(regexString)
        return True
    except re.error:
        return False

def getNewFileName(fileName, method='REPLACE'):
    if method == 'START':
        return replaceText + fileName
    if method == 'END':
        name, ext = os.path.splitext(fileName)
        return name + replaceText + ext
    if method == 'REPLACE':
        ignore = re.IGNORECASE if ignoreCase else 0
        return re.sub(findText, replaceText, fileName, flags=ignore)
    else:
        raise ValueError('Unknown <method>')

if regex:
    if not validRegexString(findText):
        raise ValueError('Input is not a valid regular expression')

renamedFiles = 0

if recurse:
    for root, dirs, files in os.walk(directory):
        for f in files:
            new_f = getNewFileName(f)
            if f != new_f:
                os.rename(os.path.join(root, f), os.path.join(root, new_f))
                renamedFiles += 1
else:
    for f in os.listdir(directory):
        new_f = getNewFileName(f)
        if f != new_f:
            os.rename(os.path.join(directory, f), os.path.join(directory, new_f)) 
            renamedFiles += 1

layout = [      
    [sg.Text('Results: renamed {} files'.format(renamedFiles))],
    [sg.Ok()],
    ] 

window = sg.Window('Results', grab_anywhere=False).Layout(layout)      

event, values = window.Read()
