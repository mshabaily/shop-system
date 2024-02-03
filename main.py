from functools import partial
from tkinter import *
from os import listdir
from data import *
from gui import User, window
from table import *
from settings import *

user : EmployeeData
detailsMapping : {str : str}

profit = 0
images = dict()

#Window is opended and set to fullscreen
window.configure(bg = windowBackground)
mainCanvas = Canvas(bg = canvasBackground)

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
        images.update({imagePath : image})

def loadMenu(type, accessLevel):
    global mainCanvas
    createDefaultCanvas()
    Table(type,mainCanvas, accessLevel).load()

def logout():
    window.clear()
    bootMenu()

def changePassword(newPassword):
    for savedPassword in passwords:
        if savedPassword.employeeId == user.employeeId:
            savedPassword.password = newPassword
            break
    messagebox.showinfo("Password Reset")

def loadUserDetails():
    mainMenu()
    loadMenu([window.user], accessLevel = "open")

def verifyPasswordChange():
    window.clear()
    mainMenu()
    loginBox(target = lambda : loadUserDetails(), master = mainCanvas)

def addPermissions(menu):
    permissions = [("Logout",logout),("Change Password",verifyPasswordChange)]
    if window.user.status == "admin":
        loadEmployees = lambda args = employees: loadMenu(args, accessLevel = "closed")
        permissions += [("View Employee Info", loadEmployees)]
    for permission in permissions:
        menu.add_command(label = permission[0], command = permission[1])

#Subroutine callable to load the Main Menu
def mainMenu():
    #Next, links to each system are placed
    navBar = Frame(window, background = headerBackground)
    loadStock = lambda args = stock: loadMenu(args, accessLevel = "closed")
    stockMenuButton = Button(navBar, image = images['stock-icon.png'], command = loadStock , border = 0)
    navBar.grid_anchor("center")
    stockMenuButton.grid(column = 0, row = 0, padx = 50)
    loadRota = lambda args = rota: loadMenu(args, accessLevel = "closed")
    rotaMenuButton = Button(navBar, image = images["rota-icon.png"], command = loadRota, border = 0)
    rotaMenuButton.grid(column = 1, row = 0, padx = 50)
    navBar.pack(fill = X, side = "top", anchor = "n")
    profileButton = Menubutton(window, image = images["profile-icon.png"])
    profileButton.menu = Menu(profileButton,tearoff=False)
    profileButton["menu"] = profileButton.menu
    addPermissions(profileButton.menu)
    profileButton.place(relx = 1, rely = 0, anchor = "ne")

#Subroutine callable to process login attempts
def validateDetails(username,password):

    #Checks if a user is already logged in, in which case verifies their password
    #Otherwise all usernames are checked for matching passwords based on ID
    checkedEmployees = employees
    if window.user != None:
        checkedEmployees = [window.user]
    
    usernameAccepted = False
    for employee in checkedEmployees:
        if username == employee.name:
            usernameAccepted = True
            break
    if usernameAccepted == False:
        messagebox.showerror("error","Incorrect Username")
        return("none")
    try:
        if password == detailsMapping[username]:
            return(employee)
        else:
            raise KeyError
    except KeyError:
        messagebox.showerror("error","Incorrect Password")
        return("none")
    
def mapDetails():
    global detailsMapping
    detailsMapping = {}
    for employee in employees:
        for password in passwords:
            if password.employeeId == employee.employeeId:
                detailsMapping.update({employee.name : password.password})
                break
    print(detailsMapping["JohnSmith"])
    
def loginAttempt(username, password, target):
    profile = validateDetails(username, password)
    if profile == "none":
        return
    username = profile.name
    window.user = User(username, detailsMapping[username], profile.status)
    window.clear()
    window.unbind_all("<Return>")
    target()

def bootMenu():
    window.user = None
    loginBox(target = lambda: mainMenu(), master = window)

#Subroutine callable to open the Login Menu
def loginBox(target, master):
    loginFrame = Frame(window, height = window.winfo_screenheight() , width = window.winfo_screenwidth(), background= appColour)
    loginFrame.grid_propagate(False)
    loginFrame.grid_anchor("center")
    #Next labels and entry boxes are placed so that a username and password may be entered
    loginLabel = Label(loginFrame, text = "Enter Details", font = titleFont)
    loginLabel.grid(column = 0, row = 0, pady = 10, columnspan = 2)
    usernameLabel = Label(loginFrame, text = "Username", font = titleFont)
    usernameLabel.grid(column = 0, row = 1, pady = 10)
    usernameEntry = Entry(loginFrame)
    usernameEntry.grid(column = 1, row = 1, pady = 10)
    passwordLabel = Label(loginFrame, text = "Password", font = titleFont)
    passwordLabel.grid(column = 0, row = 2, pady = 10)
    passwordEntry = Entry(loginFrame, show = "*")
    passwordEntry.grid(column = 1, row = 2, pady = 10)
    loginCommand = lambda target = target: loginAttempt(usernameEntry.get(),passwordEntry.get(), target)
    enterButton = Button(loginFrame, text = "Enter", font = titleFont, command = loginCommand)
    enterButton.grid(row = 3, columnspan = 2)
    loginFrame.pack(anchor = "center", pady = 200)
    window.bind("<Return>", lambda e : enterButton.invoke())

loadImages()
loadFiles()
mapDetails()
bootMenu()
window.mainloop()