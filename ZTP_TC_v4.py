import PySimpleGUI as sg, json, webbrowser, requests, sys, os

Arrayname = ''
IP1 = ''
IP2 = ''
Filename = ''
FlashArray = ''
FlashBlade = ''

def FAextractdata():
    global Arrayname
    global JSONfile
    with open(JSONfile, 'r') as f:
        rdr = json.loads(f.read())
        print('Target Array Name: ',rdr['array_name'])
        Arrayname = rdr['array_name']
        try:
            f = open(Arrayname + '.txt', 'x')
        except FileExistsError:
            os.rename(Arrayname + '.txt', Arrayname + '.old')
            f = open(Arrayname + '.txt', 'x')
        f.write('\nFlashArray Provisioning Selected\nArray: ' + (Arrayname))
        f.write('\nInitialization json file:\n' + repr(rdr) +'\n')
        f.close()
        return Arrayname, JSONfile
    

def FAarraystatus(Arrayname):
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
        print('Connection Successful, please continue')
    
    elif response.status.code == 112:
        print('Array still starting, retry connecting to array')
        
    else:
        print('Check connection to array then try again')    

def FAprovisionarray():
    IPaddress = values['-IPADDRESS-']
    filename = values['-JSONfile-']
    URL = 'https://pureapisim.azurewebsites.net/api/array-initial-config' #testing api endpoint
    #URL = 'http://'+ IPaddress +':8081/array-initial-config'
    with open(filename, 'r') as f:
        response = requests.patch(URL, data=filename)
        response2 = json.loads(response.text)
        if response.status_code == 200:
            print('Provisioning Successful, please continue')
            f = open(Arrayname + '.txt', 'a' )
            f.write('\nProvisioning Successful\n' + repr(response) + '\n')
            f.write('\nProvisioned Array State:\n' +repr(response2) + '\n')
            f.close()
        else:
            return

def FAopenGUI(Arrayname):
    IPaddress = values['-IPADDRESS2-']
    URL = 'http://'+ IPaddress
    webbrowser.open_new_tab(URL)
    f = open(Arrayname + '.txt', 'a' )
    f.write('\nOpened default browser window to FlashArray GUI at http://' + IPaddress + '\n')
    f.write('\nZero Touch Provisioning of array ' + Arrayname + ' Complete')
    f.close()
    print('Zero Touch Provisioning of array ' + Arrayname + ' Complete\nPress any key to close')

    
def FA(JSONfile, IP1, IP2):
    if event == '2. Connect to Array':
        print('JSON file Import Successful\nConnecting to Unitialized Array', IP1)
        FAextractdata()
        FAarraystatus(Arrayname)
    elif event == '3. Provision Array':
        print('Provisioning Array' , IP2)
        FAprovisionarray()
    elif event == '4. Connect to Array GUI':
        print('Connecting to Initialized Array' , IP2)
        FAopenGUI(Arrayname)
    else:
        return

def FlashBlade():
    return

sg.theme_background_color('#EE6129')
sg.theme_element_background_color('#EE6129')
sg.theme_text_element_background_color('#EE6129')

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Open', '&Save', 'E&xit']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

col1 = [[sg.Text('Zero', size=(25, 1), justification='center', text_color=('#EE6129'))],
    [sg.Text('Select Array Type to provision', size=(40,1), justification='left'), sg.Radio('FlashArray', 'RADIO1', enable_events=True, key='-FLASHARRAY-'),
    sg.Radio('FlashBlade', 'RADIO1', enable_events=True, key='-FLASHBLADE-')], 
    [sg.Text('Enter the DHCP assigned IP address of the array', size=(50,1), justification='left'), sg.InputText(default_text='xxx.xxx.xxx.xxx', size=(15,1), key='-IPADDRESS-')],
    [sg.Text('Enter the IP address for ct0.eth0', size=(50,1), justification='left'), sg.InputText(default_text='xxx.xxx.xxx.xxx', size=(15,1), key='-IPADDRESS2-')],
    #[sg.Text('1. Import JSON File', justification='left'), sg.InputText('JSON File', size=(40,1)), 
    [sg.FileBrowse(key='-JSONfile-',button_text='1. Import JSON file', size=(20,1)),
    sg.Button(button_text='2. Connect to Array', size=(20,1),)],
    [sg.Button(button_text='3. Provision Array', size=(20,1)),
    sg.Button(button_text='4. Connect to Array GUI', size=(20,1))]]

col2 = [[sg.Text('Zero', size=(5, 1), justification='center', text_color=('#EE6129'))]]
        
col3 = [[sg.Image(r'./WEB-X-Centered.png')], [sg.Image(r'./WEB-FB-Centered.png')]]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text('Zero Touch Provisioning Tool', size=(50, 1), justification='center', font=('Ariel', 25, 'bold'))],
    [sg.Text('Simply follow the numbers steps to complete the initialization of your new array\n', justification = 'left', font=('Ariel', 15, 'bold'))],
    [sg.Column(col1), sg.Column(col2), sg.Column(col3)],
    [sg.Output(size=(103,10), font=('Ariel', 10, 'bold', 'italic'))]]

window = sg.Window('Pure Storage ZTP v0.2 Draft', layout, text_justification='center', default_element_size=(5, 1), grab_anywhere=False)

while True:
    event, values = window.read()
    if values['-FLASHARRAY-']:
        print('FlashArray Provisioning Selected')
        JSONfile = values['-JSONfile-']
        IP1 = values['-IPADDRESS-']
        IP2 = values['-IPADDRESS2-']
        FA(JSONfile, IP1, IP2)
    elif values['-FLASHBLADE-']:
        print('FlashBlade Provisioning Selected')
        FlashBlade()
    else:
        print('Select type of Array to be provisioned')
        True
            
sys.exit()