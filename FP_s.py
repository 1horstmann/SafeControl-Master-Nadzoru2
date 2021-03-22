import FU_s
import PathManager
import DiagnoserFunctions
import DefineStrings

UP = []

def GetFP_s():
    strings = FU_s.GetStringPath()

    Strings = []
    for k in strings:
        for n in k:
            Strings.append(n)

    Fault_Diag_EventStrings_IDs = list()
    for i in range (len(Strings)):
        f_strings = list()
        for each in Strings[i]:
            f_strings.append(DiagnoserFunctions.GetEquivalentDiagEventFromAut(each))
        Fault_Diag_EventStrings_IDs.append(f_strings)

    # print(f'Fault_Diag_EventStrings_IDs = {Fault_Diag_EventStrings_IDs}')
    cadeias = DefineStrings.GetDiagStates(Fault_Diag_EventStrings_IDs)
    # print(f'cadeias = {cadeias}')



    lista_fp = []
    for each in cadeias:
        FP = False
        last = each[-1]

        if not PathManager.ConditionCHolds(last, antes_fu=True):
            lista_fp.append('')
        else:
            target_id_last = DiagnoserFunctions.GetNextStatesInID(last)

            if FP:
                lista_fp.append(fp)
            else:
                j = 0
                for i in range(len(each), 0, -1):
                    if i-2 < 0:
                        break
                    else:
                        if j == 0 and not PathManager.ConditionCHolds(each[i-2], antes_fu=True):
                            fp = each[i-1]
                        if PathManager.ConditionCHolds(each[i-2], antes_fu=True):
                            fp = each[i-2]
                        else: 
                            break
                    j += 0
                lista_fp.append(fp)

    nomes_lista_fp = []
    for each in lista_fp:
        nomes_lista_fp.append(DiagnoserFunctions.GetNextStatesInNames(each))

    return nomes_lista_fp

# print(f'GetFP_s = {GetFP_s()}')


def GetUP(FU_Pos):
    GetFP_s(FU_Pos)
    return (UP)
