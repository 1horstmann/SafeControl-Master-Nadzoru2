import AutomataParser
import DiagnoserParser
import AutomataFunctions
import DiagnoserFunctions
import DefineStrings
import FU_s


def GetSourcePosition(id_estado):
    n = 0
    positions = []
    for each in AutomataParser.Aut_Transition_Source_Table:
        if each == id_estado:
            positions.append(n)
        n = n + 1

    return (positions)


def GetEventsAfterState(positions):
    events = []
    for each in positions:
        events.append(AutomataParser.Aut_Transition_Event_Table[each])

    return (events)


def GetStatesAfterEstate(positions):
    states = []
    for each in positions:
        states.append(AutomataParser.Aut_Transition_Target_Table[each])

    return (states)


def GetStartingStates():
    Starting_States = []
    Faul_Events_Position = []
    Faul_Events_Position = DefineStrings.GetFaultEventsPosition()

    for each in Faul_Events_Position:
        Starting_States.append(AutomataParser.Aut_Transition_Target_Table[each])

    return (Starting_States)


# Returns the events sequence after a fault
def GetAutomataPathToAnalyse(FU_s_position):
    states = []
    temp = GetStartingStates()
    state = temp[FU_s_position]
    positions = []
    events = []
    aux = []
    aux_2 = []
    states.append(state)

    for each in states:
        if AutomataFunctions.IsSelfloopOnly(each) == 0:
            positions = GetSourcePosition(each)
            aux = GetEventsAfterState(positions)
            for cada in aux:
                if events.__contains__(cada) == False:
                    events.append(cada)
            aux_2 = GetStatesAfterEstate(positions)
            for cada in aux_2:
                if states.__contains__(cada) == False:
                    states.append(cada)

    return (events)


def GetAutomataEventsNames(FU_s_):
    events_names = []
    events = GetAutomataPathToAnalyse(FU_s_)
    for each in events:
        n = 0
        for cada in AutomataParser.Aut_Event_Id_Table:
            if cada == each:
                if events_names.__contains__(AutomataParser.Aut_Event_Name_Table[n]) == False:
                    events_names.append(AutomataParser.Aut_Event_Name_Table[n])
            n = n + 1

    return (events_names)


def GetFC_s_IDs(string):  # gets the FC(s) for a given string number

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


    # ignoring the non-certain ones
    the_certain_IDs = [] 
    i = 0  
    while i < len(string_states_names):  
        if DiagnoserFunctions.IsCertain(string_states_names[i]):  
            the_certain_IDs.append(string_states_IDs[i])  
        i += 1  

    # getting the names
    the_certain_names = []
    for each in the_certain_IDs:
        the_certain_names.append(DiagnoserFunctions.GetStateName(each))


    previus_states_uncertain = list()
    for each in the_certain_IDs:
        a = DiagnoserFunctions.GetPrevisousStatesInID(each)
        for k in a:
            b = DiagnoserFunctions.GetStateName(k)
            if DiagnoserFunctions.IsUncertain(b):
                if FU_s_StateNames[string] == b:
                    previus_states_uncertain.append(DiagnoserFunctions.GetStateName(each))
                elif FU_s_StateNames[string] != b and b not in FU_s_StateNames:
                    previus_states_uncertain.append(DiagnoserFunctions.GetStateName(each))            

    FC_s = []
    for each in previus_states_uncertain:
        FC_s.append(DiagnoserFunctions.GetStateId(each))

    return (FC_s)

