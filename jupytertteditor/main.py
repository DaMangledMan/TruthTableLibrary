# Creates a classes that simplifies the process to create and display a truth table.
# To create an instance of the class
#     'classInstance = TruthTable(numberOfVariablesDesired)
# To create a new column that compares two variables
#     'classInstance.createColumn("columnName", not for the first term {given in the form of a bool(True for ~P : False for P)}, Index of the first column you are comparing, Operator to be used {'and', 'or', 'xor', 'implies', and 'iff'}, not for the second term {given in the form of a bool(True for ~P : False for P)}, Index of the second column you are comparing)
# To create a new column that gives the not version of one other column
#     'classInstance.createNotColumn("columnName", Index of the column you are altering)
# To display the truth table
#     'classInstance.display()'

class TruthTable:
    def __init__(self, varCount: int):
        self.varCount = varCount
        # calculates the number of rows required based on the number of variables needed
        self.numOfRows = 2 ** self.varCount
        # Serves as the headers for each column
        self.head = []
        for i in range(self.varCount):
            r = int(i/26)
            self.head.append(f"{chr(65 + i - (26 * r)) * (r+1)}")
        # creates the columns of the initial variables of the truth table
        self.columns = []
        for i in range(self.varCount):
            col = []
            colCount = len(self.columns)
            for x in range(self.numOfRows // (2 ** colCount)):
                for y in range(2 ** colCount):
                    if x%2 == 0:
                        col.append(True)
                    else:
                        col.append(False)
            self.columns.append(col)
        self.table = {}
        for i in range(len(self.head)):
            self.table[self.head[i]] = [self.head[i], self.columns[-(i + 1)]]

    def changeColumnName(self, colIndex: int, newName: str) -> None:
        self.head[colIndex] = newName

    # creates a new column based on the bools of two other columns
    def createColumn(self, colName: str, notX: bool, colNameX: str, operator: str, notY: bool, colNameY: str) -> None:
        col = []
        # determines what operator is being used
        match operator:
            # creates the column for the and operator
            case "and":
                xy = self._formatXY(notX, colNameX, notY, colNameY)
                for i in range(self.numOfRows):
                    if xy[0][i] and xy[1][i]:
                        col.append(True)
                    else:
                        col.append(False)
            # creates the column for the or operator
            case "or":
                xy = self._formatXY(notX, colNameX, notY, colNameY)
                for i in range(self.numOfRows):
                    if xy[0][i] or xy[1][i]:
                        col.append(True)
                    else:
                        col.append(False)
            # creates the column for the xor operator
            case "xor":
                xy = self._formatXY(notX, colNameX, notY, colNameY)
                for i in range(self.numOfRows):
                    if self._xor(xy[0][i], xy[1][i]):
                        col.append(True)
                    else:
                        col.append(False)
            # creates the column for the implies operator
            case "implies":
                xy = self._formatXY(notX, colNameX, notY, colNameY)
                for i in range(self.numOfRows):
                    if self._implies(xy[0][i], xy[1][i]):
                        col.append(True)
                    else:
                        col.append(False)
            # creates the column for the iff operator
            case "iff":
                xy = self._formatXY(notX, colNameX, notY, colNameY)
                for i in range(self.numOfRows):
                    if self._iff(xy[0][i], xy[1][i]):
                        col.append(True)
                    else:
                        col.append(False)
            # catches when an improper operator is given
            case _:
                print("Invalid operator")
                pass
        self.table[colName] = [colName, col]

    def createNotColumn(self, colName: str, colNameX: str) -> None:
        col = []
        for i in range(self.numOfRows):
            if self.table[colNameX][1][i]:
                col.append(False)
            else:
                col.append(True)
        self.table[colName] = [colName, col]
    
    def removeColumn(self, colName: str) -> None:
        del self.table[colName]

    def _formatXY(self, notX: bool, colNameX: str, notY: bool, colNameY: str):
        colX = self.table[colNameX][1]
        colY = self.table[colNameY][1]
        if notX:
            for i in range(self.numOfRows):
                if colX[i]:
                    colX[i] = False
                else:
                    colX[i] = True
        if notY:
            for i in range(self.numOfRows):
                if colY[i]:
                    colY[i] = False
                else:
                    colY[i] = True
        return [colX, colY]

    def _xor(self, p: bool, q: bool) -> bool:
        return p != q

    def _implies(self, p: bool, q: bool) -> bool:
        return not p or q

    def _iff(self, p: bool, q: bool) -> bool:
        return not self.xor(p, q)

    def display(self) -> None:
        headerLen = []
        for i in self.table:
            x = len(self.table[i][0])
            if x < 6:
                x = 6
            x += 3
            headerLen.append(x)
        x = 0
        for i in self.table:
            print(i.rjust(headerLen[x]), end=" |")
            x += 1
        print("")
        for n in range(self.numOfRows):
            x = 0
            for i in self.table:
                print(str(self.table[i][1][n]).rjust(headerLen[x]), end=" |")
                x += 1
            print("")




TT = TruthTable(3)
TT.createColumn("not A and B", True, "A", "and", False, "B")
TT.createNotColumn("not A", "A")
TT.display()
TT.removeColumn("C")
TT.display()