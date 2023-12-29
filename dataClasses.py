class StockData:
    def __init__(self,fields):
        self.itemId = fields[0]
        self.name = fields[1]
        self.barcode = fields[2]
        self.quantity = fields[3]
        self.reorderPoint = fields[4]
        self.unitPrice = fields[5]
        self.lineValue = fields[6]
    def getPath(self):
        return "classes/stock.txt"
    def getCharLimit(self,columnNum):
        return [10,20,11,12,12,12,12][columnNum]
    
class EmployeeData:
    def __init__(self,fields):
        self.employeeId = fields[0]
        self.name = fields[1]
        self.phoneNumber = fields[2]
        self.status = fields[3]
        self.timeWorked = fields[4]
        self.timeMissed = fields[5]
    def getPath(self):
        return "classes/employees.txt"
    def getCharLimit(self,columnNum):
        return [5,20,11,10,5,5][columnNum]

class DeliveryData:
    def __init__(self,fields):
        self.cageId = fields[0]
        self.stockType = fields[1]
        self.arrivalTime = fields[2]
        self.arrivalDate = fields[3]
        self.itemCount = fields[4]
    def getPath(self):
        return "classes/deliveries.txt"
    def getCharLimit(self,columnNum):
        return [10,20,10,10,5][columnNum]