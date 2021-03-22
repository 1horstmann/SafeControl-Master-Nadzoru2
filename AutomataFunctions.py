import AutomataParser


def GetPosition(id): 
    for n in range(0, len(AutomataParser.Aut_State_Id_Table)):  
        a = AutomataParser.Aut_State_Id_Table[n]  
        if a == id:  
            return (int(n))


def GetEventPosition(id):  
    for n in range(0, len(AutomataParser.Aut_Event_Id_Table)):  
        a = AutomataParser.Aut_Event_Id_Table[n]  
        if a == id:  
            positions = n  
            return (positions)  


def GetEventNamePosition(name):
    for n in range(0, len(AutomataParser.Aut_Event_Name_Table)): 
        a = AutomataParser.Aut_Event_Name_Table[n] 
        if a == name: 
            positions = n  
            return (positions) 


def GetFaultEvent():
    Fault_Event = [] 
    n = 0 
    for each in AutomataParser.Aut_Event_Id_Table: 
        if AutomataParser.Aut_ObservableTable[n] == str(0): 
            Fault_Event = each 
        n = n + 1 
    return (Fault_Event) 


def GetFaultEventName(): 
    i = 0 
    while i < len(AutomataParser.Aut_Event_Id_Table): 
        if AutomataParser.Aut_Event_Id_Table[i] == GetFaultEvent(): 
            return (AutomataParser.Aut_Event_Name_Table[i]) 
        i += 1 


def IsSelfloopOnly(estado): 
    x = len(AutomataParser.Aut_Transition_Source_Table) 
    positions = []
    targets = [] 

    for n in range(0, x): 
        a = AutomataParser.Aut_Transition_Source_Table[n] 
        if a == str(estado): 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = str(AutomataParser.Aut_Transition_Target_Table[m]) 
        if target == estado: 
            targets.append(0) 
        else:
            targets.append(1) 

    if targets.__contains__(1) == True: 
        return (0)  
    else:
        return (1)  


def GetEventBetween(sourceID, targetID):  
    events = [] 
    i = 0
    while i < len(AutomataParser.Aut_Transition_Source_Table): 
        if (sourceID == AutomataParser.Aut_Transition_Source_Table[i] 
                and targetID == AutomataParser.Aut_Transition_Target_Table[i]): 
            events.append(AutomataParser.Aut_Transition_Event_Table[i]) 
        i += 1 
    return events 


def GetNextStatesInID(state): 
    x = len(AutomataParser.Aut_Transition_Source_Table) 
    positions = [] 
    targets = [] 
    for n in range(0, x): 
        a = str(AutomataParser.Aut_Transition_Source_Table[n]) 
        if str(state) == a: 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = AutomataParser.Aut_Transition_Target_Table[m] 
        targets.append(target) 

    return (targets) 


def GetEventName(id):
    x = 0 
    while x <= ((len(AutomataParser.Aut_Event_Id_Table)) - 1): 
        if id == AutomataParser.Aut_Event_Id_Table[x]:
            return (AutomataParser.Aut_Event_Name_Table[x]) 
        x = x + 1 


def GetNextState(actual_state, event):  # gets the next state for a given state and event
    source_table = AutomataParser.Aut_Transition_Source_Table 
    event_table = AutomataParser.Aut_Transition_Event_Table 
    target_table = AutomataParser.Aut_Transition_Target_Table 
    size = len(source_table) 
    i = 0 
    found = False 
    while i < size: 
        if (source_table[i] == actual_state) and (event_table[i] == event): 
            ret = target_table[i]
            found = True 
            break 
        i += 1 

    if found: 
        return ret 
    else: 
        return [] 