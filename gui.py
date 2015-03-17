from tkinter import *

root = Tk()

topFrame = Frame(root)
topFrame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

buttonShoot = Button(topFrame, text='Shoot photo', fg='green')
buttonShoot.pack()

root.mainloop()


