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






