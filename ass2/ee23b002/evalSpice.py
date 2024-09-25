from collections import defaultdict
import numpy


def parseCircuit(filename: str) -> dict[list]:
    """
    Function takes in the file, parses the circuit
    and creates a dictionary of the circuit elements.

    returns a dict circuit_graph containing, each node as a distinct
    key and value a tuple of the format(destinationNode, component)
    where the component is the component between the two nodes in the
    spice netlist format.
    """
    circuit_graph = defaultdict(list)

    # open the file, populating circuit_graph
    try:
        inputFile = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(
            "Please give the name of a valid SPICE file as input"
        ) from None

    with inputFile:
        data = inputFile.read()
        if (".circuit" not in data) or (".end" not in data):
            raise ValueError("Malformed circuit file")
        # taking the portion between .circuit and .end
        data = data.split(".circuit")[-1]
        data = data.split(".end")[0].strip()
        lines = data.split("\n")
        for line in lines:
            if len(line.split()) == 0:
                continue  # ignoring empty lines
            if line.strip().split()[0][0] == "#":  # checking for comments
                continue

            # collecting nodes and components/
            lineVals = line.split()
            node1 = lineVals[1]
            node2 = lineVals[2]

            # checking if lineVals is valid:
            if lineVals[0][0] == "V" or lineVals[0][0] == "I":
                if len(lineVals) != 5:
                    try:
                        if lineVals[5][0] == "#":
                            pass
                        else:
                            raise ValueError("Invalid component in input file")
                    except:
                        raise ValueError("Invalid component in input file") from None
            else:
                if len(lineVals) != 4:
                    try:
                        if lineVals[4][0] == "#":
                            pass
                        else:
                            raise ValueError("Invalid component in input file")
                    except:
                        raise ValueError("Invalid component in input file") from None

            circuit_graph[node1].append((node2, lineVals))
            circuit_graph[node2].append((node1, lineVals))

    return circuit_graph


def genEquations(circuit_graph: dict) -> tuple[numpy.array, numpy.array, dict, list]:
    """
    function takes in the circuit_graph dictionary generated from the
    parseCircuit function,

    generates a system of linear equations using Nodal Analysis, and returns
    - A `coeff_matrix` which is a numpy array, which stores the coefficients of the system of linear equations.
    - A `const_matrix` which stores the constants in the system of linear equations.
    - A `nodeList` which is a list of nodes in the circuit
    - A `vsourceList` which is a dictionary containing voltage sources, where keys are the
    voltage sources and value is the metadata of the voltage sources themselves.

    """
    nodeNum = len(circuit_graph) - 1  # number of nodes without the GND node
    numEqns = nodeNum
    coeff_matrix = numpy.zeros((numEqns, numEqns))
    const_matrix = numpy.zeros((numEqns, 1))
    vsourceList = dict()

    nodeList = list()  # list storing nodes
    # populate nodelist
    for node in circuit_graph:
        if node == "GND":
            continue
        nodeList.append(node)
    # testing if GND is there

    if "GND" not in circuit_graph:
        raise ValueError("No GND node given.")

    for node in circuit_graph:
        if node == "GND":
            continue
        # iterating through each edge i
        for destNode, component in circuit_graph[node]:
            componentType = component[0][0]
            if componentType == "V":
                # check if it is in our vsourcelist
                if component[0] not in vsourceList:
                    vsourceMetadata = {
                        "index": len(vsourceList),
                        "node1": component[1],
                        "node2": component[2],
                        "type": component[3],
                        "value": component[4],
                    }
                    vsourceList[component[0]] = vsourceMetadata
                    # aupdate the matrices, and add values in the node
                    coeff_matrix = numpy.pad(
                        coeff_matrix,
                        pad_width=(0, 1),
                        mode="constant",
                        constant_values=0,
                    )
                    const_matrix = numpy.append(
                        const_matrix, numpy.zeros((1, 1)), axis=0
                    )
                # checking the polarity of the node
                # component[1] is where the positive terminal is connected
                if component[1] == node:
                    coeff_matrix[nodeList.index(node)][
                        nodeNum + vsourceList[component[0]]["index"]
                    ] += 1
                else:
                    coeff_matrix[nodeList.index(node)][
                        nodeNum + vsourceList[component[0]]["index"]
                    ] -= 1
            elif componentType == "R":
                try:
                    # adding 1/R in the current node and -1/R in the dest node in the matrix.
                    if float(component[3]) < 0:
                        raise ValueError
                    if destNode == "GND":
                        coeff_matrix[nodeList.index(node)][
                            nodeList.index(node)
                        ] += 1 / float(component[3])
                    else:
                        coeff_matrix[nodeList.index(node)][
                            nodeList.index(node)
                        ] += 1 / float(component[3])
                        coeff_matrix[nodeList.index(node)][
                            nodeList.index(destNode)
                        ] -= 1 / float(component[3])
                except:
                    raise ValueError("Invalid Resistance") from None

            elif componentType == "I":
                # add the values in the coefficient matrix
                if component[1] == component[2]:
                    pass
                elif component[1] == node:
                    const_matrix[nodeList.index(node)] = -float(component[4])
                else:
                    const_matrix[nodeList.index(node)] = float(component[4])
            else:
                raise ValueError("Only V, I, R elements are permitted")

    for vsource in vsourceList:
        vsource = vsourceList[vsource]
        # checking if any node is GND, else adding coefficeint in coefficient matrix
        if vsource["node1"] != "GND":
            coeff_matrix[nodeNum + vsource["index"]][
                nodeList.index(vsource["node1"])
            ] += 1

        if vsource["node2"] != "GND":
            coeff_matrix[nodeNum + vsource["index"]][
                nodeList.index(vsource["node2"])
            ] -= 1
        # adding Voltage value in the constant matrix
        const_matrix[nodeNum + vsource["index"]] = vsource["value"]
    return coeff_matrix, const_matrix, vsourceList, nodeList


def evalSpice(filename: str):
    circuit_graph = parseCircuit(filename)
    coeffMatrix, constMatrix, vsourceList, nodeList = genEquations(circuit_graph)

    try:
        solution = numpy.linalg.solve(coeffMatrix, constMatrix)
    except:
        raise ValueError("Circuit error: no solution") from None
    V = dict()
    # constructing dictionary for node voltages
    for index, node in enumerate(nodeList):
        V[node] = solution[index][0]

    I = dict()

    # constructing dictionary for current through voltage sources.
    for vsource in vsourceList:
        I[vsource] = solution[vsourceList[vsource]["index"] + len(nodeList)][0]

    V["GND"] = 0
    return V, I
