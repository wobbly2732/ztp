import PySimpleGUI as sg
import json
import webbrowser
import requests
import sys

Arrayname = ''

def extractdata():
    global Arrayname
    filename = values['-JSONfile-']
    with open(filename, 'r') as f:
        rdr = json.loads(f.read())
        print('Target Array Name: ',rdr['array_name'])
        Arrayname = rdr['array_name']
        f = open(Arrayname + '.txt', 'x')
        f.write('\nInitialization json file:\n' + repr(rdr) +'\n')
        f.close()
        return Arrayname

def arraystatus(Arrayname):
    IPaddress = values['-IPADDRESS-']
    URL = 'https://pureapisim.azurewebsites.net/api/array-initial-config' #testing api endpoint
    #URL = 'http://'+ IPaddress +':8081/array-initial-config'
    response = requests.get(URL)
    response2 = json.loads(response.text)
    f = open(Arrayname + '.txt', 'a' )
    f.write('\nConnection to Unitialised Array Successful\n' + repr(response) +'\n')
    f.write('\nUnitialised Array State:\n' + repr(response2) +'\n')
    f.close() 
    if response.status_code == 200:
        print('connection successful, please continue')
        
    else:
        print('Check connection to array then try again')    

def provisionarray():
    IPaddress = values['-IPADDRESS-']
    filename = values['-JSONfile-']
    URL = 'https://pureapisim.azurewebsites.net/api/array-initial-config' #testing api endpoint
    #URL = 'http://'+ IPaddress +':8081/array-initial-config'
    with open(filename, 'r') as f:
        response = requests.patch(URL, data=filename)
        response2 = json.loads(response.text)
        if response.status_code == 200:
            print('Initialisation Successful, please continue')
            f = open(Arrayname + '.txt', 'a' )
            f.write('\nInitialisation Successful\n' + repr(response) + '\n')
            f.write('\nInitialised Array State:\n' +repr(response2) + '\n')
            f.close()
        else:
            return

def openGUI(Arrayname):
    IPaddress = values['-IPADDRESS2-']
    URL = 'http://'+ IPaddress
    webbrowser.open_new_tab(URL)
    f = open(Arrayname + '.txt', 'a' )
    f.write('\nOpened default browser window to FlashArray GUI at http://' + IPaddress + '\n')
    f.write('\nZero Touch Provisioning of array ' + Arrayname + ' Complete')
    f.close()

sg.theme_background_color('#EE6129')
sg.theme_element_background_color('#EE6129')
sg.theme_text_element_background_color('#EE6129')

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Open', '&Save', 'E&xit']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text('Zero Touch Provisioning Tool', size=(50, 1), justification='center', font=('Ariel', 25, 'bold'))],
    [sg.Text('Simply follow the numbers steps to complete the initialization of your new array\n', justification = 'left', font=('Ariel', 15, 'bold'))],
    [sg.Text('Enter the DHCP assigned IP address of the array', size=(50,1), justification='left'), sg.InputText(default_text='xxx.xxx.xxx.xxx', size=(15,1), key='-IPADDRESS-')],
    [sg.Text('Enter the IP address for ct0.eth0', size=(50,1), justification='left'), sg.InputText(default_text='xxx.xxx.xxx.xxx', size=(15,1), key='-IPADDRESS2-')],
    [sg.Text('1. Import JSON File', justification='left'),
     sg.InputText('JSON File', size=(40,1)), sg.FileBrowse(key='-JSONfile-')],
    [sg.Output(size=(40,1), font=('Ariel', 10, 'bold', 'italic'))],
    [sg.Button(button_text='2. Connect to Array', size=(20,1))],
    [sg.Button(button_text='3. Provision Array', size=(20,1))],
    [sg.Button(button_text='4. Connect to Array GUI', size=(20,1))]]

window = sg.Window('Pure Storage ZTP v0.2 Draft', layout, text_justification='center', default_element_size=(5, 1), grab_anywhere=False)

while True:
    event, values = window.read()
    if event == '2. Connect to Array':
        print('Connecting to Unitialized Array' , values['-IPADDRESS-'])
        extractdata()
        arraystatus(Arrayname)
    elif event == '3. Provision Array':
        print('Provisioning Array' , values['-IPADDRESS-'])
        provisionarray()
    elif event == '4. Connect to Array GUI':
        print('Connecting to Initialized Array' , values['-IPADDRESS2-'])
        openGUI(Arrayname)
        sys.exit()
    else:
        break
            
sys.exit()