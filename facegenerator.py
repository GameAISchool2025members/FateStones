import sys

def printDice(filepath):
    with open(filepath) as facesFile:
        for line in facesFile:
            filename = line.strip().replace(" ", "")
            faceValues = line.split(' ')
            stl = printDie(faceValues)
            with open("generated/"+filename+".stl", "w") as stlfile:
                stlfile.write(stl)

def printDie(faceValues):
    folders = ["afaces","bfaces","bottomfaces","cfaces","dfaces","topfaces"]
    out = "solid Cheetah3Dfile\n"
    faceIndex = 0
    for face in folders:
        pips = faceValues[faceIndex]
        with open(face+"/"+pips+".stl") as faceFile:
            for line in faceFile:
                if "solid" not in line:
                    out += line
        faceIndex = faceIndex + 1
    out += "endsolid"
    return out

if(len(sys.argv) == 7):
    print(printDie(sys.argv[1:]))
elif(len(sys.argv) == 2):
    printDice(sys.argv[1])