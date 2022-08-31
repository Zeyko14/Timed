import PySimpleGUI as sg # Docs : https://www.pysimplegui.org/en/stable/
import datetime
import pygame

# Variables | region
reset_timer_end = datetime.datetime(2007,2,14)
timer_end = reset_timer_end
timer = '00:00'
# endregion

# Lists | region
TYPE_LIST = ['', 'Lesson', 'Workout']
tasks_list = []
tasks_dict = [
    {'task':'Break', 'timer':5*60},
    {'task':'Lesson', 'timer':25*60},
    {'task':'Workout', 'timer':15*60}
]
seconds_list = []
for i in range(60):
    seconds = f'0{str(i)}' if len(str(i)) == 1 else str(i)
    seconds_list.append(seconds)
minutes_list = []
for i in range(60):
    minutes = f'0{str(i)}' if len(str(i)) == 1 else str(i)
    minutes_list.append(minutes)
RINGTONES = ['./sounds/sunflower.mp3'] # Add a feature to add ringtones within the app
# endregion

# Functions | region
def get_time(formated=True):
    if formated:
        return datetime.datetime.now().strftime('%H:%M:%S')
    else:
        return datetime.datetime.now()
def get_date():
    return datetime.datetime.now().strftime('%d/%m/%Y')
def new_timer(add_seconds=0):
    return datetime.datetime.now() + datetime.timedelta(seconds=add_seconds)
def check_type():
    task_type = 'Lesson'
    length = 25
    return task_type, length
def open_main_window():
    global reset_timer_end
    global timer_end
    global timer

    menu_def = [['&Timed', ['&Settings', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Debugger', ['Popout', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...']]

    layout = [
        [sg.Menu(menu_def)],
        [
            sg.Text(text='', expand_x=True, justification='left', font=('Courier', 18, 'bold'), key='-DATE-'),
            sg.Text(text='', expand_x=True, justification='right', font=('Courier', 18, 'bold'), key='-TIME-')
        ],
        [sg.HSeparator()],
        [sg.Text(text='', expand_x=True, justification='center', font=('Courier', 69, 'bold'), pad=(100, 100), key='-TIMER-')],
        [sg.HSeparator()],
        [
            sg.Button('Start', font=('Courier', 14, 'bold'), key='-START_TIMER-'),
            sg.Button('Stop', font=('Courier', 14, 'bold'), key='-STOP_RINGTONE-'), 
            sg.Frame('', 
            [
                [
                    sg.Combo(minutes_list, font=('Courier', 18, 'bold'), default_value='00', readonly=True, key='-MINUTES-'), 
                    sg.Combo(seconds_list, font=('Courier', 18, 'bold'), default_value='00', readonly=True, key='-SECONDS-')
                ]
            ], 
            border_width=0, element_justification='right', expand_x=True)
        ],
        [
            sg.Listbox(values=tasks_list, font=('Courier', 14, 'bold'), expand_x=True, size=(None, 10), key='-LIST-')
        ],
        [
            sg.Text('Task:', font=('Courier', 18, 'bold')), 
            sg.Input(font=('Courier', 18, 'bold'), size=(0, None), expand_x=True, key='-TASK-'),
            sg.Combo(values=TYPE_LIST, font=('Courier', 18, 'bold'), readonly=True, key='-TYPE-'), 
            sg.Button('Add', font=('Courier', 14, 'bold'), key='-ADD-')
        ]
    ]

    window = sg.Window('Timed', layout)

    while True:
        event, values = window.read(timeout=1)
        
        if event in [None, 'Exit']:
            break
        if event == '-ADD-':
            if values['-TYPE-']:
                if values['-TASK-']:
                    tasks_list.append(values['-TASK-'] + " " + values['-TYPE-'])
                else:
                    tasks_list.append(values['-TYPE-'])
                timer_end = tasks_dict.get('timer')
            elif values['-TASK-']:
                tasks_list.append(values['-TASK-'])
            window['-LIST-'].update(values=tasks_list)
            window['-TASK-'].update('')
        if event == '-START_TIMER-':
            timer_end = new_timer(60*int(values['-MINUTES-'])+int(values['-SECONDS-'])+1)
            timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])
        if event == '-STOP_RINGTONE-':
            timer_end = reset_timer_end
            timer = '00:00'
            pygame.mixer.music.stop()
        if event == 'Settings':
            settings_window = open_settings_window()

        local_time = get_time()
        local_date = get_date()
        if timer != '00:00':
            timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])
        if get_time() == timer_end.strftime('%H:%M:%S'):
            timer_end = reset_timer_end
            pygame.mixer.music.play()
        if values['-MINUTES-'] == '00' and values['-SECONDS-'] == '00':
            window['-SECONDS-'].update('01')

        window['-DATE-'](local_date)
        window['-TIME-'](local_time)
        window['-TIMER-'](timer)
    window.close()
def open_settings_window():
    layout = [[sg.Combo(RINGTONES, size=(None, 10), key='-RINGTONE-'), sg.Button('Apply', key='-SET_RINGTONE-')]]
    window = sg.Window('Settings', layout)
    while True:
        event, values = window.read()
        if event is None: break
    window.close()
# endregion

# PyGame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(RINGTONES[0])

# PySimpleGUI
sg.theme('Black')

open_main_window()