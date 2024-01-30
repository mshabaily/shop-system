from tkinter import END, X, Entry, Frame, Menu, messagebox
from settings import *

class Table:
    def __init__(self,objects,canvas):
        attributes = list(vars(objects[0]).keys())
        tableContainer = Frame(canvas, background= tableHighlight)
        canvas.create_window((0,0), width = canvas.winfo_reqwidth(), window = tableContainer, anchor = "nw")
        canvas.configure(background = canvasBackground)
        canvas.configure(highlightthickness = canvasBorderWidth, highlightbackground = canvasBorderColour)
        for row, item in enumerate(objects):
            rowContainer = Row(tableContainer)
            for column, attribute in enumerate(attributes):
                rowContainer.grid_columnconfigure(index=column, weight = 1)
                field = Item(rowContainer, item, attribute)
                field.grid(row = row, column = column)
            rowContainer.pack(fill=X, anchor = "nw", pady = 1)
        scrollableDepth = ((len(objects)+1) * field.winfo_reqheight())
        canvas.config(scrollregion = (0,0,0,scrollableDepth))

class Row(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, background= rowBorderColour, border = rowBorderWidth, **kwargs)
        self.menu = Menu(tearoff=False)
        self.menu.add_command(label = "Delete", command = self.delete)
        self.bind("<Button-3>", lambda event: self.popup())
    def delete(self):
        self.winfo_children()[0].item.forget()
        self.destroy()
    def popup(self):
        root = self.winfo_toplevel()
        self.menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())
    def bind_child(self,child):
        child.bind("<Button-3>", lambda event: self.popup())

def infoEntryHandler(event,object,attribute,field):
    global user
    if event.keysym == "Return" or event.keysym == "Escape":
        return
    if user.status != "staff":
        object.__setattr__(attribute,event.widget.get())
    else:
        messagebox.showerror("You do not have permission to change this")
        field.delete(0,END)
        field.insert(0,getattr(object,attribute))
        
class Item(Entry):
    def __init__(self, master, item, attribute, **kwargs):
        super().__init__(master, font = tableFont, background= rowBackground, **kwargs)
        self.item = item
        self.insert(0,getattr(item, attribute))
        response = lambda event, item = item, attribute = attribute, self = self: infoEntryHandler(event,item,attribute,self)
        self.bind("<KeyRelease>", response)
        master.bind_child(self)