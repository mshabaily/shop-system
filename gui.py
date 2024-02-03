from tkinter import Tk, font, messagebox
from data import passwords, storeData
from settings import bodyFont

def updatePassword():
    for passwordData in passwords:
        if passwordData.employeeId == window.user.employeeId:
            passwordData.password = window.user.password

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

class User:
    def __init__(self, employeeId, name, password, status):
        self.employeeId = employeeId
        self.name = name
        self.password = password
        self.status = status

class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.user : User
        self.defaultFont = font.nametofont("TkTextFont")
        self.defaultFont.configure(family= bodyFont[0], size= bodyFont[1], weight=font.NORMAL)
        self.protocol("WM_DELETE_WINDOW", closeGUI)
        self.minsize(width = 500, height = 300)
    def clear(self):
        for child in self.winfo_children():
            child.destroy()

window = GUI()
window.title("Stock System")
window.geometry("900x600")