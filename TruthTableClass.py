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

    def changeColumnName(self, colIndex: int, newName: str) -> None:
        self.head[colIndex] = newName

    # creates a new column based on the bools of two other columns
    def createColumn(self, colName: str, notX: bool, colIndexX: int, operator: str, notY: bool, colIndexY: int) -> None:
        # determines what operator is being used
        match operator:
            # creates the column for the and operator
            case "and":
                self._addEmptyColumn(colName)
                xy = self._formatXY(notX, colIndexX, notY, colIndexY)
                for i in range(self.numOfRows):
                    if xy[0][i] and xy[1][i]:
                        self.columns[0].append(True)
                    else:
                        self.columns[0].append(False)
                pass
            # creates the column for the or operator
            case "or":
                self._addEmptyColumn(colName)
                xy = self._formatXY(notX, colIndexX, notY, colIndexY)
                for i in range(self.numOfRows):
                    if xy[0][i] or xy[1][i]:
                        self.columns[0].append(True)
                    else:
                        self.columns[0].append(False)
                pass
            # creates the column for the xor operator
            case "xor":
                self._addEmptyColumn(colName)
                xy = self._formatXY(notX, colIndexX, notY, colIndexY)
                for i in range(self.numOfRows):
                    if self._xor(xy[0][i], xy[1][i]):
                        self.columns[0].append(True)
                    else:
                        self.columns[0].append(False)
                pass
            # creates the column for the implies operator
            case "implies":
                self._addEmptyColumn(colName)
                xy = self._formatXY(notX, colIndexX, notY, colIndexY)
                for i in range(self.numOfRows):
                    if self._implies(xy[0][i], xy[1][i]):
                        self.columns[0].append(True)
                    else:
                        self.columns[0].append(False)
                pass
            # creates the column for the iff operator
            case "iff":
                self._addEmptyColumn(colName)
                xy = self._formatXY(notX, colIndexX, notY, colIndexY)
                for i in range(self.numOfRows):
                    if self._iff(xy[0][i], xy[1][i]):
                        self.columns[0].append(True)
                    else:
                        self.columns[0].append(False)
                pass
            # catches when an improper operator is given
            case _:
                print("Invalid operator")
                pass

    def createNotColumn(self, colName: str, colIndex: int) -> None:
        self.head.append(colName)
        self.columns.insert(0, [])
        # edits the column index to work with how its programmed
        colNum = -(colIndex + 1)
        for i in range(self.numOfRows):
            if not self.columns[colNum][i]:
                self.columns[0].append(True)
            else:
                self.columns[0].append(False)

    def _addEmptyColumn(self, colName: str) -> None:
        self.head.append(colName)
        self.columns.insert(0, [])

    def _formatXY(self, notX: bool, colIndexX: int, notY: bool, colIndexY: int) -> tuple:
        # edits the column index to work with how its programmed
        colX = -(colIndexX + 1)
        colY = -(colIndexY + 1)
        # creates empty lists to store the bool values of X and Y
        colxBools = []
        colyBools = []
        for i in range(self.numOfRows):
            if notX:
                X = not self.columns[colX][i]
            else:
                X = self.columns[colX][i]
            colxBools.append(X)
            if notY:
                Y = not self.columns[colY][i]
            else:
                Y = self.columns[colY][i]
            colyBools.append(Y)
        return (colxBools, colyBools)

    def _xor(self, p: bool, q: bool) -> bool:
        return p != q

    def _implies(self, p: bool, q: bool) -> bool:
        return not p or q

    def _iff(self, p: bool, q: bool) -> bool:
        return not self.xor(p, q)

    def display(self) -> None:
        headerLen = []
        for i in range(len(self.head)):
            x = len(self.head[i])
            if x < 6:
                x = 6
            x += 3
            headerLen.append(x)
        for i in range(len(self.head)):
            print(self.head[i].rjust(headerLen[i]), end=" |")
        print("")
        for i in range(self.numOfRows):
            for n in range(len(self.head)):
                print(str(self.columns[-(n+1)][i]).rjust(headerLen[n]), end=" |")
            print("")



TT = TruthTable(3)
TT.createColumn("not A and B", True, 0, "and", False, 1)
TT.createColumn("(not A and B) xor not C", False, 3, "xor", True, 2)
TT.createNotColumn("not ((not A and B) xor not C)", 4)
TT.display()