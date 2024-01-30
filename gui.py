from tkinter import Tk, font
from data import storeData
from settings import bodyFont

class GUI(Tk):
    def __del__(self):
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
    def __init__(self):
        super().__init__()
        self.authority : str
        self.defaultFont = font.nametofont("TkTextFont")
        self.defaultFont.configure(family= bodyFont[0], size= bodyFont[1], weight=font.NORMAL)
    def clear(self):
        for child in self.winfo_children():
            child.destroy()

window = GUI()
window.title("Stock System")
window.geometry("900x600")