from time import sleep
from tkinter import CENTER, E, END, X, Button, Canvas, Entry, Frame, Label, Menu, Menubutton, OptionMenu, PhotoImage, Scrollbar, StringVar, Tk, messagebox
from os import listdir
from dataClasses import *

user : EmployeeData

profit = 0
stock = []
employees = []
passwords = []
rota = []
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
    global employees, stock, passwords
    arrays = [employees, stock, passwords]
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
    global passwords, employees, stock
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
            elif file.name =="classes/passwords.txt":
                passwords.append(PasswordData(fields))
            elif file.name == "classes/rota.txt":
                rota.append(RotaData(fields))
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

def inform(infoMessage):
    messagebox.showinfo(title = "Info", message = infoMessage)

def infoEntryHandler(event,object,attribute,field):
    global user
    if event.keysym == "Return" or event.keysym == "Escape":
        return
    if user.status != "staff":
        object.__setattr__(attribute,event.widget.get())
    else:
        error("You do not have permission to change this")
        field.delete(0,END)
        field.insert(0,getattr(object,attribute))

def formatTable(objects):
    global mainCanvas
    attributes = list(vars(objects[0]).keys())
    fieldsContainer = Frame(mainCanvas)
    headersContainer = Frame(mainCanvas)
    mainCanvas.create_window((0,0), width = mainCanvas.winfo_reqwidth(), window = headersContainer, anchor = "nw")
    mainCanvas.create_window((0,Label().winfo_reqheight()), width = mainCanvas.winfo_reqwidth(), window = fieldsContainer, anchor = "nw")
    for column, attribute in enumerate(attributes):
        header = Label(headersContainer, text = attribute)
        header.grid(row = 0, column = column)
        headersContainer.grid_columnconfigure(index=column, weight = 1)
        fieldsContainer.grid_columnconfigure(index=column, weight = 1)
        for row, object in enumerate(objects):
            field = Entry(fieldsContainer)
            field.insert(0,getattr(object, attribute))
            field.bind("<KeyRelease>", 
                 lambda event,object = object, attribute = attribute, field = field:
                 infoEntryHandler(event,object,attribute,field))
            field.grid(row = row, column = column)
    scrollableDepth = ((len(objects)+1) * field.winfo_reqheight())
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

def rotaMenu():
    global rota
    createDefaultCanvas()
    formatTable(rota)

def logout():
    window.clear()
    loginMenu()

def changePassword(username,password,newPassword,passwordResetWindow):
    if not validateDetails(username, password):
        return
    for savedPassword in passwords:
        if savedPassword.employeeId == user.employeeId:
            savedPassword.password = newPassword
            break
    inform("Password Reset")
    passwordResetWindow.destroy()
        
def changePasswordMenu():
    global user
    passwordResetWindow = Tk()
    passwordResetWindow.title("Reset Password")
    passwordResetWindow.geometry("400x200")
    passwordResetWindow.grid_anchor("center")
    passwordLabel = Label(passwordResetWindow, font = titleFont, text = "Enter Your Current Password")
    passwordLabel.grid(column = 0, row = 0, pady = 5)
    passwordEntry = Entry(passwordResetWindow, show = "*")
    passwordEntry.grid(column = 0, row = 1, pady = 5)
    newPasswordLabel = Label(passwordResetWindow, font = titleFont, text = "Enter Your New Password")
    newPasswordLabel.grid(column = 0, row = 2, pady = 5)
    newPasswordEntry = Entry(passwordResetWindow, show = "*")
    newPasswordEntry.grid(column = 0, row = 3, pady = 5)
    enterButton = Button(passwordResetWindow, text = "Enter", command = 
                         lambda:[changePassword(user.name, passwordEntry.get(),newPasswordEntry.get(),passwordResetWindow)])
    enterButton.grid(column = 0, row = 4, columnspan = 2)
    passwordResetWindow.bind("<Return>", lambda e : enterButton.invoke())

def addPermissions(menu):
    global user
    permissions = [("Logout",logout),("Change Password",changePasswordMenu)]
    if user.status == "admin":
        permissions += [("View Employee Info",employeeMenu)]
    for permission in permissions:
        menu.add_cascade(label = permission[0], command = permission[1])

#Subroutine callable to load the Main Menu
def mainMenu():
    global user
    #Next, links to each system are placed
    navBar = Frame(window, background = "black")
    stockMenuButton = Button(navBar, image = images['stock-icon.png'], command = stockMenu)
    navBar.grid_anchor("center")
    stockMenuButton.grid(column = 0, row = 0, padx = 50)
    rotaMenuButton = Button(navBar, image = images["rota-icon.png"], command = rotaMenu)
    rotaMenuButton.grid(column = 1, row = 0, padx = 50)
    navBar.pack(fill = X, side = "top", anchor = "n")
    profileButton = Menubutton(window, image = images["profile-icon.png"])
    profileButton.menu = Menu(profileButton)
    profileButton["menu"] = profileButton.menu
    addPermissions(profileButton.menu)
    profileButton.place(relx = 1, rely = 0, anchor = "ne")

#Subroutine callable to process login attempts
def validateDetails(username,password):
    global user
    usernameAccepted = False
    passwordAccepted = False
    for employee in employees:
        if username == employee.name:
            usernameAccepted = True
            user = employee
            break
    if usernameAccepted == False:
        error("Incorrect Username")
        return(False)
    for savedPassword in passwords:
        if savedPassword.employeeId == employee.employeeId and password == savedPassword.password:
            passwordAccepted = True
            return(True)
    if passwordAccepted == False:
        error("Incorrect Password")
        return(False)
    
def loginAttempt(username, password):
    if validateDetails(username, password):
        window.clear()
        window.unbind_all("<Return>")
        mainMenu()

#Subroutine callable to open the Login Menu
def loginMenu():
    loginFrame = Frame(window, width = 500, height = 500)
    loginFrame.grid_propagate(False)
    loginFrame.grid_anchor("center")
    #Next labels and entry boxes are placed so that a username and password may be entered
    loginLabel = Label(loginFrame, text = "Login", font = bigFont)
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
    loginFrame.pack(anchor = "center", pady = 200)
    window.bind("<Return>", lambda e : enterButton.invoke())

loadImages()
loadFiles()
loginMenu()
window.mainloop()