import DiagnoserParser
import DiagnoserFunctions

def GetFU():
    x = 0
    # to_observe = []
    uf = []
    while x < len(DiagnoserParser.State_Name_Table):
        a = DiagnoserFunctions.GetTodoTable(x)
        uncertain_counter = 0
        comp = 0
        for each in a:
            comp = len(a)
            if DiagnoserFunctions.IsUncertain(each) == True:
                uf.append(each)
                uncertain_counter = uncertain_counter + 1
                #        to_observe.append(each)
        if (comp == uncertain_counter):
            x = len(DiagnoserParser.State_Name_Table)
        x = x + 1
    return (uf)


def GetFUID(table):
    FU_id = []
    for each in table:
        for n in range(0,len(DiagnoserParser.State_Id_Table)):
            a = DiagnoserParser.State_Name_Table[n]
            if a == str(each):
                FU_id.append(DiagnoserParser.State_Id_Table[n])
    return(FU_id)
