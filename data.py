stock = []
employees = []
passwords = []
rota = []

storeData = [stock, employees, passwords, rota]

class StockData:
    def __init__(self,fields):
        if fields == []:
            fields = ["","","","","","",""]
        self.itemId = fields[0]
        self.name = fields[1]
        self.barcode = fields[2]
        self.quantity = fields[3]
        self.reorderPoint = fields[4]
        self.unitPrice = fields[5]
        self.lineValue = fields[6]
    def __del__(self):
        stock.remove(self)
    def save(self):
        stock.append(self)
    def getPath(self):
        return "classes/stock.txt"
    
class EmployeeData:
    def __init__(self,fields):
        if fields == []:
            ["","","","","",""]
        self.employeeId = fields[0]
        self.name = fields[1]
        self.phoneNumber = fields[2]
        self.status = fields[3]
        self.timeWorked = fields[4]
        self.timeMissed = fields[5]
    def __del__(self):
        employees.remove(self)
    def save(self):
        employees.append(self)
    def getPath(self):
        return "classes/employees.txt"

class PasswordData:
    def __init__(self,fields):
        self.employeeId = fields[0]
        self.password = fields[1]
    def save(self):
        passwords.append(self)
    def getPath(self):
        return "classes/passwords.txt"
    
class RotaData:
    def __init__(self,fields):
        if fields == []:
            fields = ["","","","",""]
        self.staff = fields[0]
        self.date = fields[1]
        self.position = fields[2]
        self.shiftStart = fields[3]
        self.shiftEnd = fields[4]
    def __del__(self):
        rota.remove(self)
    def save(self):
        rota.append(self)
    def getPath(self):
        return "classes/rota.txt"
