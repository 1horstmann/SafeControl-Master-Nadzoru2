import DefineStrings
import DiagnoserParser
import DiagnoserFunctions
import AutomataFunctions


def loop_verification(targets, State_Sequence):
    Loop = False
    if len(State_Sequence) > 1:

        State_Sequence_actual_way = list()
        if len(State_Sequence) > 2:
            for i in range(0, 2):
                State_Sequence_actual_way.append(State_Sequence[i])
        else:
            State_Sequence_actual_way = State_Sequence

        First = State_Sequence_actual_way[0]
        Position = list()
        for i in range(0, len(targets)):
            if First == targets[i]:
                Position.append(i)

        Len_State = len(State_Sequence_actual_way)
        Possible_matrix = list()
        for each in Position:
            Possible_vetor = list()
            if (each + Len_State) <= len(targets):
                for i in range(each, each + Len_State):
                    Possible_vetor.append(targets[i])
            Possible_matrix.append(Possible_vetor)

        for each in Possible_matrix:
            if each == State_Sequence_actual_way:
                Loop = True
                break
    return Loop


def NextStatesIdsLoopWithoutLoop(actual_state, targetID, State_Sequence_fora_do_loop):
    
    # Excluindo a cadeia com loop
    for i in range(0, len(State_Sequence_fora_do_loop)):
            if str(actual_state) in State_Sequence_fora_do_loop[i][-1]:
                State_Sequence_fora_do_loop.pop(i)
                break

    if len(State_Sequence_fora_do_loop) > 1:
        # Pegando todas as cadeias possíveis
        string = {'normal':[], 'falha':[]}
        for k in range(len(State_Sequence_fora_do_loop)):
            if State_Sequence_fora_do_loop[k][-1] == targetID:
                string['falha'] = State_Sequence_fora_do_loop[k]
            else:
                string['normal'] = State_Sequence_fora_do_loop[k]     

        State_Sequence_fora_do_loop = [string['falha']]
        for k in range(len(string['falha'])):
            if string['falha'][-k] == string['normal'][-1]:
                string['normal'] += string['falha'][-k+1:-1] + [string['falha'][-1]]
                State_Sequence_fora_do_loop.append(string['normal'])
                break

    return State_Sequence_fora_do_loop


def NextStatesIdsLoopWithLoop(actual_state, targetID, state_Sequence_fora_do_loop, diag):
    State_Sequence_fora_do_loop = []
    for i in range(len(state_Sequence_fora_do_loop)):
        if i == 0:
            tamanho = len(state_Sequence_fora_do_loop[i])
        else:
            tam = len(state_Sequence_fora_do_loop[i])
            if tam <= tamanho:
                tamanho = tam

    for i in range(len(state_Sequence_fora_do_loop)):
        if len(state_Sequence_fora_do_loop[i]) == tamanho:
            State_Sequence_fora_do_loop.append(state_Sequence_fora_do_loop[i])


    chegou_no_final = False
    State_Sequence = []
    for each in State_Sequence_fora_do_loop:
        if each[-1] == str(actual_state):
            State_Sequence_fora_do_loop.remove(each)
            State_Sequence = State_Sequence_fora_do_loop[:]
        else:
            State_Sequence.append(each)

    for each in State_Sequence_fora_do_loop:
        if each[-1] == targetID:
            State_Sequence = each
            chegou_no_final = True

    if len(State_Sequence) == 0:
        State_Sequence = State_Sequence_fora_do_loop[:]

    if not chegou_no_final:
        sourceID = State_Sequence[0][-1]
        
        if diag: 
            final_event_sequence = DefineStrings.GetDiagnoserStringBtw_WithoutLoop(sourceID, targetID)[0][0]
        else:
            final_event_sequence = DefineStrings.GetAutomataStringBtw_WithoutLoop(sourceID, targetID)[0][0]
        
        i = 0
        Event_Sequence = []
        while i < len(State_Sequence):
            answer = []
            j = 0
            while j < len(State_Sequence[i])-1:
                if diag:
                    answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[i][j], State_Sequence[i][j+1]))
                else:
                    answer.append(AutomataFunctions.GetEventBetween(State_Sequence[i][j], State_Sequence[i][j+1]))
                j += 1
            Event_Sequence.append(answer)
            i += 1

        Event_Sequence[0].append(final_event_sequence)

        return Event_Sequence[0], True

    return State_Sequence, False
    

def master_loop_verification():
    all_states = DiagnoserParser.State_Id_Table
    loop = False
    loop_state = list()
    for i in range(0, len(all_states)): 
        reachable_states = DefineStrings.GetDiagReachable(all_states[i]) 
        for n in reachable_states: 
            if n == all_states[i]:  
                loop = True
                next_states_loop = DiagnoserFunctions.GetNextStatesInID(all_states[i]) 
                for k in next_states_loop: 
                    if all_states[i] in DiagnoserFunctions.GetNextStatesInID(k): 
                        loop = False
                    else:
                        loop_state.append(all_states[i])

        if loop:
            break

    if len(loop_state) != 0:
        is_self_loop = DiagnoserFunctions.IsOnlySelfloop(loop_state[0])
    else:
        is_self_loop = 0

    if is_self_loop == 1:
        loop = False

    return loop


def checking_duplicate_string(Event_sequence):
    Final_Event_sequence = list()
    Final_Event_sequence.append(Event_sequence[0])
    for i in range(0, len(Event_sequence)):
        for j in range(0, len(Event_sequence)):
            if i != j and Event_sequence[i] != Event_sequence[j] and  Event_sequence[i] not in Final_Event_sequence:
                Final_Event_sequence.append(Event_sequence[i])

    return Final_Event_sequence






