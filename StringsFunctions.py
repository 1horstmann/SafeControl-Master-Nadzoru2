import DefineStrings
import DiagnoserFunctions
import AutomataFunctions
import FU_s
import FC_s
import FB_s
import FP_s


def ConsideredStrings_Publish():
    """Get all the strings considered by the algorithm
    """
    strings = FU_s.GetStringPath()

    Strings = []
    for k in strings:
        for n in k:
            Strings.append(n)

    sum = 0
    while sum < len(Strings):
        sum += 1
    print('\n* Serão consideradas', sum, 'cadeias até a falha:\n')  
    Sum = 0
    
    i = 0  
    while i < len(Strings):  
        state_name = []  
        for cada in Strings[i]:  
            state_name.append(AutomataFunctions.GetEventName(cada))  
        state_name.append(AutomataFunctions.GetFaultEventName())  
        Sum += 1
        print(f'cadeia {Sum} = {state_name}')
        state_name.clear()
        i += 1 


def IsDiag():  # returns True if automata is diagnosable, and False if it's not
    """[Check if automata is diagonosable. If it is, return True, else, return False]
    """

    # # getting the event sequence to the fault
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

    # getting these events names
    Fault_Aut_Strings_Names = []
    i = 0
    while i < len(Fault_Diag_EventStrings_IDs):
        state_name = []
        for each in Fault_Diag_EventStrings_IDs[i]:
            state_name.append(DiagnoserFunctions.GetEventName(each))
        state_name.append(AutomataFunctions.GetFaultEventName())
        Fault_Aut_Strings_Names.append(state_name)
        i += 1


    # getting the states to the fail by the ID
    Diag_Fault_StateString_IDs = DefineStrings.GetDiagStates(Fault_Diag_EventStrings_IDs)
    # add next states of the string if they're uncertain
    Diag_Uncertain_StateString_IDs = DefineStrings.IsNextStateUncertain(Diag_Fault_StateString_IDs)

    test = DefineStrings.IsUncertainCycle(Diag_Uncertain_StateString_IDs, antes_fu=False)

    if not test[0]:
        IsDiagnosable = True
    else:
        IsDiagnosable = False

    return IsDiagnosable


def IsDiag_Publish():  # returns True if automata is diagnosable, and False if it's not
    """[Check if automata is diagonosable. Return if each string is diagonosable]
    """
    
    print('\n\n* DIAGNOSTICABILIDADE\n')

    # # getting the event sequence to the fault
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

    # getting these events names
    Fault_Aut_Strings_Names = []
    i = 0
    while i < len(Fault_Diag_EventStrings_IDs):
        state_name = []
        for each in Fault_Diag_EventStrings_IDs[i]:
            state_name.append(DiagnoserFunctions.GetEventName(each))
        state_name.append(AutomataFunctions.GetFaultEventName())
        Fault_Aut_Strings_Names.append(state_name)
        i += 1

    # getting the states to the fail by the ID
    Diag_Fault_StateString_IDs = DefineStrings.GetDiagStates(Fault_Diag_EventStrings_IDs)
    # add next states of the string if they're uncertain
    Diag_Uncertain_StateString_IDs = DefineStrings.IsNextStateUncertain(Diag_Fault_StateString_IDs)
    # get the names for the state string
    Diag_Uncertain_StateString_Names = DefineStrings.DiagIDtoName(Diag_Fault_StateString_IDs)

    test = DefineStrings.IsUncertainCycle(Diag_Uncertain_StateString_IDs, antes_fu=False)

    IsDiagnosable = True
    for i in range(len(Diag_Uncertain_StateString_IDs)):
        incerto = False
        for k in test[1]:
            if k in Diag_Uncertain_StateString_IDs[i]:
                print('A cadeia', i + 1, 'possui um ciclo indeterminado em [', DiagnoserFunctions.GetStateName(k),
                '] e, portanto, não é diagnosticável.')
                incerto = True
                IsDiagnosable = False
                break
        if not incerto:
            print('A cadeia', i + 1, 'não possui ciclo indeterminado e, portanto, é diagnosticável.')


    if IsDiagnosable == True:
        print('\nA linguagem é diagnosticável.')
    else:
        print('\nA linguagem não é diagnosticável.')

    return IsDiagnosable


def IsSafeDiag():
    """[Check if the automata is safe diagnosable. If it is, return True, else, return False]
    """
    # if it is Language Diagnosable:
    if IsDiag():
        strings = FU_s.GetStringPath()
        
        # run one time for each string
        FC_s_IDs = []
        string_num = 0
        j = 0
        len_strings = 0
        while j < len(strings):
            for cada in strings[j]:
                len_strings += 1
            j += 1
        
        while string_num < len_strings:
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = []
        i = 0
        while i < len(FC_s_IDs):
            names = []
            for each in FC_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names)
            i += 1

       # getting the bad states
        Bad_State = [] 
        i = 0 
        while i < len(FC_s_Names): 
            isbad = [] 
            for each in FC_s_Names[i]: 
                if DiagnoserFunctions.IsNotBad(each): 
                    isbad.append(False) 
                else: 
                    isbad.append(True) 
            Bad_State.append(isbad) 
            i += 1 

        i = 0 
        diag_seg = True 
        while i < len(strings): 
            if True in Bad_State[i]: 
                diag_seg = False 
            i += 1 
        return diag_seg 

    else:
        return False


def IsSafeDiag_Publish():
    """[Check if automata is diagonosable. Return if each string is safe diagonosable]
    """
    print('\n\n* DIAGNOSTICABILIDADE SEGURA\n')

    # if it is Language Diagnosable:
    if IsDiag():
        strings = FU_s.GetStringPath()

        # run one time for each string
        FC_s_IDs = []
        string_num = 0
        j = 0
        len_strings = 0
        while j < len(strings):
            for cada in strings[j]:
                len_strings += 1
            j += 1
        
        while string_num < len_strings:
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = []
        i = 0
        while i < len(FC_s_IDs):
            names = []
            for each in FC_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names)
            i += 1


        # getting the bad states for each string
        Bad_State = []
        i = 0
        while i < len(FC_s_Names):
            isbad = []
            for each in FC_s_Names[i]:
                if DiagnoserFunctions.IsNotBad(each):
                    isbad.append(False)
                else:
                    isbad.append(True)
            Bad_State.append(isbad)
            i += 1

        print('Para cada cadeia da linguagem, calcula-se o FC(s)\n')
        i = 0 
        diag_seg = True 

        while i < len_strings:
            print('FC(', i + 1, ') =', FC_s_Names[i])
            if True in Bad_State[i]:
                j = Bad_State[i].index(True)
                print('O estado [', FC_s_Names[i][j], '] é um Bad State.',
                      'Portanto, a cadeia', i + 1, 'não é diagnosticável segura.\n')
                diag_seg = False
            else:
                print('A cadeia', i + 1, 'não possui Bad States no FC, portanto é diagnosticável segura.\n')
            i += 1

        if diag_seg:
            print('A linguagem é diagnosticável segura.')
        else:
            print('A linguagem não é diagnosticável segura.')

        return diag_seg

    # if it is not Language Diagnosable:
    else:
        print('A linguagem não é diagnosticável segura, pois não é diagnosticável em primeiro lugar.')
        return False


def IsPred():
    """[Check if automata is predictable. If it is, return True, else, return False]
    """

    IsPredictable = False

    # if it is Language Diagnosable:
    if IsDiag():

        # get reachable states from FU
        FU_states = FU_s.Get_FU_s()

        Reachable = []
        for each in FU_states:
            each_name = DiagnoserFunctions.GetStateId(each)
            Reachable.append(DefineStrings.GetDiagReachable(each_name))

        # getting the names
        i = 0
        Reachable_Names = []
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # test if there is any Normal or Uncertain Cycle (C condition)
        test_normal = DefineStrings.IsNormalCycle(Reachable)
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable, antes_fu=True)

        if not test_normal[0] and not test_uncertain[0]:
            IsPredictable = True

        return IsPredictable

    # if it is not Language Diagnosable:
    else:
        return IsPredictable


def IsPred_Publish():
    """[Check if automata is predictable. Return if each string is predictable]
    """
    print('\n\n* PROGNOSTICABILIDADE\n')

    # if it is Language Diagnosable:
    if IsDiag():

        # # publishing only
        # get reachable states from FU
        FU_states = FU_s.Get_FU_s()

        Reachable = []
        for each in FU_states:
            each_name = DiagnoserFunctions.GetStateId(each)
            Reachable.append(DefineStrings.GetDiagReachable(each_name))

        # getting the names
        i = 0
        Reachable_Names = []
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # test if there is any Normal or Uncertain Cycle (C condition)
        test_normal = DefineStrings.IsNormalCycle(Reachable)
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable, antes_fu=True)


        IsPredictable = True
        for i in range(len(Reachable)):
            normal = False
            incerto = False
            for k in test_normal[1]:
                if k in Reachable[i]:
                    print('A cadeia', i + 1, 'possui um ciclo normal em [', DiagnoserFunctions.GetStateName(k),'] e, portanto, não é prognosticável.\n')
                    normal = True
                    IsPredictable = False
                    break
            for k in test_uncertain[1]:
                if k in Reachable[i] and not normal:
                    print('A cadeia', i + 1, 'possui um ciclo incerto em [', DiagnoserFunctions.GetStateName(k),'] e, portanto, não é prognosticável.\n')
                    incerto = True
                    IsPredictable = False
                    break
            if not normal and not incerto:
                print('A cadeia', i + 1, 'não possui ciclo incerto ou normal e, portanto, é prognosticável.\n')

        if IsPredictable == True:
            print('A linguagem é prognosticável.')
        else:
            print('A linguagem não é prognosticável.')

        return IsPredictable

    # if it is not Language Diagnosable:
    else:
        print('\nA linguagem não é prognosticável, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiag():
    """[Check if automata is safe control by diagnosis. If it is, return True, else, return False]
    """
    # if it is Language Diagnosable:
    if IsDiag(): 
        strings = FU_s.GetStringPath() 

        # getting FC(s) IDs
        FC_s_IDs = []
        string_num = 0
        j = 0
        len_strings = 0
        while j < len(strings):
            for cada in strings[j]:
                len_strings += 1
            j += 1

        while string_num < len_strings:
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = [] 
        i = 0#atribuindo 0 a i
        while i < len(FC_s_IDs): 
            names = [] 
            for each in FC_s_IDs[i]: 
                names.append(DiagnoserFunctions.GetStateName(each)) 
            FC_s_Names.append(names) 
            i += 1 

        # getting the FB states
        FB_s_IDs = []
        string_num = 0
        j = 0
        len_strings = 0
        while j < len(strings):
            for cada in strings[j]:
                len_strings += 1
            j += 1

        while string_num < len_strings:
            FB_s_IDs.append(FB_s.GetFB_s_IDs(string_num))
            string_num += 1

        # getting FB(s) names
        FB_s_Names = [] 
        i = 0 
        while i < len(FB_s_IDs): 
            names = [] 
            for each in FB_s_IDs[i]: 
                names.append(DiagnoserFunctions.GetStateName(each)) 
            FB_s_Names.append(names) 
            i += 1 

        # * first condition is: FC can not be a bad state

        # searching for bad states in FC
        Bad_State = [] 
        i = 0 
        while i < len(FC_s_Names): 
            isbad = [] 
            for each in FC_s_Names[i]:
                if DiagnoserFunctions.IsNotBad(each): 
                    isbad.append(False) 
                else: 
                    isbad.append(True) 
            Bad_State.append(isbad) 
            i += 1 

        # * second condition is: sub-strings must have a controllable state between a FC and a FB

        # getting reachable for each FC
        Sub_Strings_IDs = [] 
        i = 0 
        while i < len(FC_s_IDs): 
            reachable = [] 
            for each in FC_s_IDs[i]: 
                reachable.append(DefineStrings.GetDiagReachable(each)) 
            Sub_Strings_IDs.append(reachable) 
            i += 1 

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = [] 
        i = 0 
        while i < len(Sub_Strings_IDs): 
            j = 0 
            bad_sub = [] 
            while j < len(Sub_Strings_IDs[i]):
                bad_subsub = [] 
                for each in Sub_Strings_IDs[i][j]: 
                    if each in FB_s_IDs[i]: 
                        bad_subsub.append(each) 
                bad_sub.append(bad_subsub) 
                j += 1 
            the_bads_IDs.append(bad_sub) 
            i += 1 

        i = 0 
        Controllability = [] 
        while i < len(FC_s_IDs): 
            j = 0 
            contr = [] 
            while j < len(FC_s_IDs[i]): 
                cont = [] 
                for each in the_bads_IDs[i][j]: 
                    cont.append(DefineStrings.AreAllWaysControllable(FC_s_IDs[i][j],each))
                j += 1 
                contr.append(cont) 
            i += 1 
            Controllability.append(contr) 

        final_strings =[]
        for each in strings:
            for j in each:
                final_strings.append(j)


        # testing both conditions:
        i = 0 
        Is_Controllable_By_Diagnosis = True
        Each_String_Diag_Controllable = [] 
        while i < len(final_strings): 
            Each_String = True 
            if True in Bad_State[i]: 
                j = Bad_State[i].index(True)
                Is_Controllable_By_Diagnosis = False
                Each_String = False
            if Each_String:
                w = 0
                while w < len(Controllability[i]):
                    if False in Controllability[i][w]:
                        Is_Controllable_By_Diagnosis = False
                        Each_String = False
                        break
                    w += 1
            Each_String_Diag_Controllable.append(Each_String)
            i += 1
        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        return False


def IsSafeControlByDiag_Publish():
    """[Check if automata is safe control by diagnosis. Return if each string is safe control by diagnosis]
    """
    print('\n\n* CONTROLABILIDADE SEGURA PELA DIAGNOSE\n')

    # if it is Language Diagnosable:
    if IsDiag():
        strings = FU_s.GetStringPath() 

        # getting FC(s) IDs
        FC_s_IDs = []
        string_num = 0
        j = 0
        len_strings = 0
        while j < len(strings):
            for cada in strings[j]:
                len_strings += 1
            j += 1

        while string_num < len_strings:
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = [] 
        i = 0 
        while i < len(FC_s_IDs): 
            names = [] 
            for each in FC_s_IDs[i]: 
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names) 
            i += 1 

        # getting the FB states
        FB_s_IDs = []
        string_num = 0
        j = 0
        len_strings = 0
        while j < len(strings):
            for cada in strings[j]:
                len_strings += 1
            j += 1

        while string_num < len_strings:
            FB_s_IDs.append(FB_s.GetFB_s_IDs(string_num))
            string_num += 1

        # getting FB(s) names
        FB_s_Names = [] 
        i = 0 
        while i < len(FB_s_IDs): 
            names = [] 
            for each in FB_s_IDs[i]: 
                names.append(DiagnoserFunctions.GetStateName(each)) 
            FB_s_Names.append(names) 
            i += 1 

        # * first condition is: FC can not be a bad state

        # searching for bad states in FC
        Bad_State = [] 
        i = 0
        while i < len(FC_s_Names): 
            isbad = [] 
            for each in FC_s_Names[i]: 
                if DiagnoserFunctions.IsNotBad(each): 
                    isbad.append(False) 
                else: 
                    isbad.append(True) 
            Bad_State.append(isbad) 
            i += 1 

        # * second condition is: sub-strings must have a controllable state between a FC and a FB

        # getting reachable for each FC
        Sub_Strings_IDs = [] 
        i = 0 
        while i < len(FC_s_IDs): 
            reachable = [] 
            for each in FC_s_IDs[i]: 
                reachable.append(DefineStrings.GetDiagReachable(each)) 
            Sub_Strings_IDs.append(reachable) 
            i += 1 

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = [] 
        i = 0 
        while i < len(Sub_Strings_IDs): 
            j = 0 
            bad_sub = [] 
            while j < len(Sub_Strings_IDs[i]): 
                bad_subsub = [] 
                for each in Sub_Strings_IDs[i][j]: 
                    if each in FB_s_IDs[i]: 
                        bad_subsub.append(each) 
                bad_sub.append(bad_subsub) 
                j += 1 
            the_bads_IDs.append(bad_sub) 
            i += 1 

        i = 0 
        Controllability = [] 
        while i < len(FC_s_IDs): 
            j = 0 
            contr = [] 
            while j < len(FC_s_IDs[i]): 
                cont = [] 
                for each in the_bads_IDs[i][j]: 
                    cont.append(DefineStrings.AreAllWaysControllable(FC_s_IDs[i][j],each)) 
                j += 1
                contr.append(cont)
            i += 1
            Controllability.append(contr)

        final_strings =[]
        for each in strings:
            for j in each:
                final_strings.append(j)

        # testing both conditions:
        i = 0 
        Is_Controllable_By_Diagnosis = True
        Each_String_Diag_Controllable = [] 
        while i < len(final_strings): 
            Each_String = True 
            print('Para a cadeia', i + 1, 'calcula-se o FC(s) e o FB(s)')
            print('FC(', i + 1, ') =', FC_s_Names[i])
            print('FB(', i + 1, ') =', FB_s_Names[i],'\n')
            if True in Bad_State[i]: 
                j = Bad_State[i].index(True)
                print('O estado', FC_s_Names[i][j], 'é um Bad State.',
                      '\nPortanto, a cadeia', i + 1, 'não é controlável segura pela diagnose.\n')
                Is_Controllable_By_Diagnosis = False
                Each_String = False
            if Each_String:
                w = 0
                while w < len(Controllability[i]):
                    if False in Controllability[i][w]:
                        print('No conjunto de eventos que ocorre entre o estado FC(', i + 1, ') = [', FC_s_Names[i][w], ']',
                              'e o estado FB(', i + 1, ') = [', FB_s_Names[i][w], '] não há um evento controlável',
                              '\nPortanto, a cadeia', i + 1, 'não é controlável segura pela diagnose.\n')
                        Is_Controllable_By_Diagnosis = False
                        Each_String = False
                        break
                    w += 1
            if Each_String:
                print('A cadeia', i + 1, 'não possui Bad States no FC. Além disso, sempre há um evento controlável',
                      'entre um estado FC(', i + 1, ') e um estado FB(', i + 1, ').',
                      '\nPortanto, a cadeia', i + 1, 'é controlável segura pela diagnose.\n')
            Each_String_Diag_Controllable.append(Each_String)
            i += 1  

        if Is_Controllable_By_Diagnosis:
            print('A linguagem é controlável segura pela diagnose.')
        else:
            print('A linguagem não é controlável segura pela diagnose.')

        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        print('\nA linguagem não é controlável segura pela diagnose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByProg():
    """[Check if automata is safe control by prognosis. If it is, return True, else, return False]
    """
    # if it is Language Diagnosable:
    if IsDiag():
        # * first condition is C condition

        # get reachable states from FU. Pegando todos os estados alcançaveis a partir dos Fu(s)
        FU_states = FU_s.Get_FU_s() #atribuindo a FU_states
        FU_states_ID = [] 
        for each in FU_states: 
            FU_states_ID.append(DiagnoserFunctions.GetStateId(each)) 

        Reachable = [] 
        for each in FU_states: 
            each_name = DiagnoserFunctions.GetStateId(each) 
            Reachable.append(DefineStrings.GetDiagReachable(each_name)) 

        # getting the names. Pegando o nomes dos estados alcançaveis a partir dos Fu(s)
        i = 0 
        Reachable_Names = [] 
        while i < len(Reachable): 
            names = [] 
            for each in Reachable[i]: 
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # test if there is any Normal or Uncertain Cycle (C condition).
        test_normal = DefineStrings.IsNormalCycle(Reachable)     
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable,antes_fu=True) 

        # * second condition is: sub-strings must have a controllable state between a FP and a FB

        # getting FP(s) names
        FP_s_Names = FP_s.GetFP_s()

        FP_s_IDs = [] 
        for each in FP_s_Names: 
            FP_s_IDs.append(DiagnoserFunctions.GetStateId(each)) 

        # getting the FB states
        i = 0 
        FB_s_IDs = [] 
        while i < len(FU_states): 
            FB_s_IDs.append(FB_s.GetFB_s_IDs(i)) 
            i += 1 

        # getting FB(s) names
        FB_s_Names = [] 
        i = 0 
        while i < len(FB_s_IDs): 
            names = []
            for each in FB_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FB_s_Names.append(names)
            i += 1 

        Sub_Strings_IDs = [] 
        for each in FP_s_IDs:
            Sub_Strings_IDs.append(DefineStrings.GetDiagReachable(each))

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = []
        i = 0 
        while i < len(Sub_Strings_IDs):
            bad_subsub = [] 
            for each in Sub_Strings_IDs[i]: 
                if each in FB_s_IDs[i]: 
                    bad_subsub.append(each) 
            the_bads_IDs.append(bad_subsub) 
            i+= 1 

        i = 0 
        control_FP_FB = [] 
        j = 0 
        while j < len(the_bads_IDs): 
            cont = [] 
            for each in the_bads_IDs[j]: 
                cont.append(DefineStrings.AreAllWaysControllable(FP_s_IDs[j], each)) 
            j += 1 
            control_FP_FB.append(cont) 

        # * testing both conditions:

        # calculating and printing the answers

        Is_Controllable_By_Prognosis = True
        Each_String_Diag_Controllable = []

        for i in range(len(FU_states)):
            Each_String = True

            if len(FP_s_Names[i]) == 0:
                Is_Controllable_By_Prognosis = False
                Each_String = False

            normal = False
            incerto = False
            for k in test_normal[1]:
                if k in Reachable[i] and not incerto and Each_String:
                    Is_Controllable_By_Prognosis = False
                    normal = True
                    break
            for k in test_uncertain[1]:
                if k in Reachable[i] and not normal and Each_String:
                    Is_Controllable_By_Prognosis = False
                    incerto = True
                    break

            if Each_String:
                if False in control_FP_FB[i]:
                    index = control_FP_FB[i].index(False)
                    Is_Controllable_By_Prognosis = False
                    Each_String = False
            
            Each_String_Diag_Controllable.append(Each_String)
            i += 1


        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        return False


def IsSafeControlByProg_Publish():
    """[Check if automata is safe control by prognosis. Return if each string is safe control by prognosis]
    """
    print('\n\n* CONTROLABILIDADE SEGURA PELA PROGNOSE\n')

    # if it is Language Diagnosable:
    if IsDiag(): 
        # * first condition is C condition

        # get reachable states from FU.
        FU_states = FU_s.Get_FU_s()
        FU_states_ID = [] 
        for each in FU_states:
            FU_states_ID.append(DiagnoserFunctions.GetStateId(each)) 

        Reachable = [] 
        for each in FU_states: 
            each_name = DiagnoserFunctions.GetStateId(each) 
            Reachable.append(DefineStrings.GetDiagReachable(each_name)) 

        # getting the names. Pegando o nomes dos estados alcançaveis a partir dos Fu(s)
        i = 0 
        Reachable_Names = [] 
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each)) 
            Reachable_Names.append(names) 
            i += 1 

        # test if there is any Normal or Uncertain Cycle (C condition).
        test_normal = DefineStrings.IsNormalCycle(Reachable) 
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable, antes_fu=True) 

        # * second condition is: sub-strings must have a controllable state between a FP and a FB

        # getting FP(s) names
        FP_s_Names = FP_s.GetFP_s()

        FP_s_IDs = [] 
        for each in FP_s_Names: 
            FP_s_IDs.append(DiagnoserFunctions.GetStateId(each)) 

        # getting the FB states
        i = 0 
        FB_s_IDs = [] 
        while i < len(FU_states): 
            FB_s_IDs.append(FB_s.GetFB_s_IDs(i)) 
            i += 1 

        # getting FB(s) names
        FB_s_Names = [] 
        i = 0 
        while i < len(FB_s_IDs): 
            names = [] 
            for each in FB_s_IDs[i]: 
                names.append(DiagnoserFunctions.GetStateName(each)) 
            FB_s_Names.append(names) 
            i += 1 

        Sub_Strings_IDs = []  
        for each in FP_s_IDs: 
            Sub_Strings_IDs.append(DefineStrings.GetDiagReachable(each)) 

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = []
        i = 0
        while i < len(Sub_Strings_IDs): 
            bad_subsub = [] 
            for each in Sub_Strings_IDs[i]:
                if each in FB_s_IDs[i]:
                    bad_subsub.append(each) 
            the_bads_IDs.append(bad_subsub) 
            i+= 1 

        i = 0 
        control_FP_FB = [] 
        j = 0
        while j < len(the_bads_IDs): 
            cont = [] 
            for each in the_bads_IDs[j]:
                cont.append(DefineStrings.AreAllWaysControllable(FP_s_IDs[j], each))
            j += 1 
            control_FP_FB.append(cont) 

        # * testing both conditions:

        # calculating and printing the answers

        Is_Controllable_By_Prognosis = True
        Each_String_Diag_Controllable = []

        for i in range(len(FU_states)):

            Each_String = True
            print('Para a cadeia', i + 1, 'calcula-se o FP(s) e o FB(s)')
            
            if len(FP_s_Names[i]) == 0:
                print('FP(', i + 1, ') =', FP_s_Names[i],)
            else:
                print('FP(', i + 1, ') = [', FP_s_Names[i],']')
            print('FB(', i + 1, ') =', FB_s_Names[i],'\n')

            if len(FP_s_Names[i]) == 0:
                print('A cadeia', i + 1, 'não garante prognose e, portanto, não é prognosticável.\n')
                Is_Controllable_By_Prognosis = False
                Each_String = False

            normal = False
            incerto = False
            for k in test_normal[1]:
                if k in Reachable[i] and not incerto and Each_String:
                    print('A cadeia', i + 1, 'possui um ciclo normal em [',k,'] e, portanto, não é prognosticável.\n')
                    Is_Controllable_By_Prognosis = False
                    normal = True
                    break
            for k in test_uncertain[1]:
                if k in Reachable[i] and not normal and Each_String:
                    print('A cadeia', i + 1, 'possui um ciclo incerto em [',k,'] e, portanto, não é prognosticável.\n')
                    Is_Controllable_By_Prognosis = False
                    incerto = True
                    break

            if Each_String:
                if False in control_FP_FB[i]:  
                    index = control_FP_FB[i].index(False)
                    print('No conjunto de eventos que ocorre entre [', FP_s_Names[i], '] e [', FB_s_Names[i][index],
                          '] não há um evento controlável.'
                          '\nPortanto, a cadeia', i + 1, 'não é controlável segura pela prognose.\n')
                    Is_Controllable_By_Prognosis = False
                    Each_String = False
            
            if Each_String:
                print('Na cadeia', i + 1, 'não há ciclos incertos ou normais. Além disso, sempre há um',
                      'evento controlável entre um estado FP(', i + 1, ') e um estado FB(', i + 1, ').',
                      '\nPortanto, a cadeia', i + 1, 'é controlável segura pela prognose.\n')
            Each_String_Diag_Controllable.append(Each_String)
            i += 1

        if Is_Controllable_By_Prognosis == True:
            print('A linguagem é controlável segura pela prognose.')
        else:
            print('A linguagem não é controlável segura pela prognose.')

        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        print('\nA linguagem não é controlável segura pela prognose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiagAndProg_Publish():
    """[Check if automata is safe control by diagnosis and safe control by prognosis. 
    Return if each string is safe control by diagnosis and safe control by prognosis]
    """

    # if it is Language Diagnosable:
    if IsDiag(): 

        # get FU (so I know where diagnoser is going to fail)
        FU = FU_s.Get_FU_s() 

        # getting the event sequence to the fault
        i = 0 
        Fault_Diag_EventStrings_IDs = [] 
        while i < len(FU): 
            fault_state = FU[i] 
            fault_state_ID = DiagnoserFunctions.GetStateId(fault_state) 
            Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID)) 
            i += 1 

        i = 0 
        while i < len(Fault_Diag_EventStrings_IDs): 
            state_name = [] 
            for each in Fault_Diag_EventStrings_IDs[i]: 
                state_name.append(DiagnoserFunctions.GetEventName(each)) 
            state_name.append(AutomataFunctions.GetFaultEventName()) 
            i += 1 

        print('\n\nPara cada cadeia, calcula-se a controlabilidade segura tanto pela diagnose quanto pela prognose:')

        by_diag = IsSafeControlByDiag_Publish()
        by_prog = IsSafeControlByProg_Publish()

        print('\n\n* CONTROLABILIDADE SEGURA PELA DIAGNOSE E PROGNOSE\n')

        Is_Controllable = True
        string = 0
        while string < len(by_diag):
            if by_diag[string] and by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura tanto pela diagnose quanto pela prognose.')
            elif by_diag[string]:
                print('A cadeia', string+1, 'é controlável segura pela diagnose.')
            elif by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura pela prognose.')
            else:
                print('A cadeia', string+1, 'não é controlável segura pela diagnose ou pela prognose.')
                Is_Controllable = False
            string += 1

        if Is_Controllable:
            print('\nPortanto, a linguagem é controlável segura pela diagnose e pela prognose')
        else:
            print('\nPortanto, a linguagem não é controlável segura pela diagnose e pela prognose')

        return Is_Controllable

    # if it is not Language Diagnosable:
    else:
        print('A linguagem não é controlável segura pela diagnose e prognose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiagAndProg_SelfPublish():
    """[Check if automata is safe control by diagnosis and safe control by prognosis. 
    Return if each string is safe control by diagnosis and safe control by prognosis]
    """

    # if it is Language Diagnosable:
    if IsDiag():

        # get FU (so I know where diagnoser is going to fail)
        FU = FU_s.Get_FU_s()

        # getting the event sequence to the fault
        i = 0
        Fault_Diag_EventStrings_IDs = []
        while i < len(FU):
            fault_state = FU[i]
            fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
            Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
            i += 1


        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            i += 1

        by_diag = IsSafeControlByDiag()
        by_prog = IsSafeControlByProg()

        print('\n\n* CONTROLABILIDADE SEGURA PELA DIAGNOSE E PROGNOSE\n')

        # getting these events names
        Fault_Aut_Strings_Names = []
        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            Fault_Aut_Strings_Names.append(state_name)
            i += 1

        Is_Controllable = True
        string = 0
        while string < len(by_diag):
            if by_diag[string] and by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura tanto pela diagnose quanto pela prognose.')
            elif by_diag[string]:
                print('A cadeia', string+1, 'é controlável segura pela diagnose.')
            elif by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura pela prognose.')
            else:
                print('A cadeia', string+1, 'não é controlável segura pela diagnose ou pela prognose.')
                Is_Controllable = False
            string += 1

        if Is_Controllable:
            print('\nPortanto, a linguagem é controlável segura pela diagnose e pela prognose')
        else:
            print('\nPortanto, a linguagem não é controlável segura pela diagnose e pela prognose')

        return Is_Controllable

    # if it is not Language Diagnosable:
    else:
        print('A linguagem não é controlável segura pela diagnose e prognose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiagAndProg():
    """[Check if automata is safe control by diagnosis and safe control by prognosis. 
    If it is, return True, else, return False]
    """
    # if it is Language Diagnosable:
    if IsDiag(): 

        by_diag = IsSafeControlByDiag() 
        by_prog = IsSafeControlByProg() 

        Is_Controllable = True 
        string = 0 
        while string < len(by_diag): 
            if not (by_diag[string] or by_prog[string]): 
                Is_Controllable = False 
            string += 1 
        print(Is_Controllable)
        return Is_Controllable

    # if it is not Language Diagnosable:
    else:
        return False
