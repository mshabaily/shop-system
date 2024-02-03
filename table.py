from tkinter import END, X, Entry, Frame, Label, Menu, messagebox
from settings import *
from gui import updatePassword, window

class Table(Frame):
    def __init__(self,objects,canvas,accessLevel):
        super().__init__()
        self.attributes = list(vars(objects[0]).keys())
        self.tableContainer = Frame(canvas, background= tableHighlight)
        self.canvas = canvas
        self.objects = objects
        self.accessLevel = accessLevel
    def load(self):
        self.canvas.create_window((0,0), width = self.canvas.winfo_reqwidth(), window = self.tableContainer, anchor = "nw")
        self.canvas.configure(background = canvasBackground)
        self.canvas.configure(highlightthickness = canvasBorderWidth, highlightbackground = canvasBorderColour)
        for row, item in enumerate(self.objects, 0):
            rowContainer = Row(self.tableContainer, item, self)
            for column, attribute in enumerate(self.attributes):
                rowContainer.grid_columnconfigure(index=column, weight = 1)
                if row == 0:
                    header = Label(master = rowContainer, text = attribute, font = bodyFont, bg = appColour)
                    header.grid(row = 0, column = column)
                field = Item(rowContainer, item, attribute, self.accessLevel)
                field.grid(row = row+1, column = column)
            rowContainer.pack(fill=X, anchor = "nw", pady = 1)
        objectCount = len(self.objects)+1
        offsetDepth = (objectCount * canvasBorderWidth) + Label(font = bodyFont).winfo_reqheight() + (canvasBorderWidth *2)
        scrollableDepth = (objectCount * field.winfo_reqheight()) + offsetDepth
        self.canvas.config(scrollregion = (0,0,0,scrollableDepth))
        self.menu = Menu(tearoff=False)
        self.menu.add_command(label = "Add Row", command = self.add)
        self.canvas.bind("<Button-3>", lambda event: self.popup())
    def popup(self):
        root = self.winfo_toplevel()
        self.menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())
    def clear(self):
        for child in self.tableContainer.winfo_children():
            child.destroy()
    def add(self):
        newObj = type(self.objects[0])
        newObj([]).save()
        self.clear()
        self.load()
        
class Row(Frame):
    def __init__(self, master, item, table, **kwargs):
        super().__init__(master, background= rowBorderColour, border = rowBorderWidth, **kwargs)
        self.menu = Menu(tearoff=False)
        self.menu.add_command(label = "Add Row", command = table.add)
        self.menu.add_command(label = "Delete Row", command = lambda item = item : self.delete(item))
        self.bind("<Button-3>", lambda event: self.popup())
    def delete(self, item):
        print(item)
        item.__del__()
        self.destroy()
    def popup(self):
        root = self.winfo_toplevel()
        self.menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())
    def bind_child(self,child):
        child.bind("<Button-3>", lambda event: self.popup())

def infoEntryHandler(event,object,attribute):
    if event.keysym == "Return" or event.keysym == "Escape":
        return
    if window.user.status != "staff" or event.widget.accessLevel == "open":
        object.__setattr__(attribute,event.widget.get())
        updatePassword()
    else:
        messagebox.showerror("You do not have permission to change this")
        event.widget.delete(0,END)
        event.widget.insert(0,getattr(object,attribute))
        
class Item(Entry):
    def __init__(self, master, item, attribute, accessLevel, **kwargs):
        super().__init__(master, font = tableFont, background= rowBackground, **kwargs)
        self.accessLevel = accessLevel
        self.insert(0,getattr(item, attribute))
        response = lambda event, item = item, attribute = attribute : infoEntryHandler(event,item,attribute)
        self.bind("<KeyRelease>", response)
        master.bind_child(self)