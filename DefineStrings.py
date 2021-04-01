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


def GetDiagnoserStringBtw_WithoutLoop(sourceID,targetID):
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
                State_Sequence = AuxiliaryFunctions.NextStatesIdsLoopWithoutLoop(actual_state, State_Sequence)
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


def GetDiagnoserStringBtw(sourceID,targetID):
    if targetID in GetDiagReachable(sourceID): 
        State_Sequence = [[sourceID]]
        state = sourceID
        actual_state = state 
        actual_way = 0 
        way_num = 1 
        status = False 
        there_is_loop = False

        loops_event_sequence = list()
        num_loop = 0


        while not status:        
            lista_eventos_ruins = list()
            lista_eventos_bons = list()
            for i in range(len(State_Sequence)):
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

            for i in range(0, len(State_Sequence)):
                if  maior:
                    for each in lista_eventos_ruins:
                        State_Sequence.remove(each)
                    actual_state = State_Sequence[i][-1]

                if igual:
                    for each in lista_eventos_bons:
                        a = each.copy()
                        State_Sequence.remove(a)
                        loops_sequences = [a]
                        
                        k = 0
                        while k < len(loops_sequences):
                            answer = []
                            j = 0
                            while j < len(loops_sequences[k])-1:
                                answer.append(DiagnoserFunctions.GetEventBetween(loops_sequences[k][j], loops_sequences[k][j+1]))
                                j += 1
                            loops_event_sequence.append(answer)
                            k += 1
                        
                        novo_alvo = a[-1]
                        loop_event_sequence = GetDiagnoserStringBtw_WithoutLoop(novo_alvo, targetID)[0]

                        for x in loop_event_sequence:
                            loops_event_sequence[num_loop].append(x)
                        num_loop += 1 

                    actual_state = State_Sequence[i][-1]

                if len(State_Sequence) == 1 and State_Sequence[0][-1] == targetID:
                    status = True

                if len(State_Sequence) == 0:
                    status = True

                if igual or maior or there_is_loop:
                    break
            if status:
                break
            
            NextStatesIds = DiagnoserFunctions.GetNextStatesInID(actual_state) 
            NextState = [] 
            n = 0

            for each in NextStatesIds:
                targets = GetDiagReachable(each) 

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


        if len(State_Sequence) != 0:
            primordia_state_sequence = list()
            k = 0
            while k < len(State_Sequence):
                answer = []
                j = 0
                while j < len(State_Sequence[k])-1:
                    answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[k][j], State_Sequence[k][j+1]))
                    j += 1
                
                if len(State_Sequence[k]) == 1:
                    answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[k][0], State_Sequence[k][0]))
                primordia_state_sequence.append(answer)
                k += 1

            i = 0
            for x in primordia_state_sequence:
                loops_event_sequence.insert(i, x)
                i += 1

        return loops_event_sequence


def GetAutomataStringBtw_WithoutLoop(sourceID,targetID): 
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
                State_Sequence = AuxiliaryFunctions.NextStatesIdsLoopWithoutLoop(actual_state, State_Sequence)
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
        num_loop = 0


        while not status:        
            lista_eventos_ruins = list()
            lista_eventos_bons = list()
            for i in range(len(State_Sequence)):
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

            for i in range(0, len(State_Sequence)):
                if  maior:
                    for each in lista_eventos_ruins:
                        State_Sequence.remove(each)
                    actual_state = State_Sequence[i][-1]

                if igual:
                    for each in lista_eventos_bons:
                        a = each.copy()
                        State_Sequence.remove(a)
                        loops_sequences = [a]
                        
                        k = 0
                        while k < len(loops_sequences):
                            answer = []
                            j = 0
                            while j < len(loops_sequences[k])-1:
                                answer.append(AutomataFunctions.GetEventBetween(loops_sequences[k][j], loops_sequences[k][j+1]))
                                j += 1
                            loops_event_sequence.append(answer)
                            k += 1
                        
                        novo_alvo = a[-1]
                        loop_event_sequence = GetAutomataStringBtw_WithoutLoop(novo_alvo, targetID)[0]

                        for x in loop_event_sequence:
                            loops_event_sequence[num_loop].append(x)
                        num_loop += 1 

                    actual_state = State_Sequence[i][-1]

                if len(State_Sequence) == 1 and State_Sequence[0][-1] == targetID:
                    status = True

                if len(State_Sequence) == 0:
                    status = True

                if igual or maior or there_is_loop:
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


        if len(State_Sequence) != 0:
            primordia_state_sequence = list()
            k = 0
            while k < len(State_Sequence):
                answer = []
                j = 0
                while j < len(State_Sequence[k])-1:
                    answer.append(AutomataFunctions.GetEventBetween(State_Sequence[k][j], State_Sequence[k][j+1]))
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
