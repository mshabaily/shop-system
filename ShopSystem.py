#Tkinter libraries are imported
from tkinter import CENTER, E, X, Button, Canvas, Entry, Frame, Label, Menu, Menubutton, OptionMenu, PhotoImage, Scrollbar, StringVar, Tk, messagebox
from os import listdir
from dataClasses import *

profit = 0
stock = []
employees = []
images = dict()

class GUI(Tk):
    def __del__(self):
        saveFiles()
    def __init__(self):
        super().__init__()
    def clear(self):
        for child in self.winfo_children():
            child.destroy()

#Window is opended and set to fullscreen
window = GUI()
window.title("Stock System")
window.geometry("900x600")
window.configure(bg = "lightGray")

mainFont = ("roboto",10)
titleFont = ("roboto",15)
bigFont = ("roboto,",20)

mainCanvas = Canvas()

def createDefaultCanvas():
    global mainCanvas
    try:
        mainCanvas.destroy()
    except:
        pass
    mainCanvas = Canvas(window, background = "gray", width = 1000, height = 2000)
    scrollbar = Scrollbar(window, orient = "vertical", command = mainCanvas.yview)
    scrollbar.config(command = mainCanvas.yview)
    scrollbar.place(relx = 1, rely = 0.5, anchor = E, relheight=1)
    mainCanvas.config(yscrollcommand=scrollbar.set)
    mainCanvas.grid_propagate(False)
    mainCanvas.pack(pady = 50, anchor=CENTER, expand = True)

#Subroutine callable to save 2D arrays into text files
def saveFiles():
    global employees, stock
    arrays = [employees, stock]
    for array in arrays:
        file = open(array[0].getPath(), "w")
        for object in array:
            attributes = list(vars(object).keys())
            for attribute in attributes:
                file.write(getattr(object, attribute, "none"))
                file.write(",")
            file.write("\n")
        file.close()

#Function callable to return 2D arrays, populated based on text files
def loadFiles():
    global deliveries, employees, stock
    for classFile in listdir("classes"):
        file = open("classes/" + classFile)
        while True:
            line = file.readline().rstrip('\n')
            if line == "":
                break
            fields = line.split(",")
            if file.name == "classes/employees.txt":
                employees.append(EmployeeData(fields))
            elif file.name == "classes/stock.txt":
                stock.append(StockData(fields))
        file.close()

def loadImages():
    global images
    for imagePath in listdir("images"):
        image = PhotoImage(file = "images/" + imagePath)
        image = image.subsample(5)
        images.update({imagePath : image})

#Subroutine callable to display errors
def error(errorMessage):
    messagebox.showerror(title = "Error", message = errorMessage)

def infoEntryHandler(event,object,attribute):
    object.__setattr__(attribute,event.widget.get())

def formatTable(objects):
    global mainCanvas
    attributes = list(vars(objects[0]).keys())
    fieldsContainer = Frame(mainCanvas)
    headersContainer = Frame(mainCanvas)
    mainCanvas.create_window((0,0), width = mainCanvas.winfo_reqwidth(), window = headersContainer, anchor = "nw")
    mainCanvas.create_window((0,0), width = mainCanvas.winfo_reqwidth(), window = fieldsContainer, anchor = "nw")
    for column, attribute in enumerate(attributes):
        header = Label(headersContainer, text = attribute)
        header.grid(row = 0, column = column)
        headersContainer.grid_columnconfigure(index=column, weight = 1)
        fieldsContainer.grid_columnconfigure(index=column, weight = 1)
        for row, object in enumerate(objects):
            field = Entry(fieldsContainer)
            field.insert(0,getattr(object, attribute))
            field.bind("<KeyRelease>", 
                 lambda event,object = object, attribute = attribute: infoEntryHandler(event,object,attribute))
            field.grid(row = row, column = column)
    scrollableDepth = (len(objects) * field.winfo_reqheight())
    mainCanvas.config(scrollregion = (0,0,0,scrollableDepth))

#Subroutine callable to load the Stock Menu
def stockMenu():
    global stock
    createDefaultCanvas()
    formatTable(stock)

#Subroutine callable to load the Shift Menu
def employeeMenu():
    global employees
    createDefaultCanvas()
    formatTable(employees)

def logout():
    window.clear()
    loginMenu()

def changePassword():
    print("password_changed")

#Subroutine callable to load the Main Menu
def mainMenu():
    #Next, links to each system are placed
    navBar = Frame(window, background = "black")
    stockMenuButton = Button(navBar, image = images['stock-icon.png'], command = stockMenu)
    navBar.grid_anchor("center")
    stockMenuButton.grid(column = 0, row = 0, padx = 50)
    rotaMenuButton = Button(navBar, image = images["rota-icon.png"], command = employeeMenu)
    rotaMenuButton.grid(column = 1, row = 0, padx = 50)
    navBar.pack(fill = X, side = "top", anchor = "n")
    profileButton = Menubutton(window, image = images["profile-icon.png"])
    profileButton.menu = Menu(profileButton)
    profileButton["menu"] = profileButton.menu
    profileButton.menu.add_cascade(label = "Logout", command = logout)
    profileButton.menu.add_cascade(label = "Change Password", command = changePassword)
    profileButton.place(relx = 1, rely = 0, anchor = "ne")

#Subroutine callable to process login attempts
def loginAttempt(usernameEntered,passwordEntered):
    status = "user"
    usernameAccepted = False
    for employee in employees:
        if usernameEntered == employee.name:
            usernameAccepted = True
            break
    if usernameAccepted != True:
        error("Incorrect Username")
    else:
        if usernameEntered == employees[0].name:
            status = "admin"
        if (status == "user" and passwordEntered == "a") or (status == "admin" and passwordEntered == "a"):
            window.clear()
            mainMenu()
        else:
            error("Incorrect Password")
    #If username and password are correct, the Main Menu is opened

#Subroutine callable to open the Login Menu
def loginMenu():
    loginFrame = Frame(window, width = 500, height = 500)
    loginFrame.grid_propagate(False)
    loginFrame.grid_anchor("center")
    loginFrame.pack(anchor = "center", pady = window.winfo_reqheight())
    #Next labels and entry boxes are placed so that a username and password may be entered
    loginLabel = Label(loginFrame, text = "Please Login", font = bigFont)
    loginLabel.grid(column = 0, row = 0, pady = 10, columnspan = 2)
    usernameLabel = Label(loginFrame, text = "Username", font = titleFont)
    usernameLabel.grid(column = 0, row = 1, pady = 10)
    usernameEntry = Entry(loginFrame, font = mainFont)
    usernameEntry.grid(column = 1, row = 1, pady = 10)
    passwordLabel = Label(loginFrame, text = "Password", font = titleFont)
    passwordLabel.grid(column = 0, row = 2, pady = 10)
    passwordEntry = Entry(loginFrame, show = "*", font = mainFont)
    passwordEntry.grid(column = 1, row = 2, pady = 10)
    enterButton = Button(loginFrame, text = "Enter", font = mainFont, 
                         command = lambda:[loginAttempt(usernameEntry.get(),passwordEntry.get())])
    enterButton.grid(row = 3, columnspan = 2)

loadImages()
loadFiles()
loginMenu()
window.mainloop()