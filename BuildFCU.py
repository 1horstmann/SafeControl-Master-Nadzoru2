import DiagnoserFunctions

FUa = []
FUn = []
FCs = []
FS = []
FUx = []
FUax = []
FUn = []

def Step1(FUn):
    FS = []

    for each in FUn:
        forwards = DiagnoserFunctions.GetNextStatesInID(str(each))
        for cada in forwards:
            FS.append(str(cada))
    return(FS)

def ClearFUn():
    FUn = []
    return(FUn)

def Build(state):
    aux = []
    aux.append(state)
    for cada in aux:
        FS = Step1(state)
        aux = []
        for each in FS:
            eachname = DiagnoserFunctions.GetNextStatesInNames(str(each))
            if DiagnoserFunctions.IsNormal(eachname) == True:
                if DiagnoserFunctions.IsOnlySelfloop(each) == 0:
                    x = Step1(each)
                    for cada in x:
                        FS.append(str(cada))
            elif DiagnoserFunctions.IsCertain(eachname) == True:
                FCs.append(str(each))
            elif DiagnoserFunctions.IsUncertain(eachname) == True:
                FUax.append(str(each))

def GetFUa():
    return(FUax)

def GetFCs():
    return(FCs)

def GetFUn():
    return(FUx)