import DiagnoserFunctions
import DefineStrings

def AnalyseStatePath(state): 
    answer = []
    NextStateIds = DiagnoserFunctions.GetNextStatesInID(state)
    status = False

    while status != True:
        for each in NextStateIds:
            NextStateNames = str(DiagnoserFunctions.GetNextStatesInNames(str(each)))

            if DiagnoserFunctions.IsCertain(NextStateNames) == True:
                status = True
                answer.append(1)
            else:
                if DiagnoserFunctions.IsOnlySelfloop(each) == 1:
                    status = True
                    answer.append(0)
                else:
                    state_id = DiagnoserFunctions.GetNextStatesInID(each)
                    for cada in state_id:
                        if NextStateIds.__contains__(cada) == False:
                            NextStateIds.append(cada)

            if answer.__contains__(0) == True:
                resposta_final = 0
            else:
                resposta_final = 1

    return(resposta_final)


def ConditionCHolds(state_ID, antes_fu=False):  # returns True if C condition holds
    Reachable = [] 
    Reachable.append(DefineStrings.GetDiagReachable(state_ID)) 
    
    test_normal = DefineStrings.IsNormalCycle(Reachable) 
    test_uncertain = DefineStrings.IsUncertainCycle(Reachable, antes_fu) 

    C_Condition = True 
    if test_normal[0] or test_uncertain[0]:
        C_Condition = False
    
    return C_Condition 
