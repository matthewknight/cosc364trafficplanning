import sys
import subprocess
from datetime import datetime


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
    print("Minimize \n p \nSubject to")


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


def calc_demand_flow(x, y, z, num_paths=3):
    for i in range(1, x + 1):
        for k in range(1, z + 1):
            for j in range(1, y + 1):
                path = "{0}{1}{2}".format(i, k, j)
                print("DemandFlow{0}: {1} x{0} - {2} u{0} = 0".format(path, num_paths, i + j))

#TODO
def calc_source_node_constraints(x, y, z, num_paths=3):
    pass

def calc_dest_node_constraints(x, y, z, num_paths=3):
    pass

def calc_trans_node_constraints(x, y, z, num_paths=3):
    pass


def calc_utilisation_constraints(x, y, z, num_paths=3):
    """Calculates the Utilisation Constraints for each of the transit nodes"""
    print("Utilisation")
    for i in range(1, x+1):
        for j in range(1, z+1):
            for k in range(1, y+1):
                if k == 1:
                    print(" u{}{}{}".format(i, k, j), end="")
                elif k == y:
                    print("+u{}{}{} = {}".format(i, k, j, 3))
                else:
                    print("+u{}{}{}".format(i, k, j), end="")

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
    print(" p >= 0")


def calc_binaries(x, y, z):
    print("Binaries")
    for i in range(1, x + 1):
        for k in range(1, y + 1):
            for j in range(1, z + 1):
                print(" u{0}{1}{2}".format(i, k, j))


def create_lp_file():

    return 0

def run_cplex(filename):
    """"Script for building and running Cplex based on .lp file input"""

    command = "/home/cosc/student/sbo49/cplex/cplex/bin/x86-64_linux/cplex" #GET CORRECT
    args = [
        "-c",
        "read /home/cosc/student/sbo49/cosc364/cosc364assignment/" + filename,
        "optimize",
        'display solution variables -'
    ]

    process = subprocess.Popen([command] + args, stdout=subprocess.PIPE)
    out, err = process.communicate()
    result = out.decode("utf-8")

    return result



def main():
    x, y, z = get_inputs()
    initial_setup()
    calc_demand_volumes(x, y, z)
    calc_demand_flow(x, y, z)
    calc_utilisation_constraints(x, y, z)
    calc_bounds(x, y, z)
    calc_binaries(x, y, z)
    filename = create_lp_file()

    #Start Timer, then run cplex, and get time taken at the end
    start_time = datetime.now()
    #result = run_cplex(filename)
    time_to_run = datetime.now() - start_time
    print("Time to run =", time_to_run)
main()
