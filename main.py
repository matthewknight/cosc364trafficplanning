import subprocess, time, os, sys

CPLEX_BIN_PATH = "/opt/ibm/ILOG/CPLEX_Studio_Community128/cplex/bin/x86-64_linux/"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

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