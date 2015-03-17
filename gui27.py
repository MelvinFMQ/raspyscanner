__author__ = 'melvinfoo'
from Tkinter import *
from controlcomputer import *
#import Tkinter.messagebox

def startScanButton(event):
    start_scan()

def shutDownButton(event):
    shut_down()

def restartButton(event):
    reboot()

def updateSofwareButton(event):
    update()

def about():
    pass

root = Tk()

menu = Menu(root)
root.config(menu= menu)
#Tkinter.messagebox.showinfo('Window Title', 'Hi')

#menu
subMenu= Menu(menu)
menu.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label='About', command=about)

#scanning controls
labelScan = Label(root, text='Name of the scan:')
entryScan = Entry(root)
buttonScan = Button(root, text="Start Scan", bg="green")

#Update, shutdown, restart
buttonUpdate = Button(root, text="Update Raspberry Pi server software", bg="red")
buttonShutDown = Button(root, text="Shutdown Raspberry Pis", bg="red")
buttonRestart = Button(root, text="Restart Raspberry Pis", bg="red")

#Custom command controls
labelCustomCommand = Label(root, text='Type your command here:')
buttonCustomCommand = Button(root, text="Submit a custom command")
entryCustomCommand = Entry(root)

#status bar
status = Label(root, text='This is the status bar', anchor=W, relief=SUNKEN)

#bind buttons
buttonScan.bind("<Button-1>", startScanButton)
buttonUpdate.bind("<Button-1>", updateSofwareButton)
buttonRestart.bind("<Button-1>", restartButton)
buttonShutDown.bind("<Button-1>", shutDownButton)

#layout
labelScan.grid(row=0, sticky=E, pady=5)
entryScan.grid(row=0, column=1, pady=5)
buttonScan.grid(row=0, column=2, pady=5, sticky=W)

buttonShutDown.grid(row=1, pady=5, padx=5)
buttonRestart.grid(row=1, column=1, pady=5, padx=5)
buttonUpdate.grid(row=1, column=2, pady=5, padx=5)

labelCustomCommand.grid(row=2, sticky=E, pady=5)
buttonCustomCommand.grid(row=2, column=2, pady=5)
entryCustomCommand.grid(row=2, column=1, pady=5, sticky=W)

status.grid(row=3)
root.mainloop()


