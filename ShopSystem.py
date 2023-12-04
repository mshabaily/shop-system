#This system is designed for Abdallah and Sons - a general goods store
#The Admin username is "NasserAbdallah", and the admin password is "AdminPass123"
#The default usernames for non admin users are "KamalAbdallah" and "SarahAbdallah" (more are created with the names in the shift Menu), the password for non admins is "UserPass123"

#Tkinter libraries are imported
from tkinter import *
from tkinter import messagebox
from functools import partial
from os import listdir

#Window is opended and set to fullscreen
window = Tk()
window.attributes('-fullscreen', True)
window.geometry("1920x1080")
window.title("Abdallah and Sons")
window.configure(bg = "black")

global status

#Function callable to return 2D arrays, populated based on text files
def loadArray(arrayName):
    arrayPath = "dataFiles/" + arrayName + ".txt"
    with open(arrayPath) as array:
        lines = [line.split(",") for line in array]
    array.close()
    return lines

#Subroutine callable to save 2D arrays into text files
def saveArray(arrayName):
    arrayPath = "dataFiles/" + arrayName + ".txt"
    array = open(arrayPath, "w")
    lines = loadArray(arrayName)
    for loop in len(lines):
        for loop2 in range(len(lines[0])):
            array.write(lines[loop][loop2])
            array.write(",")
        loop2 = 0
        array.write("\n")
    array.close()

def loadImages():
    global images
    images = dict()
    for loop in range (len(listdir("images"))):
        images.update({listdir("images")[loop] : PhotoImage(listdir("images")[loop])})

#Subroutine callable to send user to previous screen (should the user be in the "login" screen the window will close)
def back(currentPage):
    print(currentPage)
    if currentPage == "login":
        window.destroy()
    if currentPage == "main":
        loginMenu()
    if currentPage == "sub":
        mainMenu()
    if currentPage == "loyalty":
        parcelMenu()

#Subroutine callable to display errors
def error(errorMessage):
    messagebox.showerror(title = "Error", message = errorMessage)

#Subroutine callable to open the database editing window
def getEditValue(editType,database,frame,mainMenuFrame,status,usernameEntered,lengthDatabase,scrollbar,movementRemaining):
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    #Firstly it determines if the user is able to edit the value selected in table (launching an error if they are not)
    errorEvent = False
    if editType == "shifts" and x > 384 and x < 483:
        error("Cannot edit ID")
        errorEvent = True
    if editType == "parcel" and x > 480 and x < 580:
        error("Cannot edit ID")
        errorEvent = True
    if editType == "loyalty" and x > 440 and x < 540:
        error("Cannot edit ID")
        errorEvent = True
    if editType == "previousParcels" and x > 480 and x < 580:
        error("Cannot edit ID")
        errorEvent = True
    if (editType == "shifts" or editType == "previousParcels") and status == "user":
        error("Admin only")
        errorEvent = True
    if errorEvent == False:
        #Should they be permitted, a new window will open where the value can be entered
        window2 = Tk()
        window2.geometry("400x50")
        window2.title("Edit Value")
        window2.configure(bg = "white")
        stockCanvas = Canvas(window2, bg="white", height=50, width=400)
        stockCanvas.pack()
        #Certain selected table values trigger unique windows
        if editType == "stock" and x > 432 and x < 532:
            entryValue = Entry(window2, width = 3)
            stockCanvas.create_window(25, 27, window=entryValue)
            entryValue2 = Entry(window2, width = 3)
            stockCanvas.create_window(65, 27, window=entryValue2)
            packX = Label(window2, text = "x")
            stockCanvas.create_window(45, 27, window=packX)
            entryValue3 = None
            entryValue4 = None
        elif editType == "stock" and x > 532 and x < 732:
            currencyPound = Label(window2, text = "£")
            stockCanvas.create_window(25, 27, window=currencyPound)
            entryValue = Entry(window2, width = 3)
            stockCanvas.create_window(45, 27, window=entryValue)
            entryValue2 = Entry(window2, width = 3)
            stockCanvas.create_window(85, 27, window=entryValue2)
            currencyPoint = Label(window2, text = ".")
            stockCanvas.create_window(65, 27, window=currencyPoint)
            entryValue3 = None
            entryValue4 = None
        elif editType == "shifts" and x > 816 and x < 915:
            entryValue = Entry(window2, width = 2)
            stockCanvas.create_window(45, 27, window=entryValue)
            timeColon1 = Label(window2, text = ":")
            stockCanvas.create_window(55, 27, window=timeColon1)
            entryValue2 = Entry(window2, width = 2)
            stockCanvas.create_window(65, 27, window=entryValue2)
            timeDash = Label(window2, text = "-")
            stockCanvas.create_window(85, 27, window=timeDash)
            entryValue3 = Entry(window2, width = 2)
            stockCanvas.create_window(105, 27, window=entryValue3)
            timeColon2 = Label(window2, text = ":")
            stockCanvas.create_window(115, 27, window=timeColon2)
            entryValue4 = Entry(window2, width = 2)
            stockCanvas.create_window(125, 27, window=entryValue4)
        elif (editType == "parcel" or editType == "previousParcels") and (x > 680 and x < 780):
            entryValue = Entry(window2, width = 2)
            stockCanvas.create_window(45, 27, window=entryValue)
            timeColon1 = Label(window2, text = ":")
            stockCanvas.create_window(55, 27, window=timeColon1)
            entryValue2 = Entry(window2, width = 2)
            stockCanvas.create_window(65, 27, window=entryValue2)
            entryValue3 = None
            entryValue4 = None
        elif (editType == "parcel" or editType == "previousParcels") and (x > 780 and x < 880):
            entryValue = Entry(window2, width = 2)
            stockCanvas.create_window(45, 27, window=entryValue)
            dateSlash = Label(window2, text = "/")
            stockCanvas.create_window(55, 27, window=dateSlash)
            entryValue2 = Entry(window2, width = 2)
            stockCanvas.create_window(75, 27, window=entryValue2)
            dateSlash = Label(window2, text = "/")
            stockCanvas.create_window(85, 27, window=dateSlash)
            entryValue3 = Entry(window2, width = 4)
            stockCanvas.create_window(105, 27, window=entryValue3)
            entryValue4 = None
        elif editType == "loyalty" and x > 540 and x < 819:
            entryValue = Entry(window2, width = 20)
            stockCanvas.create_window(70, 27, window=entryValue)
            emailAt = Label(window2, text = "@")
            stockCanvas.create_window(140, 27, window=emailAt)
            entryValue2 = Entry(window2, width = 20)
            stockCanvas.create_window(210, 27, window=entryValue2)
            emailDot = Label(window2, text = ".")
            stockCanvas.create_window(270, 27, window=emailDot)
            entryValue3 = Entry(window2, width = 4)
            stockCanvas.create_window(300, 27, window=entryValue3)
            entryValue4 = None
        else:
            entryValue2 = None
            entryValue3 = None
            entryValue4 = None
            entryValue = Entry(window2, width = 45)
            stockCanvas.create_window(150, 27, window=entryValue)
        saveEditValueCommand = partial(saveEditValue,entryValue,entryValue2,entryValue3,entryValue4,x,y,editType,window2,database,frame,mainMenuFrame,status,usernameEntered,lengthDatabase,scrollbar,movementRemaining)
        editButton = Button(window2, text = "Confirm", font = ("Helvetica", 10), command = saveEditValueCommand)
        stockCanvas.create_window(350, 25, window=editButton)

def goToScreen(destination):
    if destination == "login":
        loginMenu()
    if destination == "main":
        mainMenu()
    if destination == "stock":
        stockMenu()
    if destination == "shifts":
        shiftMenu()
    if destination == "loyalty":
        loyaltyMenu()
    if destination == "parcel":
        parcelMenu()
    if destination == "previousParcels":
        previousParcelsMenu()

#Subroutine callable to remove the final row from a database
def popDatabase(currentScreen,status,database,frame):
    #First it determines if the user is able to remove the row from a database (launching an error if they are not)
    if currentScreen == "shifts" and status == "user":
        error("Admin only")
        return
    if currentScreen == "shifts" and len(database) == 1:
        error("Cannot remove admin")
        return
    frame.destroy()
    try:
        #The row is removed
        database.pop()
        #The database will then be saved
        saveArray(currentScreen)
    except:
        error("Array empty")
    goToScreen(currentScreen)

#Subroutine callable add a new row to a database
def appendDatabase(currentScreen,status,database,frame):
    #First it determines if the user is able to add a row to the database (launching an error if they are not)
    if currentScreen == "shifts" and status == "user":
        error("Admin only")
        return
    #Should the user be able then the row will be added
    newLine = (["   "] * len(database[0]))
    frame.destroy()
    #Some items in new rows will be populated with "   ", while certain others will be given more appropriate values
    if currentScreen == "stock":
        newLine[8] = "0"
        newLine[9] = "0"
    elif currentScreen == "shifts":
        if status != "admin":
            error("Admin only")
            return
        newLine[0] = "test"
        newLine[4] = "test"
    elif currentScreen == "loyalty":
        newLine[0] = "test"
        newLine[4] = "test"
    database.append(newLine)
    #The database will then be saved, and the length of the database will be updated
    saveArray(currentScreen)
    goToScreen(currentScreen)

#Function callable to determine and return the row selected by the user, ignoring appended rows (which are adjusted for elsewhere)
#Rows are dermined by comparing the cursor's y co-ordinate to the y co-ordinates of rows, each row checked using a recursive loop
def getRow(editRow,y,topBoundary,bottomBoundary):
    if y < topBoundary or y > bottomBoundary:
        topBoundary = topBoundary + 30
        bottomBoundary = bottomBoundary + 30
        editRow = editRow + 1
        editRow = getRow(editRow,y,topBoundary,bottomBoundary)
    return editRow

#Subroutine callable to update the Previous Parcels and Loyalty Scheme databases accordingly when parcels are removed from the Parcel database (done so on their collection)
def moveParcel(row,window2,clearList,clearListAdd,database,frame1,status,usernameEntered,lengthDatabase,movementRemaining,frame3,frame2):
    frame3.destroy()
    #Firstly it determines if the customer ID is entered (if not it will launch an error)
    if str(database[row][1]) != "   ":
        #Then it loads the Previous Parcels and Loyalty Scheme databases
        previousParcelsDatabase = loadArray("previousParcels")
        loyaltyDatabase = loadArray("loyalty")
        #Next it determines if the customer ID is valid (if not it will launch an error)
        if int(database[row][1]) <= int(lengthDatabase[2]):
            #Next it checks if the Previous Parcels database is long enough to recieve a new item (if not it will add a row)
            if previousParcelsDatabase[(int(lengthDatabase[4])-1)][0] != "   ":
                appendDatabase("previousParcels",frame1,status,usernameEntered,lengthDatabase,previousParcelsDatabase,frame3,4,4,movementRemaining,frame2)
            count = 0
            #Then it finds the next empty row of the Previous Parcels database and fills it with the removed row from the Parcel database
            loop = True
            while loop == True:
                if previousParcelsDatabase[count][0] != "   ":
                    count = count + 1
                else:
                    loop = False
            previousParcelsDatabase[count] = database[row]
            #It then updates the Loyalty Scheme database, updating the "total parcels" and "membership" of the customer with matching Customer ID
            loyaltyDatabase[(int(database[row][1])-1)][4] = str(int(loyaltyDatabase[(int(database[row][1])-1)][4]) + 1)
            if int(loyaltyDatabase[(int(database[row][1])-1)][4]) > 10:
                loyaltyDatabase[(int(database[row][1])-1)][3] = "Gold"
            elif int(loyaltyDatabase[(int(database[row][1])-1)][4]) > 5:
                loyaltyDatabase[(int(database[row][1])-1)][3] = "Silver"
            elif int(loyaltyDatabase[(int(database[row][1])-1)][4]) > 0:
                loyaltyDatabase[(int(database[row][1])-1)][3] = "Bronze"
            #Next, it saves the Loyalty Scheme and Previous Parcels databases
            saveArray("previousParcels", previousParcelsDatabase, lengthDatabase)
            saveArray("loyalty", loyaltyDatabase, lengthDatabase)
            #Then it loads and updates the profit
            profit = float(getProfit())
            profit = profit + 5.00
            saveProfit(profit)
            #Finally it clears the row of the parcel removed from the Parcel database and adjusts the parcel IDs accodingly
            clearList[0] = clearListAdd
            database[row] = clearList
            for loop in range((int(database[row][0])-1),int(lengthDatabase[2])):
                database[loop][0] = str(int(database[loop][0]) + 1)
                newID = ("0" * (3-(len(str(database[loop][0]))))) + str(database[loop][0])
                database[loop][0] = newID
            saveArray("parcel",database,lengthDatabase)
        else:
            error("Customer ID does not exist")
    else:
        error("Must enter customter customer ID")
    window2.destroy()
    parcelMenu(frame1,status,usernameEntered,lengthDatabase,movementRemaining,False)

#Subroutine callable to clear rows in the parcel menu (should the user not wish to update the Loyalty Scheme or Previous Parcels databases)
def destroyParcelWindow(window,clearList,clearListAdd,row,database,frame1,status,usernameEntered,lengthDatabase,movementRemaining,frame3):
    frame3.destroy()
    clearList[0] = clearListAdd
    database[row] = clearList
    saveArray("parcel",database,lengthDatabase)
    parcelMenu(frame1,status,usernameEntered,lengthDatabase,movementRemaining,False)
    window.destroy()

#Subroutine callable to clear rows in databases
def clearRow(editType,database,frame1,status,usernameEntered,frame2,frame3,lengthDatabase,scrollbar,x,movementRemaining):
    #Firstly the row is determined by getRow() and adjusted based on the position of the scrollbar
    y = window.winfo_pointery()
    row = getRow(0,y,152,181)
    if scrollbar.get()[0] != 0.0:
        percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
        row = int(row + ((int(lengthDatabase[x])-16)*(percentage/100)))
    clearList = []
    for loop in range(len(database[row])):
        clearList.append("   ")
    if editType == "stock":
        frame3.destroy()
        #Some items are populated with "   ", while others are filled with more appropriate values
        clearList[9] = "0"
        clearList[8] = "0"
        database[row] = clearList
        #After the row is updated the database is saved
        saveArray(editType,database,lengthDatabase)
        stockMenu(frame1,status,usernameEntered,lengthDatabase,movementRemaining,False,None)
    if editType == "shifts":
        if row == 0:
            error("Cannot remove admin")
        if status == "admin" and row != 0:
            frame3.destroy()
            clearListAdd2 = "0 Hours"
            clearListAdd = ("0" * (3-(len(str(row+1))))) + str(row+1)
            clearList[0] = clearListAdd
            clearList[4] = clearListAdd2
            database[row] = clearList
            saveArray(editType,database,lengthDatabase)
            shiftMenu(frame1,status,usernameEntered,lengthDatabase,movementRemaining,False)
        elif status == "user":
            error("Admin only")
    if editType == "parcel":
        ID = 0
        clearListAdd = str(database[row][0])
        window2 = Tk()
        window2.geometry("350x50")
        window2.title("Update Previous Parcels and Loyalty?")
        window2.configure(bg = "white")
        canvas = Canvas(window2, bg="white", height=50, width=400)
        canvas.pack()
        destroyParcelWindowCommand = partial(destroyParcelWindow,window2,clearList,clearListAdd,row,database,frame1,status,usernameEntered,lengthDatabase,movementRemaining,frame3)
        noButton = Button(window2, text = "No", font = ("Helvetica", 10), command = destroyParcelWindowCommand)
        canvas.create_window(50, 30, window=noButton)
        moveParcelCommand = partial(moveParcel,row,window2,clearList,clearListAdd,database,frame1,status,usernameEntered,lengthDatabase,movementRemaining,frame3,frame2)
        yesButton = Button(window2, text = "Yes", font = ("Helvetica", 10), command = moveParcelCommand)
        canvas.create_window(100, 30, window=yesButton)
    if editType == "loyalty":
        frame3.destroy()
        clearListAdd = ("0" * (3-(len(str(row+1))))) + str(row+1)
        clearListAdd2 = "0"
        clearList[0] = clearListAdd
        clearList[4] = clearListAdd2
        database[row] = clearList
        saveArray(editType,database,lengthDatabase)
        loyaltyMenu(frame1,status,usernameEntered,frame2,lengthDatabase,movementRemaining,False)
    if editType == "previousParcels":
        frame3.destroy()
        appendDatabase("previousParcels",frame1,status,usernameEntered,lengthDatabase,database,frame3,4,4,movementRemaining,frame2)
        database.remove(database[row])
        saveArray(editType,database,lengthDatabase)
        previousParcelsMenu(frame1,status,usernameEntered,frame2,lengthDatabase,movementRemaining,False)

#Subroutine callable to place buttons used in the clearing of rows onto screens
def printClears(startingXPos, frame):
    for loop in range(16):
        xButton = Button(frame,text = "X", font = ("Helvetica"), fg = "black",  width = 1, height = 1, command = clearRow)
        xButton.place(x = startingXPos, y = (152+(30*loop)))

#Function callable to return the profit of the store from the Profit text file
def getProfit():
    lengths = open("dataFiles/profit.txt")
    lines = lengths.readlines()
    return lines[0]

#Subroutine callable to save the profit of the store into the Profit text file
def saveProfit(profit):
    profit = str(round(profit,2))
    profitList = profit.split(".")
    if len(profitList[1]) == 1:
        profitList[1] = profitList[1] + "0"
    profit = profitList[0] + "." + profitList[1]
    array = open("Profit.txt", "w")
    array.write(profit)

#Subroutine callable to set the profit of the store to zero and save it
def clearProfit(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,subMenuFrame):
    saveProfit(0.0)
    subMenuFrame.destroy()
    stockMenu(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,False,None)

#Subroutine callable to record a new sale in the stock system
def sellRow(editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit,entry,y,window2):
    #Firstly it determines if the sale amount entered and unit price are valid (launching an error if one is not)
    if entry.get() == '':
        error("Enter amount to sell")
    else:
        amount = int(entry.get())
        if amount < 100:
            #Next, the row is determined by getRow() and adjusted based on the position of the scrollbar
            row = getRow(0,y,152,182)
            if scrollbar.get()[0] != 0.0:
                percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
                row = int(row + ((int(lengthDatabase[x])-16)*(percentage/100)))
            if database[row][9] != "0":
                #If the values are valid then the amount of items will decrease by the sale amount entered
                database[row][9] = str(int(database[row][9]) - amount)
                price = database[row][3]
                price = price.replace("£","")
                try:
                    #The profit is then increased by the unit price
                    profit = profit + (float(price)*amount)
                    #The stock database and profit are then saved
                    saveArray(editType,database,lengthDatabase)
                    saveProfit(profit)
                except:
                    error("Must enter unit price")
            else:
                error("No items to sell")
        else:
            error("Must be under 3 digits")
    window2.destroy()
    frame3.destroy()
    if editType == "stock":
        stockMenu(frame1,status,usernameEntered,lengthDatabase,movementRemaining,False,None)

#Subroutine callable to open a window where the amount of items being sold is entered
def getSellAmount(editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit):
    y = window.winfo_pointery()
    window2 = Tk()
    window2.geometry("400x50")
    window2.title("Enter Amount to Sell")
    window2.configure(bg = "white")
    stockCanvas = Canvas(window2, bg="white", height=50, width=400)
    stockCanvas.pack()
    entry = Entry(window2, width = 3)
    stockCanvas.create_window(160, 27, width = 300, window=entry)
    sellRowCommand = partial(sellRow,editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit,entry,y,window2)
    button = Button(window2, text = "Enter", command = sellRowCommand)
    stockCanvas.create_window(360, 27, window=button)

#Subroutine callable to place buttons used to sell items into the stock database
def printSells(xPlace,editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit):
    getSellAmountCommand = partial(getSellAmount,editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit)
    for loop in range(16):
        sellButton = Button(frame3,text = "Sell", font = ("Helvetica"), fg = "black",  width = 3, height = 1, command = getSellAmountCommand)
        sellButton.place(x = xPlace, y = (152+(30*loop)))

#Subroutine callable to record a new purchase in the stock system
def buyRow(editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit,entry,y,window2):
    #Firstly it determines if the sale amount entered and unit price are valid (launching an error if one is not)
    if entry.get() == '':
        error("Enter amount to buy")
    else:
        amount = int(entry.get())
        if amount < 100:
            #Next, the row is determined by getRow() and adjusted based on the position of the scrollbar
            row = getRow(0,y,152,182)
            if scrollbar.get()[0] != 0.0:
                percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
                row = int(row + ((int(lengthDatabase[x])-16)*(percentage/100)))
            #If the values are valid then the amount of items will increase by the purchase amount entered
            database[row][9] = str(int(database[row][9]) + amount)
            price = database[row][4]
            price = price.replace("£","")
            try:
                #The profit is then decreased by the line value
                profit = profit - (float(price)*amount)
                #The stock database and profit are then saved
                saveArray(editType,database,lengthDatabase)
                saveProfit(profit)
            except:
                error("Must enter line value")
        else:
            error("Must be under 3 digits")
    window2.destroy()
    frame3.destroy()
    if editType == "stock":
        stockMenu(frame1,status,usernameEntered,lengthDatabase,movementRemaining,False,None)

#Subroutine callable to open a window where the amount of items being bought is entered
def getBuyAmount(editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit):
    y = window.winfo_pointery()
    window2 = Tk()
    window2.geometry("400x50")
    window2.title("Enter Amount to Buy")
    window2.configure(bg = "white")
    stockCanvas = Canvas(window2, bg="white", height=50, width=400)
    stockCanvas.pack()
    entry = Entry(window2)
    stockCanvas.create_window(160, 27, width = 300, window=entry)
    buyRowCommand = partial(buyRow,editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit,entry,y,window2)
    button = Button(window2, text = "Enter", command = buyRowCommand)
    stockCanvas.create_window(360, 27, window=button)

#Subroutine callable to place buttons used to buy items into the stock database
def printBuys(xPlace,editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit):
    getBuyAmountCommand = partial(getBuyAmount,editType,database,frame1,status,usernameEntered,frame3,lengthDatabase,scrollbar,x,movementRemaining,profit)
    for loop in range(16):
        buyButton = Button(frame3,text = "Buy", font = ("Helvetica"), fg = "black",  width = 3, height = 1, command = getBuyAmountCommand)
        buyButton.place(x = xPlace, y = (152+(30*loop)))

#Subroutine callable to edit items selected in the Stock Database
def stockEditor(editValue,editValue2,x,y,editType,stockDatabase,subMenuFrame,mainMenuFrame,status,usernameEntered,lengthDatabase,scrollbar,movementRemaining):
    topBoundary = 154
    bottomBoundary = 184
    #Firstly, the row is determined by getRow() and adjusted based on the position of the scrollbar
    editRow = getRow(0,y,topBoundary,bottomBoundary)
    if scrollbar.get()[0] != 0.0:
        percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
        editRow = int(editRow + ((int(lengthDatabase[0])-16)*(percentage/100)))
    editValue = str(editValue)
    #The column is then determined by the x co-ordinate of the cursor
    if x > 80 and x < 206:
        #Next the value entered is validated specifically to each column (Lauching an error is the value doesn't fit the correct format)
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 13:
                #Should it pass validation, the database is then updated and saved
                stockDatabase[editRow][0] = editValue
            else:
                error("Invalid Length (Must be 13 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    elif x > 206 and x < 432:
        if editValue == "":
            error("Please enter a value")
        elif len(editValue) < 26:
            stockDatabase[editRow][1] = editValue
        else:
            error("Invalid Length (Cannot be over 25 letters)")
    elif x > 432 and x < 532:
        if editValue == "" or editValue2 == "":
            error("Please enter a value")
        elif len(editValue) <3 and len(editValue2) <3:
            editValue = editValue + "x" + editValue2
            stockDatabase[editRow][2] = editValue
        else:
            error("Invalid Length (Cannot be over 5 characters)")
    elif x > 532 and x < 632:
        if editValue == "" or editValue2 == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True and editValue2.isnumeric() == True:
            if len(editValue + editValue2) <6 and len(editValue2) == 2:
                editValue = "£" + editValue + "." + editValue2
                stockDatabase[editRow][3] = editValue
            else:
                error("Invalid Length (Must be under 6 characters, with 2 decimals)")
        else:
            error("Invalid Datatype (Numbers Only)")
    elif x > 632 and x < 732:
        if editValue == "" or editValue2 == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True and editValue2.isnumeric() == True:
            if len(editValue + editValue2) <6 and len(editValue2) == 2:
                editValue = "£" + editValue + "." + editValue2
                stockDatabase[editRow][4] = editValue
            else:
                error("Invalid Length (Must be 6 characters, with 2 decimals)")
        else:
            error("Invalid Datatype (Numbers only)")
    elif x > 732 and x < 832:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 2:
                stockDatabase[editRow][5] = editValue
            else:
                error("Invalid Length (Must be 2 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    elif x > 832 and x < 932:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 4:
                stockDatabase[editRow][6] = editValue
            else:
                error("Invalid Length (Must be 4 characters)")
        else:
            error("Invalid Datatype")
    elif x > 932 and x < 1032:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) < 4:
                stockDatabase[editRow][7] = editValue
            else:
                error("Invalid Length (Cannot be over 3 characters)")
        else:
            error("Invalid Datatype")
    elif x > 1032 and x < 1132:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) < 4:
                stockDatabase[editRow][8] = editValue
            else:
                error("Invalid Length (Cannot be over 3 characters)")
        else:
            error("Invalid Datatype")
    saveArray(editType,stockDatabase,lengthDatabase)
    subMenuFrame.destroy()
    stockMenu(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,False,None)

#Subroutine callable to sort values based on quantity in the Stock Database
def sort(data):
    data.sort()
    saveArray(data)
    stockMenu(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,printButton,highlightList)
    
#Subroutine callable to search for values in the Stock Database
def search(searchbar,database,mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,subMenuFrame):
    highlightList = []
    searchValue = searchbar.get()
    #First, the inputted value is checked against values in the array
    for searchLoop in range(len(database)):
        if searchValue in database[searchLoop][1] and searchValue != "":
            highlightList.append(searchLoop)
    searchValueShort = searchValue.replace(" ", "")
    #Next, if the value entered is blank or a is without letters or numbers, it returns an error
    if searchValueShort == "":
        error("Search Must Include Letters or Numbers")
        highlightList = None
    if highlightList == []:
        error("Search Not Found In Descriptions")
    subMenuFrame.destroy()
    stockMenu(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,False,highlightList)

#Subroutine callable to determine the positioning of the scrollbar
def getScrollbarValues(scrollbar,currentScreen):
    bottom = (scrollbar.get()[1]*100)
    top = (scrollbar.get()[0]*100)
    movementRemaining = 100 - bottom
    goToScreen(currentScreen)

#Subroutine callable to load the Stock Menu
def stockMenu():
    #Firstly the profit value, stock database and length database are loaded
    profit = getProfit()
    loop2 = 0
    stockDatabase = loadArray("stock")
    #Then the frame is created
    subMenuFrame = Frame(window, height = 1080, width = 1920, bg = "black")
    subMenuFrame.pack()
    #Next a canvas is created with an assigned scrollbar
    stockCanvas = Canvas(subMenuFrame, bg = "white", width = 1148, height = 460, scrollregion=(0,0,0,((16*30)-20)), yscrollincrement = 30)
    stockCanvas.place(x = 80, y = 168)
    stockScrollbar = Scrollbar(subMenuFrame, orient = "vertical", command = stockCanvas.yview)
    stockScrollbar.place(x = 42, y = 152, height = 482)
    stockCanvas.config(yscrollcommand=stockScrollbar.set)
    #Then a temporary button is optionally created (this button will immediatly be pressed automatically in order to determine the initial position of the scrollbar)
    #Next, buttons to clear rows, buy items and sell items are placed into the frame
    #printClears(60)
    #printSells(1265)
    #Then the back button and stock icon are placed
    stockIcon = PhotoImage(file = "images/stock.gif")
    stockLabel = Label(subMenuFrame,image = stockIcon, bg = "white", width = 50, height = 60)
    stockLabel.image = stockIcon
    stockLabel.place(x = 1300, y = 0)
    #A label is then placed displaying the curent profit, along with the button used to reset it
    monthlyProfitLabel= Label(subMenuFrame,text = ("Month's Profit:"), fg = "black", bg = "white", font = ("Helvetica", 15))
    monthlyProfitLabel.place(x = 80, y = 634)
    displayProfit = "£" + profit
    profitAmountLabel = Label(subMenuFrame,text = displayProfit, fg = "black", bg = "white", font = ("Helvetica",15))
    profitAmountLabel.place(x = 215, y = 634)
    #clearProfitButton = Button(subMenuFrame,text = "Reset", fg = "black", bg = "white", font = ("Helvetica",8),command = clearProfit())
    #clearProfitButton.place(x = 42, y = 634, width = 38, height = 30)
    #A searchbar is placed to allow users to locate values
    stockSearchbar = Entry(subMenuFrame, fg = "black", bg = "white", font = ("Helvetica",15), width = 84)
    stockSearchbar.place(x = 304, y = 636)
    searchCommand = partial(search,stockSearchbar,stockDatabase)
    stockSearchButton = Button(subMenuFrame, text = "Search", fg = "black", bg = "white", font = ("Helvetica",13), command = searchCommand)
    stockSearchButton.place(x = 1233, y = 634, height = 30, width = 70)
    #Then a button is placed to sort the database based on quantity)
    sortButton = Button(subMenuFrame, fg = "black", bg = "white", font = ("Helvetica",10), text = "Sort", command = sort())
    sortButton.place(x = 1233, y = 130, height = 25, width = 70)
    #Next, buttons used to add and remove rows from the database are added
    plusButton = Button(subMenuFrame,text = "+", bg = "white", command = appendDatabase(), height = 1)
    plusButton.place(x = 60, y = 126)
    minusButton = Button(subMenuFrame,text = "-", bg = "white", command = popDatabase(), height = 1)
    minusButton.place(x = 43, y = 126)
    errorCommand = partial(error, "Edit quantity by buying/selling items")
    #Iteration is then used to place buttons on the canvas displaying each item in the stock database (on press allowing for the editing of the item should the user be permitted)
    a = 61
    b = 0
    for loop in range(16):
        loop2 = 0
        for loop2 in range(10):
            background = "white"
            #If the Reorder point is higher than the Amount, the label's background will be red
            if int(stockDatabase[loop][9]) < int(stockDatabase[loop][8]):
               background = "red"
            #If the value is being searched for, the label's background will be yellow
            highlightList = "test"
            if highlightList != None:
                for highlightLoop in range(len(highlightList)):
                    if loop == int(highlightList[highlightLoop]) and loop2 == 1:
                        background = "yellow"
            if loop2 == 0:
                stockArrayLabel = Button(text = stockDatabase[loop][loop2], font = ("Helvetica"), bg = background,  width = 13, height = 1, command = getEditValue())
                stockCanvas.create_window(a, b, window=stockArrayLabel)
                a = a + 77
            elif loop2 == 1:
                stockArrayLabel = Button(text = stockDatabase[loop][loop2], font = ("Helvetica"), bg = background, width = 24, height = 1, command = getEditValue())
                stockCanvas.create_window(a, b, window=stockArrayLabel)
                a = a + 63
            elif loop2 == 9:
                stockArrayLabel = Button(text = stockDatabase[loop][loop2], font = ("Helvetica"), bg = background, width = 10, height = 1, command = errorCommand)
                stockCanvas.create_window(a, b, window=stockArrayLabel)
            else:
                stockArrayLabel = Button(text = stockDatabase[loop][loop2], font = ("Helvetica"), bg = background, width = 10, height = 1, command = getEditValue())
                stockCanvas.create_window(a, b, window=stockArrayLabel)
            a = a + 100
        a = 61
        b = b + 30
    b = 130
    stockArrayHeading = ["Barcode", "Description", "Pack","Unit Price", "Line Value", "VAT Code", "SRP", "PQR", "Reorder","Quantity"]
    a = 80
    #Finally, headings are placed onto the table
    for loop3 in range(10):
        if loop3 == 0:
            stockArrayHeadingLabel = Label(subMenuFrame,text = stockArrayHeading[loop3], font = ("Helvetica"), width = 13, height = 1)
            stockArrayHeadingLabel.place(x = a, y = b)
            a = a + 120
        elif loop3 == 1:
            stockArrayHeadingLabel = Label(subMenuFrame,text = stockArrayHeading[loop3], font = ("Helvetica"), width = 24, height = 1)
            stockArrayHeadingLabel.place(x = a, y = b)
            a = a + 220
        else:
            stockArrayHeadingLabel = Label(subMenuFrame,text = stockArrayHeading[loop3], font = ("Helvetica"), width = 12, height = 1)
            stockArrayHeadingLabel.place(x = a, y = b)
            a = a + 100

#Subroutine callable to edit items selected in the Shift Database
def shiftEditor(editValue,editValue2,editValue3,editValue4,x,y,editType,shiftDatabase,subMenuFrame,mainMenuFrame,status,usernameEntered,lengthDatabase,scrollbar,movementRemaining):
    topBoundary = 153
    bottomBoundary = 183
    #Firstly, the row is determined by getRow() and adjusted based on the position of the scrollbar
    editRow = getRow(0,y,topBoundary,bottomBoundary)
    if scrollbar.get()[0] != 0.0:
        percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
        editRow = int(editRow + ((int(lengthDatabase[1])-16)*(percentage/100)))
    #The column is then determined by the x co-ordinate of the cursor
    if x > 384 and x < 483:
        #Next the value entered is validated specifically to each column (Lauching an error is the value doesn't fit the correct format)
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 3:
                #Should it pass validation, the database is then updated and saved
                shiftDatabase[editRow][0] = editValue
            else:
                error("Invalid Length (Must be 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 483 and x < 708:
        if editValue == "":
                error("Please enter a value")
        elif len(editValue) < 25:
            shiftDatabase[editRow][1] = editValue
        else:
            error("Invalid Length (Must be under 25 characters)")
    if x > 708 and x < 816:
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 11:
                shiftDatabase[editRow][2] = editValue
            else:
                error("Invalid Length (Must be 11 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 816 and x < 915:
        if editValue == "" or editValue2 == "" or editValue3 == "" or editValue4 == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True and editValue2.isnumeric() == True and editValue3.isnumeric() == True and editValue4.isnumeric() == True:
            if int(editValue) < 24 and int(editValue2) < 60 and int(editValue3) < 24 and int(editValue4) < 60 and len(editValue) == 2 and len(editValue2) == 2 and len(editValue3) == 2 and len(editValue4) == 2:
                editValue = editValue + ":" + editValue2 + " - " + editValue3 + ":" + editValue4
                shiftDatabase[editRow][3] = editValue
            else:
                error("Invalid (Must be valid 24hr Clock Time)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 915 and x < 1014:
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) < 3:
                editValue = editValue + " Hours"
                shiftDatabase[editRow][4] = editValue
            else:
                error("Invalid Length (Must be under 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 1014 and x < 1114:
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) < 4:
                editValue = "£" + editValue + "/h"
                shiftDatabase[editRow][5] = editValue
            else:
                error("Invalid Length (Must be under 4 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    subMenuFrame.destroy()
    saveArray(editType,shiftDatabase,lengthDatabase)
    shiftMenu(mainMenuFrame,status,usernameEntered,scrollbar,movementRemaining,False)

#Subroutine callable to calculate what an employee should be payed and remove it from the profit
def pay(entryValue,window2,mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,subMenuFrame):
    days = float(entryValue.get())
    window2.destroy()
    #Firstly, the inputted days are checked for validity (launching an error if invalid)
    if len(str(int(days))) > 2:
        #Next, the Shift Database, Length Database and profit are loaded
        shiftDatabase = loadArray("shifts")
        profit = float(getProfit())
        for loop in range(int(lengthDatabase[1])):
            #Then the payment is determined based on the wage, absense and shift
            wage = float((shiftDatabase[loop][5])[1])
            absense = float((shiftDatabase[loop][4])[0])
            hoursList = shiftDatabase[loop][3].split("-")
            hoursListFirst = hoursList[0].split(":")
            hoursListSecond = hoursList[1].split(":")
            hoursFirst = hoursListFirst[0] + "." + hoursListFirst[1]
            hoursSecond = hoursListSecond[0] + "." + hoursListSecond[1]
            hours = float(hoursSecond) - float(hoursFirst)
            payment = wage * ((hours * days) - absense)
            profit = profit - payment
            #Next, the absense is reset
            shiftDatabase[loop][4] = "0 Hours"
        #Finally the Shift Database and profit are saved
        saveArray("shifts", shiftDatabase, lengthDatabase)
        saveProfit(profit)
    error("Cannot be over 2 digits")
    subMenuFrame.destroy()
    shiftMenu(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,False)

#Subroutine callable to open the payment entry window
def payEntry(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,subMenuFrame):
    #Firstly the status of the user is determined (returning an error if not an admin)
    if status == "admin":
        #Then, the window is opened and days worked can be entered
        window2 = Tk()
        window2.geometry("400x50")
        window2.title("Enter Days Worked")
        window2.configure(bg = "white")
        canvas = Canvas(window2, bg="white", height=50, width=400)
        canvas.pack()
        entryValue = Entry(window2, width = 45)
        canvas.create_window(150, 27, window=entryValue)
        payCommand = partial(pay, entryValue, window2,mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,subMenuFrame)
        editButton = Button(window2, text = "Confirm", font = ("Helvetica", 10), command =  payCommand)
        canvas.create_window(350, 25, window=editButton)
    else:
        error("Admin only")
        

#Subroutine callable to load the Shift Menu
def shiftMenu():
    #Firstly, the shift database and length database are loaded
    shiftDatabase = loadArray("shifts")
    #Then the frame is created
    subMenuFrame = createDefaultFrame
    #Next a canvas is created with an assigned scrollbar
    shiftCanvas = Canvas(subMenuFrame, bg = "white", width = 725, height = 460, scrollregion=(0,0,0,((16*30)-20)), yscrollincrement = 30)
    shiftCanvas.place(x = 385, y = 168)
    shiftScrollbar = Scrollbar(subMenuFrame, orient = "vertical", command = shiftCanvas.yview)
    shiftScrollbar.place(x = 347, y = 152, height = 482)
    shiftCanvas.config(yscrollcommand=shiftScrollbar.set)
    #Then a temporary button is optionally created (this button will immediatly be pressed automatically in order to determine the initial position of the scrollbar)
    #Next, buttons to clear rows and pay employees are placed into the frame
    payEntryCommand = partial(payEntry,mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,subMenuFrame)
    payButton = Button(subMenuFrame,text = "Pay Employees", bg = "white", command = payEntryCommand)
    payButton.place(x = 346, y = 633)
    printClears(365)
    shiftIcon = PhotoImage(file = "images/shiftIcon.gif")
    shiftLabel = Label(subMenuFrame,image = shiftIcon, bg = "white", width = 50, height = 60)
    shiftLabel.image = shiftIcon
    shiftLabel.place(x = 1200, y = 0, width = 200)
    #Next, buttons used to add and remove rows from the database are added
    plusButton = Button(subMenuFrame,text = "+", bg = "white", command = appendDatabase(), height = 1)
    plusButton.place(x = 365, y = 126)
    minusButton = Button(subMenuFrame,text = "-", bg = "white", command = popDatabase(), height = 1)
    minusButton.place(x = 348, y = 126)
    a = 48
    b = 0
    #Iteration is then used to place buttons on the canvas displaying each item in the stock database (on press allowing for the editing of the item should the user be permitted)
    for loop in range(16):
        loop2 = 0
        for loop2 in range(6):
            #Should "Absense" be higher than 3 hours, the background of that row will become red
            background = "white"
            if int(str(shiftDatabase[loop][4])[0]) > 3:
                background = "red"
            if loop2 == 0:
                shiftArrayLabel = Button(text = shiftDatabase[loop][loop2], font = ("Helvetica"), width = 10, height = 1, bg = background, command = getEditValue())
                shiftCanvas.create_window(a, b, window=shiftArrayLabel)
                a = a + 63
            elif loop2 == 1:
                shiftArrayLabel = Button(text = shiftDatabase[loop][loop2], font = ("Helvetica"), width = 24, height = 1, bg = background, command = getEditValue())
                shiftCanvas.create_window(a, b, window=shiftArrayLabel)
                a = a + 67
            elif loop2 == 2:
                shiftArrayLabel = Button(text = shiftDatabase[loop][loop2], font = ("Helvetica"), width = 11, height = 1, bg = background, command = getEditValue())
                shiftCanvas.create_window(a, b, window=shiftArrayLabel)
                a = a + 5
            else:
                shiftArrayLabel = Button(text = shiftDatabase[loop][loop2], font = ("Helvetica"), width = 10, height = 1, bg = background, command = getEditValue())
                shiftCanvas.create_window(a, b, window=shiftArrayLabel)
            a = a + 99
        a = 48
        b = b + 30
    shiftArrayHeading = ["ID", "Name", "Telephone", "Shift", "Absense", "Wage(£/h)"]
    a = 385
    b = 130
    #Finally, headings are placed onto the table
    for loop3 in range(6):
        if loop3 == 0:
            shiftArrayHeadingLabel = Label(subMenuFrame,text = shiftArrayHeading[loop3], font = ("Helvetica"), width = 11, height = 1, bg = "white")
            shiftArrayHeadingLabel.place(x = a, y = b)
            a = a + 100
        elif loop3 == 1:
            shiftArrayHeadingLabel = Label(subMenuFrame,text = shiftArrayHeading[loop3], font = ("Helvetica"), width = 24, height = 1, bg = "white")
            shiftArrayHeadingLabel.place(x = a, y = b)
            a = a + 220
        else:
            shiftArrayHeadingLabel = Label(subMenuFrame,text = shiftArrayHeading[loop3], font = ("Helvetica"), width = 11, height = 1, bg = "white")
            shiftArrayHeadingLabel.place(x = a, y = b)
            a = a + 100

#Subroutine callable to display confirmation of sucessful bill verification and adjust profit
def confirmBill(window3,membership):
    #Firstly, the message is displayed
    messagebox.showinfo(title = "Confirmation", message = "Bill Paid")
    #Next, profit is loaded
    profit = float(getProfit())
    #Then the discout is applied
    if membership == "None":
        profit = float(profit + 0.30)
    if membership == "Bronze":
        profit = float(profit + 0.25)
    if membership == "Silver":
        profit = float(profit + 0.20)
    if membership == "Gold":
        profit = float(profit + 0.15)
    #Finally profit is saved
    saveProfit(profit)
    window3.destroy()

#Subroutine callable to validate entered bill information, and to open a window where the user can verify the details
def billEnter(subMenuFrame,billCardIDEntry,paymentEntry,billType,membership):
    #Firstly, bill information is saved into variables
    billCardID = billCardIDEntry.get()
    payment = paymentEntry.get()
    billTypeStr = billType.get()
    membershipStr = membership.get()
    count = 0
    #Then bill information is validated (launching an error should it fail validation)
    if billCardID == "":
        error("Please enter bill card ID")
    elif len(billCardID) < 25:
        count = count + 1
    else:
        error("Invalid Length (Must be under 25 characters)")
    if payment == "":
        error("Please enter a payment")
    elif payment.isnumeric() == True:
        if len(payment) < 6:
            count = count + 1
        else:
            error("Invalid Length (Must be under 6 characters)")
    else:
        error("Invalid datatype (Must be Number")
    if billTypeStr == "":
        error("Please enter a bill type")
    else:
        count = count + 1
    if count == 3:
        billArray = [billCardID, payment, billTypeStr, membershipStr]
        billArrayTitle = ["Bill Card ID:", "Payment:", "Bill Type:", "Membership:"]
        #Next, a window is opened where the user can verify information
        window3 = Tk()
        window3.geometry("400x200")
        window3.title("Detail verification")
        window3.configure(bg = "white")
        stockCanvas = Canvas(window3, bg="white", height=200, width=400)
        stockCanvas.pack()
        text1 = stockCanvas.create_text(145,20, text = "Are these details correct?", font = ("Helvetica",15))
        y = 80
        for x in range(len(billArray)):
            arrayTitle = stockCanvas.create_text(60,y, text = billArrayTitle[x])
            arrayText = stockCanvas.create_text(200,y, text = billArray[x])
            y = y + 20
        confirmBillCommand = partial(confirmBill,window3,membershipStr)
        billConfirmationButton = Button(window3, text = "Confirm", font = ("Helvetica",15), command = confirmBillCommand)
        stockCanvas.create_window(340, 160, window=billConfirmationButton)

#Subroutine callable to load the Bill Menu
def billMenu(mainMenuFrame,status,usernameEntered):
    #Firstly, the frame is created
    subMenuFrame = createDefaultFrame("sub")
    #Next the back button and bill icon are placed
    #Then labels and entry boxes are placed where the user can input information
    billIcon = images['bill']
    billLabel = Label(subMenuFrame,image = billIcon, bg = "white", width = 60, height = 60)
    billLabel.image = billIcon
    billLabel.place(x = 1300, y = 0)
    billTypeLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Bill Type", height = 1, width = 15)
    billTypeLabel.place(x = 165, y = 251)
    billType = StringVar(window)
    billType.set("")
    billTypeEntry = OptionMenu(subMenuFrame, billType, "Council Tax", "Heating", "Water", "Internet", "Television licence")
    billTypeEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    billTypeEntry.place(x = 400, y = 250)
    billCardIDLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Bill Card ID", height = 1, width = 15)
    billCardIDLabel.place(x = 165, y = 291)
    billCardIDEntry = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    billCardIDEntry.place(x = 400, y = 290)
    paymentLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Payment (£)", height = 1, width = 15)
    paymentLabel.place(x = 165, y = 331)
    paymentEntry = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    paymentEntry.place(x = 400, y = 330)
    membershipLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Membership", height = 1, width = 15)
    membershipLabel.place(x = 165, y = 371)
    membership = StringVar(window)
    membership.set("None")
    membershipEntry = OptionMenu(subMenuFrame, membership, "None", "Bronze", "Silver", "Gold")
    membershipEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    membershipEntry.place(x = 400, y = 370)
    billEnterCommand = partial(billEnter,subMenuFrame,billCardIDEntry,paymentEntry,billType,membership)
    billEnterButton = Button(subMenuFrame,text = "Enter Details", bg = "black", fg = "white", font = ("Helvetica", 20), command = billEnterCommand)
    billEnterButton.place(x = 165, y = 410)

#Subroutine callable to display confirmation of sucessful Western Union verification and adjust the profit
def confirmWu(window3,membership):
    #Firstly, the message is displayed
    messagebox.showinfo(title = "Confirmation", message = "Transfer Complete")
    #Next, profit is loaded
    profit = float(getProfit())
    #Then the discout is applied
    if membership == "None":
        profit = float(profit + 0.30)
    if membership == "Bronze":
        profit = float(profit + 0.25)
    if membership == "Silver":
        profit = float(profit + 0.20)
    if membership == "Gold":
        profit = float(profit + 0.15)
    #Finally profit is saved
    saveProfit(profit)
    window3.destroy()

#Subroutine callable to validate entered Western Union information, and to open a window where the user can verify the details
def wuEnter(subMenuFrame,senderNameEntry,recipientNameEntry,senderEmailEntry,senderEmailEntry2,senderEmailEntry3,accountPasswordEntry,amountEntry,recipientLocation,senderFormat,recipientFormat,membership):
    #Firstly, Western Union information is saved into variables
    senderName = senderNameEntry.get()
    recipientName = recipientNameEntry.get()
    senderEmail = senderEmailEntry.get() + "@" + senderEmailEntry2.get() + "." + senderEmailEntry3.get()
    accountPassword = accountPasswordEntry.get()
    amount = amountEntry.get()
    recipientLocationStr = recipientLocation.get()
    membershipStr = membership.get()
    if recipientLocationStr.find("\n") != -1:
        recipientLocationStr = recipientLocationStr.replace("\n","")
    senderFormatStr = senderFormat.get()
    recipientFormatStr = recipientFormat.get()
    count = 0
    #Then bill information is validated (launching an error should it fail validation)
    if senderName == "":
        error("Please enter sender name")
    elif len(senderName) < 25:
        count = count + 1
    else:
        error("Invalid Length (Must be under 25 characters)")
    if recipientName == "":
        error("Please enter recipient name")
    elif len(recipientName) < 25:
        count = count + 1
    else:
        error("Invalid Length (Must be under 25 characters)")
    if senderEmail == "":
        error("Please enter a sender email")
    elif len(senderEmail) < 38:
        count = count + 1
    else:
        error("Invalid Length (Must be under 35 characters)")
    if accountPassword == "":
        error("Please enter an account password")
    else:
        count = count + 1
    if recipientLocationStr == "":
        error("Please enter a recipient location")
    else:
        count = count + 1
    if amount == "":
        error("Please enter an amount")
    elif amount.isnumeric() == True:
        if len(amount) < 6:
            count = count + 1
        else:
            error("Invalid Length (Must be under 6 characters)")
    else:
        error("Invalid Datatype (Numbers only)")
    if senderFormatStr == "":
        error("Please enter a sender format")
    else:
        count = count + 1
    if recipientFormatStr == "":
        error("Please enter a recipient format")
    else:
        count = count + 1
    if count == 8:
        #Next, a window is opened where the user can verify information
        wuArray = [senderName, recipientName, senderEmail, accountPassword, recipientLocationStr, amount, senderFormatStr, recipientFormatStr, membershipStr]
        wuArrayTitle = ["Sender Name:", "Recipient Name:", "Sender Email:", "Account Password:", "Recipient Location:", "Amount:", "Sender Format:", "Recipient Format:", "Membership:"]
        window3 = Tk()
        window3.geometry("400x200")
        window3.title("Detail verification")
        window3.configure(bg = "white")
        wuCanvas = Canvas(window3, bg="white", height=200, width=400)
        wuCanvas.pack()
        text1 = wuCanvas.create_text(145,20, text = "Are these details correct?", font = ("Helvetica",15))
        y = 40
        for x in range(len(wuArray)):
            arrayTitle = wuCanvas.create_text(60,y, text = wuArrayTitle[x])
            arrayText = wuCanvas.create_text(200 + (len(wuArray[x])),y, text = wuArray[x])
            y = y + 15
        confirmWuCommand = partial(confirmWu,window3,membershipStr)
        wuConfirmationButton = Button(window3, text = "Confirm", font = ("Helvetica",15), command = confirmWuCommand)
        wuCanvas.create_window(340, 160, window=wuConfirmationButton)

#Subroutine callable to load the Western Union Menu
def wuMenu(mainMenuFrame,status,usernameEntered):
    #Firstly, the frame is created
    subMenuFrame = createDefaultFrame("sub")
    wuIcon = PhotoImage(file = "images/wuIcon.gif")
    wuLabel = Label(subMenuFrame,image = wuIcon, bg = "white", width = 60, height = 60)
    wuLabel.image = wuIcon
    wuLabel.place(x = 1300, y = 0)
    #Then labels and entry boxes are placed where the user can input information
    senderNameLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Sender Name", height = 1, width = 15)
    senderNameLabel.place(x = 165, y = 211)
    senderNameEntry = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    senderNameEntry.place(x = 400, y = 210)
    recipientNameLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Recipient Name", height = 1, width = 15)
    recipientNameLabel.place(x = 165, y = 251)
    recipientNameEntry = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    recipientNameEntry.place(x = 400, y = 250)
    senderEmailLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Sender Email", height = 1, width = 15)
    senderEmailLabel.place(x = 165, y = 291)
    senderEmailEntry = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 16)
    senderEmailEntry.place(x = 400, y = 290)
    senderEmailLabel2 = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "@", height = 1)
    senderEmailLabel2.place(x = 649, y = 291)
    senderEmailEntry2 = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 16)
    senderEmailEntry2.place(x = 685, y = 290)
    senderEmailLabel3 = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = ".", height = 1)
    senderEmailLabel3.place(x = 927, y = 291)
    senderEmailEntry3 = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 4)
    senderEmailEntry3.place(x = 940, y = 290)
    accountPasswordLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Account Password", height = 1, width = 15)
    accountPasswordLabel.place(x = 165, y = 331)
    accountPasswordEntry = Entry(subMenuFrame,show = "*",bg = "white", font = ("Helvetica", 20), width = 40)
    accountPasswordEntry.place(x = 400, y = 330)
    recipientLocationLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Recipient Location", height = 1, width = 15)
    recipientLocationLabel.place(x = 165, y = 371)
    #The countries text file is opened to provide options for recipient location entry
    countries = open("countries.txt")
    countryArray = []
    lines = countries.readlines()
    for x in range(len(lines)):
        countryArray.append(lines[x])
    recipientLocation = StringVar(window)
    recipientLocation.set("")
    recipientLocationEntry = OptionMenu(subMenuFrame, recipientLocation, *countryArray)
    recipientLocationEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    recipientLocationEntry.place(x = 400, y = 370)
    amountLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Amount (£)", height = 1, width = 15)
    amountLabel.place(x = 165, y = 411)
    amountEntry = Entry(subMenuFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    amountEntry.place(x = 400, y = 410)
    senderFormatLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Sender Format", height = 1, width = 15)
    senderFormatLabel.place(x = 165, y = 451)
    senderFormat = StringVar(window)
    senderFormat.set("")
    senderFormatEntry = OptionMenu(subMenuFrame, senderFormat, "Cash", "Bank Transfer", "Voucher", "Cheque")
    senderFormatEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    senderFormatEntry.place(x = 400, y = 450)
    recipientFormatLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Recipient Format", height = 1, width = 15)
    recipientFormatLabel.place(x = 165, y = 491)
    recipientFormat = StringVar(window)
    recipientFormat.set("")
    recipientFormatEntry = OptionMenu(subMenuFrame, recipientFormat, "Cash", "Bank Transfer", "Voucher", "Cheque")
    recipientFormatEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    recipientFormatEntry.place(x = 400, y = 490)
    membershipLabel = Label(subMenuFrame,bg = "white", font = ("Helvetica", 19), text = "Membership", height = 1, width = 15)
    membershipLabel.place(x = 165, y = 531)
    membership = StringVar(window)
    membership.set("None")
    membershipEntry = OptionMenu(subMenuFrame, membership, "None", "Bronze", "Silver", "Gold")
    membershipEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    membershipEntry.place(x = 400, y = 530)
    wuEnterCommand = partial(wuEnter,subMenuFrame,senderNameEntry,recipientNameEntry,senderEmailEntry,senderEmailEntry2,senderEmailEntry3,accountPasswordEntry,amountEntry,recipientLocation,senderFormat,recipientFormat,membership)
    wuEnterButton = Button(subMenuFrame,text = "Enter Details", bg = "black", fg = "white", font = ("Helvetica", 20), command = wuEnterCommand)
    wuEnterButton.place(x = 165, y = 570)

#Subroutine callable to edit items selected in the Loyalty Scheme Database
def loyaltyEditor(editValue,editValue2,editValue3,x,y,editType,loyaltyDatabase,loyaltyMenuFrame,status,usernameEntered,mainMenuFrame,lengthDatabase,scrollbar,movementRemaining):
    #Firstly, the row is determined by getRow() and adjusted based on the position of the scrollbar
    topBoundary = 152
    bottomBoundary = 181
    editRow = 0
    editRow = getRow(editRow,y,topBoundary,bottomBoundary)
    if scrollbar.get()[0] != 0.0:
        percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
        editRow = int(editRow + ((int(lengthDatabase[2])-16)*(percentage/100)))
    #The column is then determined by the x co-ordinate of the cursor
    if x > 440 and x < 540:
        #Next the value entered is validated specifically to each column (Lauching an error is the value doesn't fit the correct format)
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 3:
                #Should it pass validation, the database is then updated and saved
                loyaltyDatabase[editRow][0] = editValue
            else:
                error("Invalid Length (Must be 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 540 and x < 819:
        if editValue == "":
                error("Please enter a value")
        elif len(editValue + editValue2 + editValue3) < 35:
            editValue = editValue + "@" + editValue2 + "." + editValue3
            loyaltyDatabase[editRow][1] = editValue
        else:
            error("Invalid Length (Must be under 35 characters)")
    if x > 819 and x < 919:
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 11:
                loyaltyDatabase[editRow][2] = editValue
            else:
                error("Invalid Length (Must be 11 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 919 and x < 1019:
        if editValue == "":
                error("Please enter a value")
        elif editValue == "Bronze" or editValue == "Silver" or editValue == "Gold":
            loyaltyDatabase[editRow][3] = editValue
        else:
            error("Invalid (Must be Bronze, Silver or Gold)")
    if x > 1019 and x < 1119:
        if editValue == "":
                error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) < 3:
                loyaltyDatabase[editRow][4] = editValue
            else:
                error("Invalid Length (Must be under 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    loyaltyMenuFrame.destroy()
    saveArray(editType,loyaltyDatabase,lengthDatabase)
    loyaltyMenu(loyaltyMenuFrame,status,usernameEntered,mainMenuFrame,lengthDatabase,movementRemaining,False)

#Subroutine callable to load the Loyalty Scheme Menu
def loyaltyMenu():
    #Firstly, the loyalty database and length database are loaded
    loyaltyDatabase = loadArray("loyalty")
    #Then the frame is created
    loyaltyMenuFrame = createDefaultFrame("loyalty")
    #Next a canvas is created with an assigned scrollbar
    loyaltyCanvas = Canvas(loyaltyMenuFrame, bg = "white", width = 675, height = 460, scrollregion=(0,0,0,((6*30)-20)), yscrollincrement = 30)
    loyaltyCanvas.place(x = 440, y = 166)
    loyaltyScrollbar = Scrollbar(loyaltyMenuFrame, orient = "vertical", command = loyaltyCanvas.yview)
    loyaltyScrollbar.place(x = 402, y = 152, height = 482)
    loyaltyCanvas.config(yscrollcommand=loyaltyScrollbar.set)
    #Next, buttons to clear rows are placed into the frame
    printClears(420,"loyalty")
    #Then the back button and Loyalty Scheme icon are placed
    loyaltyIcon = PhotoImage(file = "images/loyaltyIcon.gif")
    loyaltyLabel = Label(loyaltyMenuFrame, image = loyaltyIcon, bg = "white", width = 50, height = 60)
    loyaltyLabel.image = loyaltyIcon
    loyaltyLabel.place(x = 1300, y = 0)
    #Next, buttons used to add and remove rows from the database are added

    plusButton = Button(loyaltyMenuFrame,text = "+", bg = "white", command = appendDatabase(), height = 1)
    plusButton.place(x = 420, y = 126)
    minusButton = Button(loyaltyMenuFrame,text = "-", bg = "white", command = popDatabase(), height = 1)
    minusButton.place(x = 403, y = 126)
    a = 48
    b = 0
    #Iteration is then used to place buttons on the canvas displaying each item in the stock database (on press allowing for the editing of the item should the user be permitted)
    for loop in range(4):
        loop2 = 0
        for loop2 in range(5):
            if loop2 == 0:
                loyaltyArrayLabel = Button(loyaltyMenuFrame, text = loyaltyDatabase[loop][loop2], font = ("Helvetica"), width = 10, height = 1, command = getEditValue())
                loyaltyCanvas.create_window(a, b, window=loyaltyArrayLabel)
                a = a + 90
            if loop2 == 1:
                loyaltyArrayLabel = Button(loyaltyMenuFrame, text = loyaltyDatabase[loop][loop2], font = ("Helvetica"), width = 30, height = 1, command = getEditValue())
                loyaltyCanvas.create_window(a, b, window=loyaltyArrayLabel)
                a = a + 90
            else:
                a = a + 100
                loyaltyArrayLabel = Button(loyaltyMenuFrame, text = loyaltyDatabase[loop][loop2], font = ("Helvetica"), width = 10, height = 1, command = getEditValue())
                loyaltyCanvas.create_window(a, b, window=loyaltyArrayLabel)
        a = 48
        b = b + 30
    loyaltyArrayHeading = ["CustomerID", "Email", "Telephone", "Status", "Parcel Total"]
    a = 437
    b = 128
    #Finally, headings are placed onto the table
    for loop3 in range(5):
        if loop3 == 1:
            loyaltyArrayHeadingLabel = Label(loyaltyMenuFrame,text = loyaltyArrayHeading[loop3], font = ("Helvetica"), width = 31, height = 1)
            loyaltyArrayHeadingLabel.place(x = a, y = b)
            a = a + 180
        else:
            loyaltyArrayHeadingLabel = Label(loyaltyMenuFrame,text = loyaltyArrayHeading[loop3], font = ("Helvetica"), width = 11, height = 1)
            loyaltyArrayHeadingLabel.place(x = a, y = b)
        a = a + 100

#Subroutine callable to edit items selected in the Previous Parcels Database
def previousParcelsEditor(editValue,editValue2,editValue3,x,y,editType,previousParcelsDatabase,loyaltyMenuFrame,status,usernameEntered,mainMenuFrame,lengthDatabase,scrollbar,movementRemaining):
    topBoundary = 152
    bottomBoundary = 181
    editRow = 0
    #Firstly, the row is determined by getRow() and adjusted based on the position of the scrollbar
    editRow = getRow(editRow,y,topBoundary,bottomBoundary)
    if scrollbar.get()[0] != 0.0:
        percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
        editRow = int(editRow + ((int(lengthDatabase[3])-16)*(percentage/100)))
    #The column is then determined by the x co-ordinate of the cursor
    if x > 480 and x < 580:
        #Next the value entered is validated specifically to each column (Lauching an error is the value doesn't fit the correct format)
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 3:
                #Should it pass validation, the database is then updated and saved
                previousParcelsDatabase[editRow][0] = editValue
            else:
                error("Invalid Length (Must be 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 580 and x < 680:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 3:
                previousParcelsDatabase[editRow][1] = editValue
            else:
                error("Invalid Length (Must be 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 680 and x < 780:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 2 and len(editValue2) == 2:
                if int(editValue) < 24 and int(editValue2) < 60:
                    editValue = editValue + ":" + editValue2
                    previousParcelsDatabase[editRow][2] = editValue
                else:
                    error("Invald (Must be valid 24hr Clock Time)")
            else:
                error("Invalid Length (Must be 4 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 780 and x < 880:
        if editValue == "" or editValue2 == "" or editValue3 == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 2 and len(editValue2) == 2 and len(editValue3) == 4:
                if editValue2 == "01" or editValue2 == "03" or editValue2 == "05" or editValue2 == "07" or editValue2 == "08" or editValue2 == "10" or editValue2 == "12" and int(editValue) <= 31:
                        editValue = editValue + "/" + editValue2 + "/" + editValue3
                        previousParcelsDatabase[editRow][3] = editValue
                elif editValue2 == "04" or editValue2 == "06" or editValue2 == "09" or editValue2 == "11" and int(editValue) <= 30:
                        editValue = editValue + "/" + editValue2 + "/" + editValue3
                        previousParcelsDatabase[editRow][3] = editValue
                elif editValue2 == "02" and int(editValue) <= 29:
                        editValue = editValue + "/" + editValue2 + "/" + editValue3
                        previousParcelsDatabase[editRow][3] = editValue
                else:
                    error("Invalid Date")
            else:
                error("Invalid Length (Must be in dd/mm/yyyy format)")
        else:
            error("Invalid Datatype (Numbers only)")
    loyaltyMenuFrame.destroy()
    saveArray(editType,previousParcelsDatabase,lengthDatabase)
    previousParcelsMenu()

#Subroutine callable to load the Previous Parcels Menu
def previousParcelsMenu():
    previousParcelsDatabase = loadArray("loyalty")
    #Then the frame is created
    loyaltyMenuFrame = createDefaultFrame("loyalty")
    #Next a canvas is created with an assigned scrollbar
    loyaltyCanvas = Canvas(loyaltyMenuFrame, bg = "white", width = 395, height = 460, scrollregion=(0,0,0,(((16)*30)-20)), yscrollincrement = 30)
    loyaltyCanvas.place(x = 480, y = 166)
    loyaltyScrollbar = Scrollbar(loyaltyMenuFrame, orient = "vertical", command = loyaltyCanvas.yview)
    loyaltyScrollbar.place(x = 440, y = 152, height = 482)
    loyaltyCanvas.config(yscrollcommand=loyaltyScrollbar.set)
    #Then the back button and Parcel icon are placed
    parcelIcon = PhotoImage(file = "images/parcelIcon.gif")
    parcelLabel = Label(loyaltyMenuFrame,image = parcelIcon, bg = "white", width = 60, height = 60)
    parcelLabel.image = parcelIcon
    parcelLabel.place(x = 1300, y = 0)
    a = 480
    b = 125
    #Finally, headings are placed onto the table
    for _ in range(4):
        parcelArrayHeadingLabel = Label(loyaltyMenuFrame,text = "test", font = ("Helvetica"), width = 11, height = 1)
        parcelArrayHeadingLabel.place(x = a, y = b)
        a = a + 100

#Subroutine callable to edit items selected in the Parcel Database
def parcelEditor(editValue,editValue2,editValue3,x,y,editType,parcelDatabase,subMenuFrame,mainMenuFrame,status,usernameEntered,lengthDatabase,scrollbar,movementRemaining):
    topBoundary = 152
    bottomBoundary = 181
    editRow = 0
    #Firstly, the row is determined by getRow() and adjusted based on the position of the scrollbar
    editRow = getRow(editRow,y,topBoundary,bottomBoundary)
    if scrollbar.get()[0] != 0.0:
        percentage = 100 - (((100 - ((scrollbar.get()[1]*100)))/movementRemaining) * 100)
        editRow = int(editRow + ((int(lengthDatabase[3])-16)*(percentage/100)))
    #The column is then determined by the x co-ordinate of the cursor
    if x > 480 and x < 580:
        #Next the value entered is validated specifically to each column (Lauching an error is the value doesn't fit the correct format)
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 3:
                #Should it pass validation, the database is then updated and saved
                parcelDatabase[editRow][0] = editValue
            else:
                error("Invalid Length (Must be 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 580 and x < 680:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 3:
                parcelDatabase[editRow][1] = editValue
            else:
                error("Invalid Length (Must be 3 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 680 and x < 780:
        if editValue == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 2 and len(editValue2) == 2:
                if int(editValue) < 24 and int(editValue2) < 60:
                    editValue = editValue + ":" + editValue2
                    parcelDatabase[editRow][2] = editValue
                else:
                    error("Invald (Must be valid 24hr Clock Time)")
            else:
                error("Invalid Length (Must be 4 characters)")
        else:
            error("Invalid Datatype (Numbers only)")
    if x > 780 and x < 880:
        if editValue == "" or editValue2 == "" or editValue3 == "":
            error("Please enter a value")
        elif editValue.isnumeric() == True:
            if len(editValue) == 2 and len(editValue2) == 2 and len(editValue3) == 4:
                if editValue2 == "01" or editValue2 == "03" or editValue2 == "05" or editValue2 == "07" or editValue2 == "08" or editValue2 == "10" or editValue2 == "12" and int(editValue) <= 31:
                        editValue = editValue + "/" + editValue2 + "/" + editValue3
                        parcelDatabase[editRow][3] = editValue
                elif editValue2 == "04" or editValue2 == "06" or editValue2 == "09" or editValue2 == "11" and int(editValue) <= 30:
                        editValue = editValue + "/" + editValue2 + "/" + editValue3
                        parcelDatabase[editRow][3] = editValue
                elif editValue2 == "02" and int(editValue) <= 29:
                        editValue = editValue + "/" + editValue2 + "/" + editValue3
                        parcelDatabase[editRow][3] = editValue
                else:
                    error("Invalid Date")
            else:
                error("Invalid Length (Must be in dd/mm/yyyy format)")
        else:
            error("Invalid Datatype (Numbers only)")
    subMenuFrame.destroy()
    saveArray(editType,parcelDatabase,lengthDatabase)
    parcelMenu(mainMenuFrame,status,usernameEntered,lengthDatabase,movementRemaining,False)

#Subroutine callable to load the Parcel Menu
def parcelMenu():
    #Firstly, the Parcel database and length database are loaded
    parcels = loadArray("parcels")
    #Then the frame is created
    parcelFrame = createDefaultFrame("sub")
    #Next a canvas is created with an assigned scrollbar
    parcelCanvas = Canvas(parcelFrame, bg = "white", width = 395, height = 460, scrollregion=(0,0,0,290), yscrollincrement = 30)
    parcelCanvas.place(x = 480, y = 166)
    parcelScrollbar = Scrollbar(parcelFrame, orient = "vertical", command = parcelCanvas.yview)
    parcelScrollbar.place(x = 440, y = 152, height = 482)
    parcelCanvas.config(yscrollcommand=parcelScrollbar.set)
    #Next, buttons to clear rows are placed into the frame
    printClears(460, parcelFrame)
    parcelLabel = Label(parcelFrame,image = images["parcel"], bg = "white", width = 60, height = 60)
    parcelLabel.place(x = 1300, y = 0)
    #Next, buttons linking to the Loyalty Scheme and Previous Parcels menus are placed
    loyaltyButton = Button(parcelFrame,text = "Loyalty Scheme", fg = "white", bg = "black", font = ("Helvetica", 15), command = loyaltyMenu)
    loyaltyButton.place(x = 150, y = 700)
    previousParcelsButton = Button(parcelFrame,text = "Previous Parcels", fg = "white", bg = "black", font = ("Helvetica", 15), command = previousParcelsMenu)
    previousParcelsButton.place(x = 350, y = 700)
    position = 48
    #Iteration is then used to place buttons on the canvas displaying each item in the stock database (on press allowing for the editing of the item should the user be permitted)
    #Finally, headings are placed onto the table
    for _ in range(4):
        parcelArrayHeadingLabel = Label(parcelFrame,text = "temp", font = ("Helvetica"), width = 11, height = 1)
        parcelArrayHeadingLabel.place(x = position, y = 0)
        position += 100

#Subroutine callable to validate entered Mobile Top-up information, and to open a window where the user can verify the details
def enterMobileInfo(phoneNumber,serviceProvider,topUpAmount,membership):
    #Firstly, Mobile Top-up information is saved into variables
    count = 0
    #Then top-up information is validated (launching an error should it fail validation)
    if phoneNumber == "" or phoneNumber.isnumeric() == False:
        error("Please enter a valid phone number")
    if topUpAmount == "" or topUpAmount.isnumeric() == False:
        error("Please enter a valid top-up amount")
    if serviceProvider == "":
        error("Please enter a service provider")
    else:
        if len(phoneNumber) != 11:
            error("Invalid Length (Must be 11 characters)")
        if len(topUpAmount) >= 6:
            error("Invalid Length (Must be under 6 characters)")
        else:
            #Next, profit is loaded
            profit = float(getProfit())
            #Then the discout is applied
            if membership == "None":
                profit = profit + 0.30
            if membership == "Bronze":
                profit = profit + 0.25
            if membership == "Silver":
                profit = profit + 0.20
            if membership == "Gold":
                profit = profit + 0.15
            messagebox.showinfo(title = "Confirmation", message = "Top-up Complete")
            saveProfit(profit)
            #Finally profit is saved

#Subroutine callable to load the Mobile Top-up Menu
def mobileMenu():
    #Firstly, the frame is created
    mobileFrame = createDefaultFrame("sub")
    mobileLabel = Label(mobileFrame,image = images["mobile"], bg = "white", width = 50, height = 60)
    mobileLabel.place(x = 1200, y = 0)
    #Then labels and entry boxes are placed where the user can input information
    phoneNumberLabel = Label(mobileFrame,bg = "white", font = ("Helvetica", 19), text = "Phone Number", height = 1, width = 15)
    phoneNumberLabel.place(x = 165, y = 291)
    phoneNumberTextBox = Entry(mobileFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    phoneNumberTextBox.place(x = 400, y = 290)
    serviceProviderLabel = Label(mobileFrame,bg = "white", font = ("Helvetica", 19), text = "Service Provider", height = 1, width = 15)
    serviceProviderLabel.place(x = 165, y = 331)
    serviceProvider = StringVar(window)
    serviceProvider.set("")
    serviceProviderEntry = OptionMenu(mobileFrame,serviceProvider, "EE", "Three", "Vodafone", "O2")
    serviceProviderEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    serviceProviderEntry.place(x = 400, y = 330)
    topUpAmountLabel = Label(mobileFrame,bg = "white", font = ("Helvetica", 19), text = "Top-up Amount (£)", height = 1, width = 15)
    topUpAmountLabel.place(x = 165, y = 371)
    topUpAmountTextBox = Entry(mobileFrame,bg = "white", font = ("Helvetica", 20), width = 40)
    topUpAmountTextBox.place(x = 400, y = 370)
    membershipLabel = Label(mobileFrame,bg = "white", font = ("Helvetica", 19), text = "Membership", height = 1, width = 15)
    membershipLabel.place(x = 165, y = 411)
    membership = StringVar(window)
    membership.set("None")
    membershipEntry = OptionMenu(mobileFrame, membership, "None", "Bronze", "Silver", "Gold")
    membershipEntry.configure(bg = "white", font = ("Helvetica", 13), width = 62, height = 1)
    membershipEntry.place(x = 400, y = 410)
    mobileEnterCommand = partial(enterMobileInfo,phoneNumberTextBox.get(),serviceProvider,topUpAmountTextBox.get(),membership)
    mobileButton = Button(mobileFrame,text = "Enter Details", bg = "black", fg = "white", font = ("Helvetica", 20), command = mobileEnterCommand)
    mobileButton.place(x = 165, y = 450)

def createDefaultFrame(page):
    #Firstly, the frame is created
    frame = Frame(window, height = 1080, width = 1920, bg = "black")
    frame.pack()
    #Next the back button is placed
    backButton = Button(frame,image = images['back.gif'] , bg = "white", command = lambda:[frame.destroy(), back(page)])
    backButton.place(x = 0, y = 0)
    return frame

#Subroutine callable to load the Main Menu
def mainMenu():
    mainMenuFrame = createDefaultFrame("main")
    #Next labels showing the user's status and username are placed
    welcomeLabel = Label(mainMenuFrame, text = ("Welcome","test"), fg = "white", bg = "black", font = ("Helvetica", 15))
    welcomeLabel.place(x = 580, y = 0)
    #Next, links to each system are placed
    stockMenuButton = Button(mainMenuFrame, image = images["stock.gif"], bg = "white", command = lambda:[mainMenuFrame.destroy(), stockMenu()])
    stockMenuButton.place(x = 390, y = 300, width = 200)
    shiftMenuButton = Button(mainMenuFrame, image = images["shift.gif"], bg = "white", command = lambda:[mainMenuFrame.destroy(), shiftMenu()])
    shiftMenuButton.place(x = 590, y = 300, width = 200)
    billMenuButton = Button(mainMenuFrame, image = images["bill.gif"], bg = "white", command = lambda:[mainMenuFrame.destroy(), billMenu()])
    billMenuButton.place(x = 790, y = 300, width = 200)
    wuMenuButton = Button(mainMenuFrame, image = images["wu.gif"], bg = "white", command = lambda:[mainMenuFrame.destroy(), wuMenu()])
    wuMenuButton.place(x = 390, y = 371, width = 200)
    parcelMenuButton = Button(mainMenuFrame, image = images["parcel.gif"], bg = "white", command = lambda:[mainMenuFrame.destroy(), parcelMenu()])
    parcelMenuButton.place(x = 590, y = 371, width = 200)
    mobileMenuButton = Button(mainMenuFrame, image = images["mobile.gif"], bg = "white", command = lambda:[mainMenuFrame.destroy(), mobileMenu()])
    mobileMenuButton.place(x = 790, y = 371, width = 200)

#Subroutine callable to process login attempts
def loginAttempt(usernameEntered,passwordEntered):
    #The Shift Database is loaded
    shifts = loadArray("shifts")
    #Next, each name in the shift database is compared to the username entered
    destination = "login"
    status = "user"
    usernameAccepted = False
    for loop in range(len(shifts)):
        print(usernameEntered, " == ", shifts[loop][1])
        if usernameEntered == shifts[loop][1]:
            usernameAccepted = True
            break
    if usernameAccepted != True:
        error("Incorrect Username")
    #Appropriate errors are displayed should usernames or passwords not match
    else:
        if usernameEntered == shifts[0][1]:
            status = "admin"
        if (status == "user" and passwordEntered == "UserPass123") or (status == "admin" and passwordEntered == "AdminPass123"):
            destination = "main"
        else:
            error("Incorrect Password")
    #If username and password are correct, the Main Menu is opened
    goToScreen(destination)

#Subroutine callable to open the Login Menu
def loginMenu():
    page = "login"
    #Firstly, the frame is created
    loginFrame = createDefaultFrame("login")
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
    window.mainloop()

loadImages()
loginMenu()