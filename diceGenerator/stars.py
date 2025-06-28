
for a in range(7):
    for b in range(7):
        for c in range(7):
            for d in range(7):
                for e in range(7):
                    for f in range(7):
                        if(a+b+c+d+e+f == 6):
                            faces = ""
                            for aPrint in range(a):
                                faces += "1 "
                            for aPrint in range(b):
                                faces += "2 "
                            for aPrint in range(c):
                                faces += "3 "
                            for aPrint in range(d):
                                faces += "4 "
                            for aPrint in range(e):
                                faces += "5 "
                            for aPrint in range(f):
                                faces += "6 "
                            print (faces)