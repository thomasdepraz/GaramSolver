import random as rd
import operator, copy

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,  # use operator.div for Python 2
    '%' : operator.mod,
    '^' : operator.xor,
}

grid = []
operations = []

cells = []
globalOperations = []
linkingNums = []
linkingOperations = []
def TestCandidates(candidates, num, opTypesH, values, operations) :
    for candidate in candidates : #Test Every candidates
            testOps = copy.copy(opTypesH)
            rd.shuffle(testOps)    
            for operation in testOps : # Test different operation to try and match the candidate
                rd.shuffle(values)
                for value in values : 
                    result = str(ops[operation](num[0],value))
                    if len(result) > 1 and int(result) > 0 and int(result[1]) == candidate :  # we have a match
                        operations[3] = operation
                        num[9] = value
                        num[8] = int(result[0])
                        num[7] = int(result[1])
                        for value in values : 
                            if ops[operations[2]](num[7],value) == num[5] : 
                                num[6] = value
                                break
                        if num[6] == -1 :
                            print('ERROR')
                        return   

def GenerateCell() : 
    num = []
    operations = []
    opTypesH = ['*','+','-']
    opTypesV = ['*','+']
    values = [0,1,2,3,4,5,6,7,8,9]
    
    for i in range(10) : 
        num.append(-1)
    for i in range(4) : 
        operations.append('none')

    # Generate first number
    num[0] = rd.randint(1,9)

    # Generate first operator
    operations[0] = opTypesH[rd.randint(0,2)]

    if operations[0] == '+' : 
        num[1] = rd.randint(0,9-num[0])
    elif operations[0] == '-' : 
        num[1] = rd.randint(0, num[0] - 1)
    elif operations[0] == '*' : 
        if num[0] == 1 : 
            num[1] = rd.randint(1,9)
        elif num[0] == 2 : 
            num[1] = rd.randint(1,4)
        elif num[0] == 3 : 
            num[1] = rd.randint(1,3)
        elif num[0] == 4 : 
            num[1] = rd.randint(1,2)
        else : 
            num[1] = 1


    num[2] = ops[operations[0]](num[0],num[1])

    # Generate next operator :
    if(num[2]) > 1  : 
        operations[1] = opTypesV[rd.randint(0,1)]
    else  : 
        operations[1] = '+'

    if operations[1] == '+' :
        num[3] = rd.randint(10-num[2], 9)
    elif operations[1] == '*' :
        if num[2] == 2 : 
            num[3] = rd.randint(5,9)
        elif num[2] == 3 : 
            num[3] = rd.randint(4,9)
        elif num[2] == 4 : 
            num[3] = rd.randint(3,9)
        else : 
            num[3] = rd.randint(2,9)

    result = str(ops[operations[1]](num[2],num[3]))

    num[4] = int(result[0])
    num[5] = int(result[1])

    #Reverse engineer the rest of the cell
    rd.shuffle(opTypesH)
    for op in opTypesH : 
        candidates = []
        candidates.clear()
        operations[2] = op

        if op == '+' : 
            for i in range(0, num[5] + 1) : 
                candidates.append(i)
        elif op == '-' : 
            for i in range(num[5] ,10) : 
                candidates.append(i) 
        elif op == '*' : 
            if num[5] > 0 : 
                candidates.append(1)
                candidates.append(num[5])
                if num[5] % 2 == 0 : 
                    candidates.append(2)
                if num[5] % 3 == 0 :
                    candidates.append(3)
                if num[5] % 4 == 0 : 
                    candidates.append(4)
                if 0 in candidates :
                    candidates.remove(0)
                    
            else : 
                for i in range(0, 1) : 
                    candidates.append(i)   
        
        rd.shuffle(candidates)
        TestCandidates(candidates, num, opTypesH, values, operations)

    #Fill in last number
    cells.append(num)
    globalOperations.append(operations)

def CheckMatching(valueA, valueB) : 
    opTypes = ['*','+','-']
    values = [0,1,2,3,4,5,6,7,8,9]

    rd.shuffle(opTypes)
    rd.shuffle(values)

    for operations in opTypes : 
        for value in values :
            if ops[operations](valueA, value) == valueB : 
                #add operation
                linkingOperations.append(operations)
                #add new Value
                linkingNums.append(value)
                return True
    
    return False

def PrintGaram() : 
    print(str(cells[0][0]) + ' ' + globalOperations[0][0] + ' ' + str(cells[0][1]) + ' = ' + str(cells[0][2]) + '       ' + str(cells[1][0]) + ' ' + globalOperations[1][0]+ ' ' + str(cells[1][1]) + ' = ' + str(cells[1][2]))
    print(globalOperations[0][3] + '       ' + globalOperations[0][1] + '       ' + globalOperations[1][3] + '       ' + globalOperations[1][1])
    print(str(cells[0][9]) + '       ' + str(cells[0][3]) + ' ' + linkingOperations[0] + ' ' + str(linkingNums[0]) + ' = ' + str(cells[1][9]) + '       ' + str(cells[1][3]))
    print('=' + '       ' + '=' + '       ' + '=' + '       ' + '=')
    print(str(cells[0][8]) + '       ' + str(cells[0][4]) + '       ' + str(cells[1][8]) + '       ' + str(cells[1][4]))
    print(str(cells[0][7]) + ' ' + globalOperations[0][2] + ' ' + str(cells[0][6]) + ' = ' + str(cells[0][5]) + '       ' + str(cells[1][7]) + ' ' + globalOperations[1][2]+ ' ' + str(cells[1][6]) + ' = ' + str(cells[1][5]))
   
    print('    ' + linkingOperations[3] + '               ' + linkingOperations[1])
    print('    ' + str(linkingNums[3]) + '               ' + str(linkingNums[1]))
    print('    ' + '=' + '               ' + '=')
    
    print(str(cells[3][0]) + ' ' + globalOperations[3][0] + ' ' + str(cells[3][1]) + ' = ' + str(cells[3][2]) + '       ' + str(cells[2][0]) + ' ' + globalOperations[2][0]+ ' ' + str(cells[2][1]) + ' = ' + str(cells[2][2]))
    print(globalOperations[3][3] + '       ' + globalOperations[3][1] + '       ' + globalOperations[2][3] + '       ' + globalOperations[2][1])
    print(str(cells[3][9]) + '       ' + str(cells[3][3]) + ' ' + linkingOperations[2] + ' ' + str(linkingNums[2]) + ' = ' + str(cells[2][9]) + '       ' + str(cells[2][3]))
    print('=' + '       ' + '=' + '       ' + '=' + '       ' + '=')
    print(str(cells[3][8]) + '       ' + str(cells[3][4]) + '       ' + str(cells[2][8]) + '       ' + str(cells[2][4]))
    print(str(cells[3][7]) + ' ' + globalOperations[3][2] + ' ' + str(cells[3][6]) + ' = ' + str(cells[3][5]) + '       ' + str(cells[2][7]) + ' ' + globalOperations[2][2]+ ' ' + str(cells[2][6]) + ' = ' + str(cells[2][5]))
   
    return

def CheckSafe(index, num, grid, operations):#TODO complete this method
    currentCell = 0
    candidates = []
    for i in range(index) : #Get current cell
        if i % 11 == 0 : 
            currentCell += 1
    
    if index % 11 == 0 : #Check upper left corner cell
        if num == 0 : 
            return False

        if grid[1 + currentCell * 11] != -1 :
            if operations[0 + currentCell * 5] == '-' : 
                if num < grid[1 + currentCell * 11] : 
                    return False
            elif operations[0 + currentCell * 5] == '+' :
                if num > 9 - grid[1 + currentCell * 11] :
                    return False
            elif operations[0 + currentCell * 5] == '*' :
                if num * grid[1 + currentCell * 11] > 9 :
                    return False

        if grid[2 + currentCell * 11] != -1 : 
            if grid[1 + currentCell * 11] != -1 :
                if ops[operations[0 + currentCell * 5]](num, grid[1 + currentCell * 11]) != grid[2 + currentCell * 11] : 
                    return False
            else : 
                if operations[0 + currentCell * 5] == '-' : 
                    if num < grid[2 + currentCell * 11] : 
                        return False
                elif operations[0 + currentCell * 5] == '+' :
                    if num > grid[2 + currentCell * 11] :
                        return False
                elif operations[0 + currentCell * 5] == '*' :
                    temp = num / grid[2 + currentCell * 11]
                    if isinstance(temp, int) == False:
                        return False

    return True

def CheckFullGrid(grid) : 
    for i in range(len(grid)) : 
        if grid[i] ==  -1 : 
            return False
    return True

counter = 0
def Solver(grid, operations) : 
    global counter
    for i in range(len(grid)) :
        if grid[i] == -1 : 
            nums = [0,1,2,3,4,5,6,7,8,9]
            for num in nums : 
                if CheckSafe(i, num, grid, operations) : #TODO create check safe method (hard part)
                    grid[i] = num
                    if CheckFullGrid() : 
                        counter +=1
                        break
                    else : 
                        if(Solver(grid, operations)) : 
                            return True      
            break
    grid[i] = -1





# Generate first 2 cells
GenerateCell()
GenerateCell()
while CheckMatching(cells[0][3],cells[1][9]) == False : 
    del cells[-1]
    del globalOperations[-1]
    GenerateCell()

GenerateCell()
while CheckMatching(cells[1][6],cells[2][1]) == False : 
    del cells[-1]
    del globalOperations[-1]
    GenerateCell()

GenerateCell()
while CheckMatching(cells[3][3],cells[2][9]) == False or CheckMatching(cells[0][6], cells[3][1]) == False : 
    del cells[-1]
    del globalOperations[-1]
    GenerateCell()

PrintGaram()

for i in range(len(cells)) : 
    for j in range(len(cells[i])) : 
        grid.append(cells[i][j])
    grid.append(linkingNums[i])

for i in range(len(globalOperations)) : 
    for j in range(len(globalOperations[i])) : 
        operations.append(globalOperations[i][j])
    operations.append(linkingOperations[i])

cells.clear()
globalOperations.clear()
linkingNums.clear()
linkingOperations.clear()