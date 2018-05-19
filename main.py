import subprocess, time, os, sys


def get_inputs():
    #for testing to make things easier
    if (len(sys.argv)) == 4:
        x = sys.argv[1]
        y= sys.argv[2]
        z = sys.argv[3]
        return int(x), int(y), int(z)
    x = input("X? ")
    y = input("Y? ")
    z = input("Z? ")
    return int(x), int(y), int(z)


def initial_setup():
    print("Minimize \n r \nSubject to")



def calc_demand_volumes(x, y, z):
    toPrint = ""
    for i in range(1, x+1):
        for j in range(1, z+1):
            h = i + j
            for k in range(1, y+1):

                if k == 1:
                    toPrint += "DemandVolume{0}{1}: x{0}{2}{1}".format(i, j, k)
                else:
                    toPrint += " + x{0}{2}{1}".format(i, j, k)
            toPrint += " = {}\n".format(h)
    print(toPrint)


def calc_demand_flow(x, y, z, paths=3):
    for i in range(1, x + 1):
        for j in range(1, z + 1):
            for k in range(1, y + 1):
                l = "{}{}{}".format(i, k, j)
                print(" demandflow{}: {} x{} - {} u{} = 0".format(l, paths, l, i + j, l))

def calc_bounds(x, y, z):
    print("Bounds")
    for i in range(1, x + 1):
        for j in range(1, z + 1):
            for k in range(1, y + 1):
                l = str(i) + str(j) + str(k)
                print(" x{} >= 0".format(l, l))
    for i in range(1, x + 1):
        for k in range(1, y + 1):
            print(" c{2}{3} >= 0".format(i, k, i, k))
    for j in range(1, z + 1):
        for k in range(1, y + 1):
            print(" d{2}{3} >= 0".format(k, j, k, j))
    print(" r >= 0")


def calc_binaries(x, y, z):
    for i in range(1, x + 1):
        for k in range(1, y + 1):
            for j in range(1, z + 1):
                print(" u{0}{1}{2}".format(i, k, j))




def executeCPLEX(tmLocation):
    statement = CPLEX_BIN_PATH + 'cplex -c "read ' + tmLocation + '" "optimize" "display solution variables -"'
    process = subprocess.run(statement, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout


def extractSolution(variable, cplexReturn, hValue):
    for line in cplexReturn.split("\n"):
        if line.startswith(variable):
            solution = line.split()
            solution.append(hValue)
            print(solution)
            # TODO log solutions -> graph? hah

def wahtDo():
    for h in range(1, 19, 1):
        fileString = "Minimize\n 10 x12 + 5 x x132\n Subject to\n demandflow: x12 + x132 =" + str(h)
        fileString += "\n capp1: x12 <= 10\n capp2: x132 <= 10\nBounds\n 0 <= x12\n 0 <= x132\nEnd"
        f = open("tm.lp", "w+")
        f.write(fileString)
        fileToUse = open("tm.lp", "r")
        f.close()

        returnValue = executeCPLEX(DIR_PATH + "/tm.lp")
        extractSolution("x12", returnValue, h)
        extractSolution("x132", returnValue, h)

def main():
    x, y, z = get_inputs()
    initial_setup()
    calc_demand_volumes(x, y, z)
    calc_demand_flow(x, y, z)
    calc_bounds(x, y, z)
    calc_binaries(x, y, z)
main()
