from tkinter import *
from tkinter import filedialog 

async def browse_directory(): 
    root = Tk()
    root.option_add('*background', 'white')  
    root.option_add('*activeBackground', 'grey')
    root.option_add('*foreground', 'black')  
    root.option_add('*activeForeground', 'black')
    root.withdraw()
    dir_name = filedialog.askdirectory() 
    return dir_name
