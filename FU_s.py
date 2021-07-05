import DefineStrings
import AutomataParser
import DiagnoserParser
import AutomataFunctions
import DiagnoserFunctions


def Get_FU_s(): 
    Strings = [] 

    Fault_Events = DefineStrings.GetFaultEventsPosition()
    
    for each in Fault_Events: 
        y = DefineStrings.GetString(each) 
        for i in range(0, len(y)):
            Strings.append(y[i]) 

    i = 0 
    Diag_Event_ID = [] 
    while i < len(Strings): 
        diag_event_id = [] 
        for each in Strings[i]: 
            event_id = each 
            n = AutomataFunctions.GetEventPosition(event_id) 
            aut_event_name = AutomataParser.Aut_Event_Name_Table[n] 
            for diag_event_name in DiagnoserParser.Event_Name_Table: 
                if aut_event_name == diag_event_name: 
                    n = DiagnoserParser.Event_Name_Table.index(diag_event_name) 
                    diag_event_id.append(DiagnoserParser.Event_Id_Table[n]) 
                    break
        Diag_Event_ID.append(diag_event_id) 
        i += 1

    FU_s = [] 
    i = 0 
    while i < len(Diag_Event_ID): 
        # starting from initial state:
        actual_state = DiagnoserParser.Initial_State_ID 
        for each in Diag_Event_ID[i]: 
            n = 0 
            while n < len(DiagnoserParser.Transition_Event_Table): 
                if (each == DiagnoserParser.Transition_Event_Table[n] 
                        and actual_state == DiagnoserParser.Transition_Source_Table[n]): 
                    actual_state = DiagnoserParser.Transition_Target_Table[n] 
                    break 
                n += 1 
        actual_state_name = DiagnoserFunctions.GetStateName(actual_state)

        if DiagnoserFunctions.IsUncertain(actual_state_name):  # just to be sure
            FU_s.append(actual_state_name) 
        i += 1  

    return FU_s 


def GetUfsInId(state): 
    n = 0 
    for each in DiagnoserParser.State_Name_Table: 
        if state == each: 
            return(DiagnoserParser.State_Id_Table[n]) 
        n = n + 1 


def GetStringPath():
    Strings = [] 

    Fault_Events = DefineStrings.GetFaultEventsPosition() 

    for n, each in enumerate(Fault_Events): 
        y = DefineStrings.GetString(each) 

        if n == 0:
            Strings.append(y) 
        elif y != Strings[n-1]:
            Strings.append(y) 



    return(Strings) 

