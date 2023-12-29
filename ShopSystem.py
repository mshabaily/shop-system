#This system is designed for Abdallah and Sons - a general goods store
#The Admin username is "NasserAbdallah", and the admin password is "AdminPass123"
#The default usernames for non admin users are "KamalAbdallah" and "SarahAbdallah" (more are created with the names in the shift Menu)
#, the password for non admins is "UserPass123"

#Tkinter libraries are imported
from tkinter import *
from tkinter import messagebox
from os import listdir
from dataClasses import *

stock = []
deliveries = []
employees = []
images = dict()

class GUI(Tk):
    def __del__(self):
        saveFiles()
    def __init__(self):
        super().__init__()

#Window is opended and set to fullscreen
window = GUI()
window.attributes('-fullscreen', True)
window.geometry("1920x1080")
window.title("Abdallah and Sons")
window.configure(bg = "white")

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

#Subroutine callable to save 2D arrays into text files
def saveFiles():
    global deliveries, employees, stock
    arrays = [deliveries, employees, stock]
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
            if file.name == "classes/deliveries.txt":
                deliveries.append(DeliveryData(fields))
            elif file.name == "classes/employees.txt":
                employees.append(EmployeeData(fields))
            elif file.name == "classes/stock.txt":
                stock.append(StockData(fields))
        file.close()

def loadImages():
    global images
    for imagePath in listdir("images"):
        images.update({imagePath : PhotoImage(file = "images/" + imagePath)})

#Subroutine callable to display errors
def error(errorMessage):
    messagebox.showerror(title = "Error", message = errorMessage)

#Function callable to return the profit of the store from the Profit text file
def getProfit():
    profit = open("dataFiles/profit.txt")
    return profit

#Subroutine callable to save the profit of the store into the Profit text file
def saveProfit(profit):
    array = open("dataFiles/profit.txt", "w")
    array.write(profit)

def infoEntryHandler(event,object,attribute):
    object.__setattr__(attribute,event.widget.get())

def formatTable(array):
    global mainCanvas
    attributes = list(vars(array[0]).keys())
    for counter, attribute in enumerate(attributes):
        attributeLabel = Label(mainCanvas, font = ("roboto",15), text=attribute, width = array[0].getCharLimit(counter))
        attributeLabel.grid(row = 0, column = counter)
    internalFrame = Frame(mainCanvas)
    mainCanvas.create_window((0,attributeLabel.winfo_reqheight()), window = internalFrame, anchor = "nw")
    for rowNum, object in enumerate(array,1):
        for columnNum, attribute in enumerate(attributes):
            field = Entry(internalFrame, width = object.getCharLimit(columnNum), font=("roboto",15))
            field.insert(0, getattr(object, attribute, "none"))
            field.bind("<KeyRelease>", lambda event, object = object, attribute = attribute: 
                       infoEntryHandler(event,object,attribute))
            field.grid(row = rowNum, column = columnNum)
    scrollableDepth = (len(array) * field.winfo_reqheight())
    mainCanvas.config(scrollregion = (0,0,0,scrollableDepth))
    mainCanvas.pack(pady = 200, anchor=CENTER, expand = True)

#Subroutine callable to load the Stock Menu
def stockMenu():
    global stock
    createDefaultCanvas()
    fields = formatTable(stock)

#Subroutine callable to load the Shift Menu
def employeeMenu():
    global employees
    createDefaultCanvas()
    formatTable(employees)

#Subroutine callable to load the Parcel Menu
def deliveryMenu():
    global deliveries
    createDefaultCanvas()
    formatTable(deliveries)

#Subroutine callable to load the Main Menu
def mainMenu():
    #Next, links to each system are placed
    navBar = Frame(window, background = "black")
    backButton = Button(navBar, image = images["back.gif"], command = window.destroy)
    backButton.grid(row = 0, column = 0, padx=(0,90))
    stockMenuButton = Button(navBar, image = images['stock.gif'], command = stockMenu)
    stockMenuButton.grid(row = 0, column = 1)
    shiftMenuButton = Button(navBar, image = images["shift.gif"], command = employeeMenu)
    shiftMenuButton.grid(row = 0, column = 2)
    parcelMenuButton = Button(navBar, image = images["parcel.gif"], command = deliveryMenu)
    parcelMenuButton.grid(row = 0, column = 3)
    navBar.pack(fill = X, anchor = "n")
    window.mainloop()

#Subroutine callable to process login attempts
def loginAttempt(usernameEntered,passwordEntered):
    #The Shift Database is loaded
    #Next, each name in the shift database is compared to the username entered
    status = "user"
    usernameAccepted = False
    for employee in employees:
        if usernameEntered == employee.name:
            usernameAccepted = True
            break
    if usernameAccepted != True:
        error("Incorrect Username")
    #Appropriate errors are displayed should usernames or passwords not match
    else:
        if usernameEntered == employees[0].name:
            status = "admin"
        if (status == "user" and passwordEntered == "a") or (status == "admin" and passwordEntered == "a"):
            mainMenu()
            return
        else:
            error("Incorrect Password")
    loginMenu()
    #If username and password are correct, the Main Menu is opened

#Subroutine callable to open the Login Menu
def loginMenu():
    loginFrame = Frame(width = 1920, height = 1080)
    loginFrame.pack()
    #Next labels and entry boxes are placed so that a username and password may be entered
    loginLabel = Label(loginFrame, text = "Please Login", font = ("Helvetica", 15), fg = "white", bg = "black")
    loginLabel.place(x = 625, y = 100)
    usernameTextBox = Entry(loginFrame, font = ("Helvetica",15), fg = "white", bg = "black")
    usernameTextBox.place(x = 665, y = 350, height = 30, width = 200)
    usernameLabel = Label(loginFrame, text = "Username", font = ("Helvetica",15), fg = "white", bg = "black")
    usernameLabel.place(x = 515, y = 350)
    passwordTextBox = Entry(loginFrame, show = "*", font = ("Helvetica",15), fg = "white", bg = "black")
    passwordTextBox.place(x = 665, y = 400, height = 30, width = 200)
    passwordLabel = Label(loginFrame, text = "Password", font = ("Helvetica",15), fg = "white", bg = "black")
    passwordLabel.place(x = 515, y = 400)
    enterButton = Button(loginFrame, text = "Enter", font = ("Helvetica",15), fg = "white", bg = "black", 
                         command = lambda:[loginAttempt(usernameTextBox.get(),passwordTextBox.get()),loginFrame.destroy()])
    enterButton.place(x = 650, y = 500)

loadImages()
loadFiles()
mainMenu()