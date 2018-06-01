import sys
import subprocess
from datetime import datetime

FILE_TO_WRITE = "assignment2.lp"

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


def initial_statements():
    return "Minimize \n p \nSubject to\n"


def calc_demand_volumes(x, y, z):
    toReturn = ""
    for i in range(1, x+1):
        for j in range(1, z+1):
            h = i + j
            for k in range(1, y+1):
                if k == 1:
                    toReturn += "DemandVolume{0}{1}: x{0}{2}{1}".format(i, j, k)
                else:
                    toReturn += " + x{0}{2}{1}".format(i, j, k)
            toReturn += " = {}\n".format(h)

    return toReturn


def calc_demand_flow(x, y, z, num_paths=3):
    toReturn = ""
    for i in range(1, x + 1):
        for k in range(1, z + 1):
            for j in range(1, y + 1):
                path = "{0}{1}{2}".format(i, k, j)
                toReturn += "DemandFlow{0}: {1} x{0} - {2} u{0} = 0\n".format(path, num_paths, i + j)

    return toReturn

def calc_source_node_constraints(x, y, z):
    toReturn = ""
    for i in range(1, x+1):
        for j in range(1, y+1):
            for k in range(1, z+1):
                if k == 1:
                    toReturn += ("SrcConstraints: x{}{}{}".format(i, j, k))
                elif k < z:
                    toReturn += (" + x{}{}{}".format(i, j, k))
                else:
                    toReturn += (" + x{}{}{} - c{}{} = 0\n".format(i, j, k, i, j))
    return toReturn

def calc_dest_node_constraints(x, y, z):
    toReturn = ""
    for i in range(1, z + 1):
        for j in range(1, y + 1):
            for k in range(1, x + 1):
                if k == 1:
                    toReturn += ("DstConstraints: x{}{}{}".format(k, j, i))
                elif k < z:
                    toReturn += (" + x{}{}{}".format(k, j, i))
                else:
                    toReturn += (" + x{}{}{} - d{}{} = 0\n".format(k, j, i, j, i))
    return toReturn

def calc_trans_node_constraints(x, y, z):
    toReturn = ""
    for i in range(1, y+1):
        for j in range(1, x+1):
            for k in range(1, z+1):
                if j == 1 and k == 1:
                    toReturn += "TransConstraints: x{}{}{}".format(j, i, k)
                elif j == x and k == z:
                    toReturn += " + x{}{}{} - p <= 0\n".format(j, i, k)
                else:
                    toReturn += " + x{}{}{}".format(j, i, k)
    return toReturn


def calc_utilisation_constraints(x, y, z, num_paths=3):
    """Calculates the Utilisation Constraints for each of the transit nodes"""
    toReturn = ""
    for i in range(1, x+1):
        for j in range(1, z+1):
            for k in range(1, y+1):
                if k == 1:
                    toReturn += "Utilisation: u{}{}{}".format(i, k, j)
                elif k == y:
                    toReturn += " + u{}{}{} = {}\n".format(i, k, j, 3)
                else:
                    toReturn += " + u{}{}{}".format(i, k, j)
    return toReturn

def calc_bounds(x, y, z):
    toReturn = "Bounds\n"
    for i in range(1, x + 1):
        for j in range(1, y + 1):
            for k in range(1, z + 1):
                l = str(i) + str(j) + str(k)
                toReturn += " x{} >= 0\n".format(l, l)
    for i in range(1, x + 1):
        for k in range(1, y + 1):
            toReturn += " c{2}{3} >= 0\n".format(i, k, i, k)
    for j in range(1, z + 1):
        for k in range(1, y + 1):
            toReturn += " d{2}{3} >= 0\n".format(k, j, k, j)
    toReturn += " p >= 0\n"
    return toReturn


def calc_binaries(x, y, z):
    toReturn = "Binaries\n"
    for i in range(1, x + 1):
        for k in range(1, y + 1):
            for j in range(1, z + 1):
                toReturn += " u{0}{1}{2}\n".format(i, k, j)
    return toReturn


def create_lp_file(fileToWrite, text):
    file = open(fileToWrite, "w")
    file.write(text)
    file.close()


def run_cplex(lp_filename):
    """"Builds and runs CPLEX with the .lp file created"""

    cplex_command = "/home/cosc/student/sbo49/COSC364/cplex/bin/x86-64_linux/cplex" #GET CORRECT
    args = [
        "-c",
        "read /home/cosc/student/sbo49/COSC364/cosc364trafficplanning/" + lp_filename,
        "optimize",
        'display solution variables -'
    ]

    process = subprocess.Popen([cplex_command] + args, stdout=subprocess.PIPE)
    out, err = process.communicate()
    result = out.decode("utf-8")

    return result


def main():

    x, y, z = get_inputs()
    lp_text = ""
    lp_text += initial_statements()
    lp_text += calc_demand_volumes(x, y, z)
    lp_text += calc_demand_flow(x, y, z)
    lp_text += calc_source_node_constraints(z, y, z)
    lp_text += calc_dest_node_constraints(x, y, z)
    lp_text += calc_trans_node_constraints(x, y, z)
    lp_text += calc_utilisation_constraints(x, y, z)
    lp_text += calc_bounds(x, y, z)
    lp_text += calc_binaries(x, y, z)
    lp_text += "END"
    create_lp_file(FILE_TO_WRITE, lp_text)
    #Start Timer, then run cplex, and get time taken at the end
    start_time = datetime.now()
    result = run_cplex(FILE_TO_WRITE)
    time_to_run = datetime.now() - start_time
    print("\n\nTime to run =", time_to_run)
    #print(result)


if __name__ == "__main__":
    main()
