from tkinter import *
from os import listdir
from data import *
from gui import window
from table import *
from settings import *

user : EmployeeData

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

def loadMenu(type):
    global mainCanvas
    createDefaultCanvas()
    Table(type,mainCanvas)

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
    messagebox.showinfo("Password Reset")
    passwordResetWindow.destroy()
        
def changePasswordMenu():
    global user
    passwordResetWindow = Tk()
    passwordResetWindow.title("Reset Password")
    passwordResetWindow.geometry("400x200")
    passwordResetWindow.grid_anchor("center")
    passwordLabel = Label(passwordResetWindow, text = "Enter Your Current Password")
    passwordLabel.grid(column = 0, row = 0, pady = 5)
    passwordEntry = Entry(passwordResetWindow, show = "*")
    passwordEntry.grid(column = 0, row = 1, pady = 5)
    newPasswordLabel = Label(passwordResetWindow, text = "Enter Your New Password")
    newPasswordLabel.grid(column = 0, row = 2, pady = 5)
    newPasswordEntry = Entry(passwordResetWindow, show = "*")
    newPasswordEntry.grid(column = 0, row = 3, pady = 5)
    enterButton = Button(passwordResetWindow, text = "Enter", command = 
                         lambda:[changePassword(user.name, passwordEntry.get(),newPasswordEntry.get(),passwordResetWindow)])
    enterButton.grid(column = 0, row = 4, columnspan = 2)
    passwordResetWindow.bind("<Return>", lambda e : enterButton.invoke())

def addPermissions(menu):
    global user,employees
    permissions = [("Logout",logout),("Change Password",changePasswordMenu)]
    if window.authority == "admin":
        loadEmployees = lambda args = employees: loadMenu(args)
        permissions += [("View Employee Info", loadEmployees)]
    for permission in permissions:
        menu.add_command(label = permission[0], command = permission[1])

#Subroutine callable to load the Main Menu
def mainMenu():
    global stock, rota
    #Next, links to each system are placed
    navBar = Frame(window, background = headerBackground)
    loadStock = lambda args = stock: loadMenu(args)
    stockMenuButton = Button(navBar, image = images['stock-icon.png'], command = loadStock , border = 0)
    navBar.grid_anchor("center")
    stockMenuButton.grid(column = 0, row = 0, padx = 50)
    loadRota = lambda args = rota: loadMenu(args)
    rotaMenuButton = Button(navBar, image = images["rota-icon.png"], command = loadRota, border = 0, )
    rotaMenuButton.grid(column = 1, row = 0, padx = 50)
    navBar.pack(fill = X, side = "top", anchor = "n")
    profileButton = Menubutton(window, image = images["profile-icon.png"])
    profileButton.menu = Menu(profileButton,tearoff=False)
    profileButton["menu"] = profileButton.menu
    addPermissions(profileButton.menu)
    profileButton.place(relx = 1, rely = 0, anchor = "ne")

#Subroutine callable to process login attempts
def validateDetails(username,password):
    usernameAccepted = False
    passwordAccepted = False
    for employee in employees:
        if username == employee.name:
            usernameAccepted = True
            break
    if usernameAccepted == False:
        messagebox.showerror("Incorrect Username")
        return(False)
    for savedPassword in passwords:
        if savedPassword.employeeId == employee.employeeId and password == savedPassword.password:
            passwordAccepted = True
            return(accessMap[username])
    if passwordAccepted == False:
        messagebox.showerror("Incorrect Password")
        return(False)
    
def loginAttempt(username, password):
    access = validateDetails(username, password)
    if access != "none":
        window.authority = access
        window.clear()
        window.unbind_all("<Return>")
        mainMenu()

#Subroutine callable to open the Login Menu
def loginMenu():
    loginFrame = Frame(window, width = 500, height = 500, background= appColour)
    loginFrame.grid_propagate(False)
    loginFrame.grid_anchor("center")
    #Next labels and entry boxes are placed so that a username and password may be entered
    loginLabel = Label(loginFrame, text = "Login", font = titleFont)
    loginLabel.grid(column = 0, row = 0, pady = 10, columnspan = 2)
    usernameLabel = Label(loginFrame, text = "Username", font = titleFont)
    usernameLabel.grid(column = 0, row = 1, pady = 10)
    usernameEntry = Entry(loginFrame)
    usernameEntry.grid(column = 1, row = 1, pady = 10)
    passwordLabel = Label(loginFrame, text = "Password", font = titleFont)
    passwordLabel.grid(column = 0, row = 2, pady = 10)
    passwordEntry = Entry(loginFrame, show = "*")
    passwordEntry.grid(column = 1, row = 2, pady = 10)
    enterButton = Button(loginFrame, text = "Enter", font = titleFont, command = lambda:[loginAttempt(usernameEntry.get(),passwordEntry.get())])
    enterButton.grid(row = 3, columnspan = 2)
    loginFrame.pack(anchor = "center", pady = 200)
    window.bind("<Return>", lambda e : enterButton.invoke())

loadImages()
loadFiles()
loginMenu()
window.mainloop()