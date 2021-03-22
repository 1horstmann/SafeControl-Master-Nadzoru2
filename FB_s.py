import AutomataParser
import DiagnoserParser
import AutomataFunctions
import DiagnoserFunctions
import DefineStrings
import FU_s
import FC_s


def GetFB_s_IDs(string):  # gets the FB(s) for a given string number

    FU_s_StateNames = FU_s.Get_FU_s()  

    # for this string only, getting the FU(s):
    FU_s_StateIDs = []  
    FU_s_StateIDs.append(DiagnoserFunctions.GetStateId(FU_s_StateNames[string]))  

    # and getting the reachable states for this string in ID
    string_states_IDs = DefineStrings.GetDiagReachable(FU_s_StateIDs[0])  

    # getting the names
    string_states_names = []  
    for each in string_states_IDs:  
        string_states_names.append(DiagnoserFunctions.GetStateName(each))  

    # ignoring the non-bad ones
    the_bad_IDs = []  
    i = 0  
    while i < len(string_states_names):  
        if not DiagnoserFunctions.IsNotBad(string_states_names[i]):  
            the_bad_IDs.append(string_states_IDs[i])  
        i += 1  

    # and verifying if they lead to each other to ignore the target ones (once they're not the first ones)
    is_first = []  
    for each in the_bad_IDs:  
        i = 0  
        first = True  
        while i < len(DiagnoserParser.Transition_Target_Table): 
            if (each == DiagnoserParser.Transition_Target_Table[i]  
                    and DiagnoserParser.Transition_Source_Table[i] != each  
                    and DiagnoserParser.Transition_Source_Table[i] in the_bad_IDs):  
                first = False  
            i += 1  
        is_first.append(first)  

    almost = []  
    i = 0  
    while i < len(the_bad_IDs):  
        if is_first[i]: 
            almost.append(the_bad_IDs[i])  
        i += 1  

    FC_s_StateIDs = []  
    FC_s_StateIDs.append(FC_s.GetFC_s_IDs(string))  

    FB_s = []
    i = 0
    while i < len(FC_s_StateIDs):
        j = 0
        while j < len(FC_s_StateIDs[i]):
            reachable_fc = DefineStrings.GetDiagReachable(FC_s_StateIDs[i][j])
            for each in almost:
                if each in reachable_fc:
                    FB_s.append(each)
            j += 1
        i += 1

    return FB_s  