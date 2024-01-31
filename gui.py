from tkinter import Tk, font, messagebox
from data import storeData
from settings import bodyFont

def saveFiles():
    for data in storeData:
        file = open(data[0].getPath(), "w")
        for object in data:
            attributes = list(vars(object).keys())
            for attribute in attributes:
                file.write(getattr(object, attribute, "none"))
                file.write(",")
            if data.index(object) != len(data):
                file.write("\n")
        file.close()

def closeGUI():
    if messagebox.askyesno("Quit", "Save changes?"):
        saveFiles()
    window.destroy()

class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.authority : str
        self.defaultFont = font.nametofont("TkTextFont")
        self.defaultFont.configure(family= bodyFont[0], size= bodyFont[1], weight=font.NORMAL)
        self.protocol("WM_DELETE_WINDOW", closeGUI)
    def clear(self):
        for child in self.winfo_children():
            child.destroy()

window = GUI()
window.title("Stock System")
window.geometry("900x600")