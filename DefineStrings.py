import copy
import AutomataParser
import AutomataFunctions
import DiagnoserParser
import DiagnoserFunctions
import AuxiliaryFunctions
import FU_s


def GetFaultEventsPosition(): 
    Fault_Events = [] 
    Fault_Event = AutomataFunctions.GetFaultEvent()  
    
    x = 0 
    for each in AutomataParser.Aut_Transition_Event_Table: 
        if each == Fault_Event: 
            Fault_Events.append(x)  
        x = x + 1 

    return (Fault_Events) 


def GetLastState(state): 
    x = len(AutomataParser.Aut_Transition_Source_Table) 
    positions = [] 
    targets = []

    for n in range(0, x): 
        a = str(AutomataParser.Aut_Transition_Target_Table[n]) 
        if state == a:
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = AutomataParser.Aut_Transition_Source_Table[m] 
        targets.append(target) 

    return (targets) 


def GetLastEvent(state): 
    x = len(AutomataParser.Aut_Transition_Source_Table) 
    positions = [] 
    targets = [] 

    for n in range(0, x): 
        a = str(AutomataParser.Aut_Transition_Target_Table[n]) 
        if state == a: 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = AutomataParser.Aut_Transition_Event_Table[m] 
        targets.append(target) 

    return (targets) 


def GetOneLastEvent(state): 
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = str(AutomataParser.Aut_Transition_Target_Table[n])
        if state == a:
            positions.append(n)

    for each in positions:
        m = int(each)
        target = AutomataParser.Aut_Transition_Event_Table[m]
        targets.append(target)

    return (targets[0])


def GetNextStatesInID(state):
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = [] 
    targets = []

    for n in range(0, x): 
        a = str(AutomataParser.Aut_Transition_Source_Table[n])
        if state == a: 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = AutomataParser.Aut_Transition_Target_Table[m] 
        targets.append(target) 

    return (targets) 


def GetString(position):
    initial_state = AutomataParser.Aut_Initial_State_ID  
    state = AutomataParser.Aut_Transition_Target_Table[position]
    seq = GetAutomataStringBtw(initial_state, state)

    ret = []  
    i = 0 
    while i<len(seq): 
        hold = [] 
        for each in seq[i]: 
            for one in each: 
                hold.append(one) 
        del(hold[-1]) 
        ret.append(hold) 
        i += 1 

    return ret 


def GetDiagnoserString(targetID): 
    initial_state = DiagnoserParser.Initial_State_ID  
    seq = GetDiagnoserStringBtw(initial_state, targetID)  
    ret = []  
    i = 0 

    while i<len(seq): 
        hold = [] 
        for each in seq[i]: 
            for one in each: 
                hold.append(one) 
        ret.append(hold) 
        i += 1 

    return ret 


def GetDiagReachable(state_ID): 
    string_states_IDs = [] 
    verified_states = []
    actual_state_ID = [state_ID] 
    ended = False 
    while not ended: 
        for each in actual_state_ID:
            if each not in verified_states: 
                verified_states.append(each)
                next_state_IDs = DiagnoserFunctions.GetNextStatesInID(each) 
            for each in next_state_IDs: 
                if each not in string_states_IDs: 
                    string_states_IDs.append(each) 
                    actual_state_ID.append(each) 
        ended = True 
    return string_states_IDs


def GetAutReachable(state_ID): 
    string_states_IDs = [] 
    verified_states = [] 
    actual_state_ID = [state_ID] 
    ended = False
    while not ended: 
        for each in actual_state_ID:
            if each not in verified_states: 
                verified_states.append(each) 
                next_state_IDs = AutomataFunctions.GetNextStatesInID(each) 
            for each in next_state_IDs: 
                if each not in string_states_IDs: 
                    string_states_IDs.append(each) 
                    actual_state_ID.append(each) 
        ended = True 
    return string_states_IDs 


def GetDiagnoserStringBtw_WithoutLoop(sourceID,targetID, just_string=False):
    Event_Sequence = [] 
    W = 0
    # runs only if it is possible to reach it (returns [] if there is no possible string)
    if targetID in GetDiagReachable(sourceID): 
        State_Sequence = [[sourceID]]
        state = sourceID 
        actual_state = state 
        actual_way = 0 
        way_num = 1 
        status = False 
        first_loop_state = 0
        NextStatesIdsLoop = False

        while not status: 
            NextStatesIds = DiagnoserFunctions.GetNextStatesInID(actual_state) 
            NextState = [] 
            n = 0 

            if first_loop_state == actual_state:
                NextStatesIdsLoop = True
                W += 1
            else:
                first_loop_state = actual_state

            for each in NextStatesIds: 
                targets = GetDiagReachable(each) 
                Loop = AuxiliaryFunctions.loop_verification(targets, State_Sequence[actual_way])

                if ((targetID in targets) or (each == targetID)) and (each not in State_Sequence[actual_way]) and not Loop: 
                    NextState.append(each) 
                    n += 1 

            # if more then one next state was saved, increases the number of ways to get to the target
            way_num += len(NextState) -1 

            if NextStatesIdsLoop and W > 5:
                State_Sequence = AuxiliaryFunctions.NextStatesIdsLoopWithoutLoop(actual_state, targetID, State_Sequence)
                break

            # and copy actual way how many times it's needed
            i = 1 
            while i < len(NextState): 
                State_Sequence.insert(i+actual_way,copy.deepcopy(State_Sequence[actual_way])) 
                i += 1 

            #save the next states on respectives copied ways
            i = actual_way 
            for each in NextState: 
                State_Sequence[i].append(each) 
                i += 1 

            # if ended one string, go to the next one
            if State_Sequence[actual_way][-1] == targetID:
                actual_way += 1

            # if still have strings to test, update actual_state to last one
            if actual_way < len(State_Sequence):
                actual_state = State_Sequence[actual_way][-1]
            # and if there is no more strings to test, end it
            else:
                status = True
        
        if just_string:
            return State_Sequence

        # getting the events for the state sequence
        i = 0
        while i < len(State_Sequence):
            answer = []
            j = 0
            while j < len(State_Sequence[i])-1:
                answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[i][j], State_Sequence[i][j+1]))
                j += 1
            Event_Sequence.append(answer)
            i += 1
    return Event_Sequence


# def GetDiagnoserStringBtw(sourceID,targetID):
#     if targetID in GetDiagReachable(sourceID): 
#         State_Sequence = [[sourceID]]
#         state = sourceID
#         actual_state = state 
#         actual_way = 0 
#         way_num = 1 
#         status = False 
#         there_is_loop = False
#         loops_event_sequence = list()
#         todas_as_cadeias = list()
#         num_loop = 0

#         while not status:        
#             lista_eventos_ruins = list()
#             lista_eventos_bons = list()
#             lista_termos_ruins = list()
#             for i in range(len(State_Sequence)):

#                 #? Função que tirar loops indevidos. Exemplo: ['1', '2', '1', '2'] 
#                 strin = ''
#                 for each in State_Sequence[i]:
#                     strin = strin + str(each)

#                 n_termos = 1
#                 n = [1,2,3,4,5,6,7,8,9,10]
#                 for numero in n:
#                     if numero*2 < len(strin):
#                         n_termos += 1
#                     else:
#                         break

#                 lista_termos = list()
#                 while n_termos != 1:
#                     for n in range(len(strin)-n_termos+1):
#                         lista_termos.append(strin[n:n+n_termos])
#                     n_termos -= 1

#                 for k in range(len(lista_termos)):
#                     if k+len(lista_termos[k]) < len(lista_termos):
#                         targets_ultimo = DiagnoserFunctions.GetNextStatesInID(State_Sequence[i][-1])
#                         if lista_termos[k] == lista_termos[k+len(lista_termos[k])] and len(targets_ultimo) < 3:
#                             if len(targets_ultimo) == 1:
#                                 lista_termos_ruins.append(State_Sequence[i])
#                                 break

#                             else:
#                                 for j in range(len(State_Sequence[i])):
#                                     if State_Sequence[i][j] in DiagnoserFunctions.GetNextStatesInID(State_Sequence[i][j]):
#                                         lista_termos_ruins.append(State_Sequence[i])
#                                         break

#                 for j in range(len(State_Sequence[i])):
#                     if State_Sequence[i].count(str(State_Sequence[i][j])) > 2:
#                         lista_eventos_ruins.append(State_Sequence[i])
#                         break
#                     elif State_Sequence[i].count(str(actual_state)) == 2:
#                         lista_eventos_bons.append(State_Sequence[i])
#                         break

#             if len(lista_eventos_ruins) > 0:
#                 maior = True
#             else:
#                 maior = False

#             if len(lista_eventos_bons) > 0:
#                 igual = True
#             else:
#                 igual = False

#             if len(lista_termos_ruins) > 0:
#                 repetido = True
#             else:
#                 repetido = False 

#             for i in range(0, len(State_Sequence)):
#                 if  maior:
#                     for each in lista_eventos_ruins:
#                         State_Sequence.remove(each)
                
#                 if repetido:
#                     for each in lista_termos_ruins:
#                         State_Sequence.remove(each)  
                
                
#                 elif igual:
#                     for each in lista_eventos_bons:
#                         a = each.copy()
#                         State_Sequence.remove(a)
#                         loops_sequences = [a]

#                         todas_as_cadeias.append(a[:])
#                         if a[-1] != targetID:
#                             final_cadeia = GetDiagnoserStringBtw_WithoutLoop(a[-1], targetID, just_string=True)[0]

#                             for x in range(len(final_cadeia)):
#                                 if x != 0:
#                                     todas_as_cadeias[-1].append(final_cadeia[x])

#                         nao = False
#                         if targetID in a:
#                             nao = True

#                         k = 0
#                         while k < len(loops_sequences):
#                             answer = []
#                             j = 0
#                             while j < len(loops_sequences[k])-1:
#                                 answer.append(DiagnoserFunctions.GetEventBetween(loops_sequences[k][j], loops_sequences[k][j+1]))
#                                 j += 1
#                             loops_event_sequence.append(answer)
#                             k += 1
                        
#                         if not nao:
#                             loop_event_sequence = GetDiagnoserStringBtw_WithoutLoop(a[-1], targetID)[0]

#                             for x in loop_event_sequence:
#                                 if nao:
#                                     break
#                                 loops_event_sequence[num_loop].append(x)
#                             num_loop += 1 


#                 if len(State_Sequence) == 1 and State_Sequence[0][-1] == targetID:
#                     status = True

#                 if len(State_Sequence) == 0:
#                     status = True

#                 if igual or maior or repetido or there_is_loop:
#                     if len(State_Sequence) != 0:
#                         for k in range(len(State_Sequence)):
#                             if State_Sequence[k][-1] == targetID:
#                                 status = True

#                             if State_Sequence[k][-1] != targetID:
#                                 actual_state = State_Sequence[k][-1]
#                                 actual_way = k
#                                 status = False
#                                 break
#                     break

#             if status:
#                 break
            
#             NextStatesIds = DiagnoserFunctions.GetNextStatesInID(actual_state) 
#             NextState = [] 
#             n = 0

#             for each in NextStatesIds:
#                 targets = GetDiagReachable(each) 

#                 if ((targetID in targets) or (each == targetID)): 
#                     NextState.append(each) 
#                     n += 1 

#             # if more then one next state was saved, increases the number of ways to get to the target
#             way_num += len(NextState) -1 

#             # and copy actual way how many times it's needed
#             i = 1 
#             while i < len(NextState): 
#                 State_Sequence.insert(i+actual_way,copy.deepcopy(State_Sequence[actual_way])) 
#                 i += 1 

#             #save the next states on respectives copied ways
#             i = actual_way 
#             for each in NextState: 
#                 State_Sequence[i].append(each) 
#                 i += 1 

#             # if ended one string, go to the next one
#             if State_Sequence[actual_way][-1] == targetID:
#                 actual_way += 1

#             # if still have strings to test, update actual_state to last one
#             if actual_way < len(State_Sequence):
#                 actual_state = State_Sequence[actual_way][-1]
#             # and if there is no more strings to test, end it
#             else:
#                 status = True

#         #? Pega a combinação linear dos loops
#         if len(todas_as_cadeias) != 0:
#             comum_inicial = list()
#             inicial = True

#             comum_final = list()
#             final = True
#             diferente = list()

#             i = 0 #posições
#             parar = False
#             while not parar:
#                 estado_igual1 = list()
#                 estado_igual2 = list()
#                 for j in range(len(todas_as_cadeias)):  #cadeia
#                     estado_igual1.append(todas_as_cadeias[j][i])
#                     if i != 0:
#                         estado_igual2.append(todas_as_cadeias[j][-i])
                        
#                     if i+1 == len(todas_as_cadeias[j]):
#                         parar = True
                        
#                 if len(set(estado_igual1)) == 1 and inicial:
#                     comum_inicial.append(estado_igual1[0][0]) 
#                 else:
#                     inicial = False

#                 if len(set(estado_igual2)) == 1 and final:
#                     comum_final.append(estado_igual2[0][0])
#                 elif i != 0:
#                     final = False
                    
#                 i += 1
                
#             comum_final.reverse()
#             comum_final.pop(0)
#             diferente = todas_as_cadeias[:]
#             for n in range(len(diferente)):
#                 del(diferente[n][:len(comum_inicial)])
#                 del(diferente[n][-len(comum_final):])

#             for n in range(len(diferente)):
#                 for k in range(len(diferente)):
#                     if n + k < len(diferente) and diferente[n] != diferente[n+k] and comum_inicial + diferente[n] + diferente[n+k] + comum_final not in State_Sequence: 
#                         State_Sequence.append(comum_inicial + diferente[n] + diferente[n+k] + comum_final)
                        
#                     elif diferente[n] != diferente[n+k-len(diferente)] and comum_inicial + diferente[n] + diferente[n+k-len(diferente)] + comum_final not in State_Sequence:
#                         State_Sequence.append(comum_inicial + diferente[n] + diferente[n+k-len(diferente)] + comum_final)
            
#         if len(State_Sequence) != 0:
#             primordia_state_sequence = list()
#             k = 0
#             while k < len(State_Sequence):
#                 answer = []
#                 j = 0
#                 while j < len(State_Sequence[k])-1:
#                     answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[k][j], State_Sequence[k][j+1]))
#                     if State_Sequence[k][j+1] == targetID:
#                         break
#                     j += 1
                
#                 if len(State_Sequence[k]) == 1:
#                     answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[k][0], State_Sequence[k][0]))
#                 primordia_state_sequence.append(answer)
#                 k += 1

#             i = 0
#             for x in primordia_state_sequence:
#                 loops_event_sequence.insert(i, x)
#                 i += 1

#         return loops_event_sequence



























































def GetAutomataStringBtw_WithoutLoop(sourceID,targetID, just_string=False): 
    Event_Sequence = [] 
    W = 0
    # runs only if it is possible to reach it (returns [] if there is no possible string)
    if targetID in GetAutReachable(sourceID): 
        State_Sequence = [[sourceID]] 
        state = sourceID 
        actual_state = state 
        actual_way = 0 
        way_num = 1 
        status = False 
        first_loop_state = 0
        NextStatesIdsLoop = False

        while not status: 
            NextStatesIds = AutomataFunctions.GetNextStatesInID(actual_state) 
            NextState = [] 
            n = 0

            if first_loop_state == actual_state:
                NextStatesIdsLoop = True
                W += 1
            else:
                first_loop_state = actual_state

            for each in NextStatesIds: 
                targets = GetAutReachable(each) 
                Loop = AuxiliaryFunctions.loop_verification(targets, State_Sequence[actual_way])

                if ((targetID in targets) or (each == targetID)) and (each not in State_Sequence[actual_way]) and not Loop:
                    NextState.append(each) 
                    n += 1 

            # if more then one next state was saved, increases the number of ways to get to the target
            way_num += len(NextState) -1 

            if NextStatesIdsLoop and W > 5:
                State_Sequence = AuxiliaryFunctions.NextStatesIdsLoopWithoutLoop(actual_state, targetID, State_Sequence)
                break

            # and copy actual way how many times it's needed
            i = 1 
            while i < len(NextState):
                State_Sequence.insert(i+actual_way,copy.deepcopy(State_Sequence[actual_way]))
                i += 1 

            #save the next states on respectives copied ways
            i = actual_way 
            for each in NextState:
                State_Sequence[i].append(each) 
                i += 1 

            # if ended one string, go to the next one
            if State_Sequence[actual_way][-1] == targetID:
                actual_way += 1

            # if still have strings to test, update actual_state to last one
            if actual_way < len(State_Sequence):
                actual_state = State_Sequence[actual_way][-1]
            # and if there is no more strings to test, end it
            else:
                status = True
        
        if just_string:
            return State_Sequence

        # getting the events for the state sequence
        i = 0
        while i < len(State_Sequence):
            answer = []
            j = 0
            while j < len(State_Sequence[i])-1:
                answer.append(AutomataFunctions.GetEventBetween(State_Sequence[i][j], State_Sequence[i][j+1]))
                j += 1
            Event_Sequence.append(answer)
            i += 1
    return Event_Sequence


def GetAutomataStringBtw(sourceID,targetID):
    if targetID in GetAutReachable(sourceID): 
        State_Sequence = [[sourceID]]
        state = sourceID
        actual_state = state 
        actual_way = 0 
        way_num = 1 
        status = False 
        there_is_loop = False

        loops_event_sequence = list()
        todas_as_cadeias = list()
        num_loop = 0

        while not status:        
            lista_eventos_ruins = list()
            lista_eventos_bons = list()
            lista_termos_ruins = list()
            for i in range(len(State_Sequence)):

                #? Função que tirar loops indevidos. Exemplo: ['1', '2', '1', '2'] 
                #! Isso aqui da pra arrumar, não precisa usar strings, da pra fazer com lista

                n_termos = 0
                for numero in range(1, len(State_Sequence[i])):
                    if numero*2 <= len(State_Sequence[i]):
                        n_termos += 1
                        
                lista_termos = list()
                for k in range(n_termos, 1, -1):
                    for n in range(len(State_Sequence[i]) - k + 1):
                        lista_termos.append(State_Sequence[i][n:n+k])

                for k in range(len(lista_termos)):
                    if k+len(lista_termos[k]) < len(lista_termos):
                        targets_ultimo = AutomataFunctions.GetNextStatesInID(State_Sequence[i][-1])
                        if lista_termos[k] == lista_termos[k+len(lista_termos[k])] and len(targets_ultimo) < 3:
                            if len(targets_ultimo) == 1:
                                lista_termos_ruins.append(State_Sequence[i])
                                break

                            else:
                                for j in range(len(State_Sequence[i])):
                                    if State_Sequence[i][j] in AutomataFunctions.GetNextStatesInID(State_Sequence[i][j]):
                                        lista_termos_ruins.append(State_Sequence[i])
                                        break
                
                for j in range(len(State_Sequence[i])):
                    if State_Sequence[i].count(str(State_Sequence[i][j])) > 2:
                        lista_eventos_ruins.append(State_Sequence[i])
                        break
                    elif State_Sequence[i].count(str(actual_state)) == 2:
                        lista_eventos_bons.append(State_Sequence[i])
                        break

            if len(lista_eventos_ruins) > 0:
                maior = True
            else:
                maior = False

            if len(lista_eventos_bons) > 0:
                igual = True
            else:
                igual = False

            if len(lista_termos_ruins) > 0:
                repetido = True
            else:
                repetido = False 

            for i in range(0, len(State_Sequence)):
                if  maior:
                    for each in lista_eventos_ruins:
                        State_Sequence.remove(each)
                
                if repetido:
                    for each in lista_termos_ruins:
                        State_Sequence.remove(each)  
                
                
                elif igual:
                    for each in lista_eventos_bons:
                        a = each.copy()
                        State_Sequence.remove(a)
                        loops_sequences = [a]

                        todas_as_cadeias.append(a[:])

                        #? Essa parte faz a mesma coisa que uma parte há baixo, porém lá pega os eventos, enquanto que aqui 
                        #? pega os estados
                        if a[-1] != targetID:
                            final_cadeia = GetAutomataStringBtw_WithoutLoop(a[-1], targetID, just_string=True)

                            todas_as_cadeias[-1].pop(-1)
                            for k in range(len(final_cadeia)):
                                final_cadeia[k] = todas_as_cadeias[-1] + final_cadeia[k]
                            todas_as_cadeias.pop(-1)

                            for cadeia in final_cadeia:
                                todas_as_cadeias.append(cadeia)

                        nao = False
                        if targetID in a:
                            nao = True

                        k = 0
                        while k < len(loops_sequences):
                            answer = []
                            j = 0
                            while j < len(loops_sequences[k])-1:
                                answer.append(AutomataFunctions.GetEventBetween(loops_sequences[k][j], loops_sequences[k][j+1]))
                                j += 1
                            loops_event_sequence.append(answer)
                            k += 1
                        
                        if not nao:
                            loop_event_sequence = GetAutomataStringBtw_WithoutLoop(a[-1], targetID)

                            for k in range(len(loop_event_sequence)):
                                loop_event_sequence[k] = loops_event_sequence[-1] + loop_event_sequence[k]
                            loops_event_sequence.pop(-1)

                            for cadeia in loop_event_sequence:
                                loops_event_sequence.append(cadeia)

                if len(State_Sequence) == 1 and State_Sequence[0][-1] == targetID:
                    status = True

                if len(State_Sequence) == 0:
                    status = True

                if igual or maior or repetido or there_is_loop:
                    if len(State_Sequence) != 0:
                        for k in range(len(State_Sequence)):
                            if State_Sequence[k][-1] == targetID:
                                status = True

                            if State_Sequence[k][-1] != targetID:
                                actual_state = State_Sequence[k][-1]
                                actual_way = k
                                status = False
                                break
                    break

            if status:
                break
            
            NextStatesIds = AutomataFunctions.GetNextStatesInID(actual_state) 
            NextState = [] 
            n = 0

            for each in NextStatesIds:
                targets = GetAutReachable(each) 

                if ((targetID in targets) or (each == targetID)): 
                    NextState.append(each) 
                    n += 1 

            # if more then one next state was saved, increases the number of ways to get to the target
            way_num += len(NextState) -1 

            # and copy actual way how many times it's needed
            i = 1 
            while i < len(NextState): 
                State_Sequence.insert(i+actual_way,copy.deepcopy(State_Sequence[actual_way])) 
                i += 1 

            #save the next states on respectives copied ways
            i = actual_way 
            for each in NextState: 
                State_Sequence[i].append(each) 
                i += 1 

            # if ended one string, go to the next one
            if State_Sequence[actual_way][-1] == targetID:
                actual_way += 1

            # if still have strings to test, update actual_state to last one
            if actual_way < len(State_Sequence):
                actual_state = State_Sequence[actual_way][-1]
            # and if there is no more strings to test, end it
            else:
                status = True

        #? Pega a combinação linear dos loops
        if len(todas_as_cadeias) > 1:

            inicial = True
            final = True

            strings_module = {
                'initial': [],
                'middle':[],
                'different':[],
                'final': []
            }

            i = 0 #posições
            parar = False
            while not parar:
                estado_igual1 = list()
                estado_igual2 = list()
                for j in range(len(todas_as_cadeias)):  #cadeia
                    estado_igual1.append(todas_as_cadeias[j][i])
                    if i != 0:
                        estado_igual2.append(todas_as_cadeias[j][-i])
                        
                    if i+1 == len(todas_as_cadeias[j]):
                        parar = True
                
                if len(set(estado_igual1)) == 1 and inicial:
                    strings_module['initial'].append(estado_igual1[0])
                else:
                    inicial = False
                    
                if len(set(estado_igual2)) == 1 and final:
                    strings_module['final'].append(estado_igual2[0])
                elif i != 0:
                    final = False
                    
                i += 1

            strings_module['final'].reverse()
            strings_module['final'].pop(0)

            diferente = todas_as_cadeias[:]
            for n in range(len(diferente)):
                del(diferente[n][:len(strings_module['initial'])])
                del(diferente[n][-len(strings_module['final']):])
            key_state = diferente[0][-1]

            diferente1 = list()
            for i in range(len(diferente)):
                for k in range(len(diferente[i])):
                    if diferente[i][k] == key_state and k != len(diferente[i])-1:
                        diferente1.append(diferente[i][:k+1])
                        diferente[i] = diferente[i][k+1:]
                        break
            [strings_module['middle'].append(x) for x in diferente1 if not strings_module['middle'].count(x)]
            [strings_module['different'].append(x) for x in diferente if not strings_module['different'].count(x)]

            if len(strings_module['middle']) == 0:
                while strings_module['initial'][-1] != strings_module['different'][0][-1]: #comparando
                    for n in range(len(strings_module['different'])): #adicionando
                        strings_module['different'][n].insert(0, strings_module['initial'][-1])
                    strings_module['initial'].pop(-1) #excluindo
            else:
                for i in range(len(strings_module['middle'])):
                    while strings_module['middle'][i][-1] != strings_module['different'][0][-1]: #comparando
                        for n in range(len(strings_module['different'])): #adicionando
                            strings_module['different'][n].insert(0, strings_module['initial'][-1])
                        strings_module['initial'].pop(-1) #excluindo

            listao = list()
            if strings_module['middle'] != []:
                for state in strings_module['middle']:
                    for n in range(len(strings_module['different'])):
                        for k in range(len(strings_module['different'])):
                            if n + k < len(strings_module['different']) and strings_module['different'][n] != strings_module['different'][n+k] and strings_module['initial'] + strings_module['different'][n] + strings_module['different'][n+k] + strings_module['final'] not in State_Sequence: 
                                listao.append(strings_module['initial'] + state + strings_module['different'][n] + strings_module['different'][n+k] + strings_module['final'])

                            elif strings_module['different'][n] != strings_module['different'][n+k-len(strings_module['different'])] and strings_module['initial'] + strings_module['different'][n] + strings_module['different'][n+k-len(strings_module['different'])] + strings_module['final'] not in State_Sequence:
                                listao.append(strings_module['initial'] + state + strings_module['different'][n] + strings_module['different'][n+k-len(strings_module['different'])] + strings_module['final'])

            else:
                for n in range(len(strings_module['different'])):
                        for k in range(len(strings_module['different'])):
                            if n + k < len(strings_module['different']) and strings_module['different'][n] != strings_module['different'][n+k] and strings_module['initial'] + strings_module['different'][n] + strings_module['different'][n+k] + strings_module['final'] not in State_Sequence: 
                                listao.append(strings_module['initial'] + strings_module['different'][n] + strings_module['different'][n+k] + strings_module['final'])

                            elif strings_module['different'][n] != strings_module['different'][n+k-len(strings_module['different'])] and strings_module['initial'] + strings_module['different'][n] + strings_module['different'][n+k-len(strings_module['different'])] + strings_module['final'] not in State_Sequence:
                                listao.append(strings_module['initial'] + strings_module['different'][n] + strings_module['different'][n+k-len(strings_module['different'])] + strings_module['final'])
                                
            for each in listao:
                n_termos = 0
                for numero in range(1, len(each)):
                    if numero*2 < len(each):
                        n_termos += 1

                lista_termos = list()
                for i in range(n_termos, 1, -1):
                    for n in range(len(each) - i + 1):
                        lista_termos.append(each[n:n+i])
                        
                bad_string = False
                for k in range(len(lista_termos)):
                    if k + len(lista_termos[k]) < len(lista_termos):
                        if lista_termos[k] == lista_termos[k + len(lista_termos[k])]: #verificando se a cadeia repetida
                            if len(lista_termos[k + len(lista_termos[k])]) == len(lista_termos[k + len(lista_termos[k]) + 1]): #verificando se os tamanhos das cadeias são iguais
                            #existe esse if pois se o tamanho for diferente, "lista_termos[k + len(lista_termos[k]) + 1]" não estará correto
                                if lista_termos[k][-1] + lista_termos[k + len(lista_termos[k])][0] == lista_termos[k + len(lista_termos[k])][-1] + lista_termos[k + len(lista_termos[k]) + 1][-1]:
                                    #verificando se a cadeia está correta, ou seja, se esse loop a mais criado agrega em algo na cadeia final ou é apenas uma repetição
                                    bad_string = True
                                    break
                if not bad_string:
                    State_Sequence.append(each)

        if len(State_Sequence) != 0:
            primordia_state_sequence = list()
            k = 0
            while k < len(State_Sequence):
                answer = []
                j = 0
                while j < len(State_Sequence[k])-1: 
                    answer.append(AutomataFunctions.GetEventBetween(State_Sequence[k][j], State_Sequence[k][j+1]))
                    if State_Sequence[k][j+1] == targetID:
                        break
                    j += 1
                primordia_state_sequence.append(answer)
                k += 1
            
            i = 0
            for x in primordia_state_sequence:
                loops_event_sequence.insert(i, x)
                i += 1

        return loops_event_sequence


def GetStringsToFault():
    fault_events = GetFaultEventsPosition() 

    # gets the sequence of events that lead to fault on automata
    fault_aut_strings = []
    for each in fault_events: 
        y = GetString(each) 
        fault_aut_strings.append(y) 
    i = 0 
    rows = len(fault_aut_strings)
    while i < rows:
        fault_aut_strings[i] = list(reversed(fault_aut_strings[i]))
        i += 1

    # gets the same sequence for diagnoser (event IDs may be different)
    fault_diag_strings = []
    i = 0
    while i < (len(fault_aut_strings)):
        diag_string = []
        for each in fault_aut_strings[i]:
            x = DiagnoserFunctions.GetEquivalentDiagEventFromAut(each)
            diag_string.append(x)
        fault_diag_strings.append(diag_string)
        i += 1
    i += 1

    return fault_aut_strings, fault_diag_strings


def GetDiagStates(diag_eventstrings_IDs):  # gets the sequence of diagnoser's states for a given event sequence

    sequence = [] 
    diag_fault_statestring_IDs = [] 

    for cada in diag_eventstrings_IDs: 
        seq_row = [DiagnoserParser.Initial_State_ID]  
        for n in range(0, len(cada)):
            x = DiagnoserFunctions.GetNextState(seq_row[n], cada[n]) 
            seq_row.append(x) 
        sequence.append(seq_row) 
        diag_fault_statestring_IDs.append(seq_row) 

    return diag_fault_statestring_IDs 


def GetStatePosition(state): 
    positions = [] 
    i = 0 
    while i < len(DiagnoserParser.Transition_Target_Table): 
        if DiagnoserParser.Transition_Target_Table[i] == state: 
            positions.append(i) 
        i += 1 
    return positions 


def DiagIDtoName(diag_statestrings_IDs):  # gets the names of diagnoser's states for a given ID sequence
    diag_fault_statestring_names = []
    i = 0
    while i < len(diag_statestrings_IDs):
        seq_row = []
        for each in diag_statestrings_IDs[i]:
            x = DiagnoserFunctions.GetStateName(each)
            seq_row.append(x)
        diag_fault_statestring_names.append(seq_row)
        i += 1
    return diag_fault_statestring_names


def IsNextStateUncertain(diag_fault_statestring_ID):  # evaluate if next state is uncertain and add it to the fault sequence if it is
    last_state = [] 
    i = 0 
    rows = len(diag_fault_statestring_ID) 
    while i < rows:
        last_state.append(diag_fault_statestring_ID[i][-1]) 
        i += 1 
    i = 0 
    end_loop = [['no'], ['no']] 
    while i < rows: 
        for ended in end_loop: 
            while ended == ['no']: 
                a = DiagnoserFunctions.GetNextStatesInID(last_state[i]) 
                for each in a: 
                    b = DiagnoserFunctions.GetStateName(each) 
                    if DiagnoserFunctions.IsUncertain(b) and each not in diag_fault_statestring_ID[i]: 
                        last_state[i] = each 
                        end_loop[i] = ['no'] 
                        diag_fault_statestring_ID[i].append(each)
                        break  
                    else: 
                        end_loop[i] = ['yes'] 
                ended = end_loop[i] 
        i += 1 
    return diag_fault_statestring_ID 


def GetDiagStateTarget(state):  
    source_table = DiagnoserParser.Transition_Source_Table 
    target_table = DiagnoserParser.Transition_Target_Table 

    size = len(source_table) 
    i = 0 
    target = [] 

    while i < size: 
        if source_table[i] == state: 
            target.append(target_table[i]) 
        i += 1 

    return (target) 


def AreAllWaysControllable(stateID1,stateID2): 
    event_string = GetDiagnoserStringBtw(stateID1,stateID2) 

    #finding if any event between the states is controllable
    i = 0 
    retval = True 
    while i < len(event_string): 
        test = False 
        for each in event_string[i]: 
            if DiagnoserFunctions.EventIsControllable(each[0]): 
                test = True 
        if not test: 
            retval = False 
        i += 1 

    return retval


def IsNormalCycle(diag_statestring_IDs):  # find uncertain loop in a given string

    # mark all uncertain states on each string
    NormalCycle = False
    i = 0 
    Eventos_falhas = list()
    while i < len(diag_statestring_IDs): 
        j = 0
        for each in diag_statestring_IDs[i]: 
            if DiagnoserFunctions.GetNextStatesInID(each)[0] == each or len(DiagnoserFunctions.GetNextStatesInID(each)) == 0: 
                name = DiagnoserFunctions.GetStateName(each)
                if DiagnoserFunctions.IsNormal(name):
                    NormalCycle = True
                    Eventos_falhas.append(diag_statestring_IDs[i][j])
            j += 1
        i += 1
    if NormalCycle:
        return NormalCycle, Eventos_falhas
    a = '-1'
    Eventos_falhas.append(a)
    return NormalCycle, Eventos_falhas


def IsUncertainCycle(diag_statestring_IDs,antes_fu=False):  # find uncertain loop in a given string

    if not antes_fu:
        UncertainCycle = False
        i = 0 
        Eventos_falhas = list()
        while i < len(diag_statestring_IDs): 
            j = 0
            for each in diag_statestring_IDs[i]:
                target =  DiagnoserFunctions.GetNextStatesInID(each)[0]
                if target == each or len(target) == 0 or each in DiagnoserFunctions.GetNextStatesInID(target): 
                    name = DiagnoserFunctions.GetStateName(each)
                    if DiagnoserFunctions.IsUncertain(name):
                        UncertainCycle = True
                        Eventos_falhas.append(diag_statestring_IDs[i][j])
                Next_States = DiagnoserFunctions.GetNextStatesInID(each) 
                for k in Next_States: 
                    name_next_state = DiagnoserFunctions.GetStateName(k) 
                    if DiagnoserFunctions.IsUncertain(name_next_state) and each in GetDiagReachable(k) and len(Next_States) > 1: 
                        estado_anterior = DiagnoserFunctions.GetPrevisousStatesInID(int(each))
                        nome_estado_anterior = DiagnoserFunctions.GetStateName(estado_anterior[0])
                        
                        if DiagnoserFunctions.IsUncertain(nome_estado_anterior): 
                            UncertainCycle = True
                            Eventos_falhas.append(diag_statestring_IDs[i][j])
                            break
                j += 1
            i += 1
        if UncertainCycle:
            return UncertainCycle, Eventos_falhas
        a = '-1'
        Eventos_falhas.append(a)

        return UncertainCycle, Eventos_falhas

    else:

        fu_name = FU_s.Get_FU_s()
        state_names = []
        state_ids = []
        for k in diag_statestring_IDs:
            for n in k:
                state_ids.append(n)
                state_names.append(DiagnoserFunctions.GetStateName(n))

        uncertain_cycle = False
        uncertain_state = ['-1']
        for i in range(len(state_names)):
            if DiagnoserFunctions.IsUncertain(state_names[i]):
                if state_names[i] not in fu_name:
                    uncertain_cycle = True
                    uncertain_state = [state_ids[i]]

        return uncertain_cycle, uncertain_state
