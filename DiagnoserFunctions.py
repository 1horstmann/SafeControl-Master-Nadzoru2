import DiagnoserParser
import AutomataParser


def IsUncertain_old(data):
    if len(data) == 7:
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')) and (str(data[6]) == 'N'):
            return (True)
        elif (((str(data[2]) == 'N') or (str(data[3]) == 'N')) and (str(data[6]) == 'F')):
            return (True)
        else:
            return (False)
    elif len(data) == 8:
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')) and ((str(data[6]) == 'N') or (str(data[7]) == 'N')):
            return (True)
        elif (((str(data[2]) == 'N') or (str(data[3]) == 'N')) and ((str(data[6]) == 'F') or (str(data[7]) == 'F'))):
            return (True)
        else:
            return (False)
    elif len(data) == 9:
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')) and (
                (str(data[6]) == 'N') or (str(data[7]) == 'N') or (str(data[8]) == 'N')):
            return (True)
        elif (((str(data[2]) == 'N') or (str(data[3]) == 'N')) and (
                (str(data[6]) == 'F') or (str(data[7]) == 'F') or (str(data[8]) == 'F'))):
            return (True)
        else:
            return (False)
    elif (len(data) <= 11) and ((len(data) >= 10)):
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')) and ((str(data[8]) == 'N') or (str(data[9]) == 'N')):
            return (True)
        elif ((str(data[2]) == 'N') or (str(data[3]) == 'N')) and ((str(data[8]) == 'F') or (str(data[9]) == 'F')):
            return (True)
        elif ((len(data) == 11) and
              ((str(data[2]) == 'N') or (str(data[6]) == 'N')) and ((str(data[6]) == 'F') or (str(data[10]) == 'F'))):
            return (True)
        else:
            return (False)
    elif len(data) >= 12:
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')) and (
                (str(data[9]) == 'N') or (str(data[10]) == 'N') or (str(data[11]) == 'N')):
            return (True)
        elif ((str(data[2]) == 'N') or (str(data[3]) == 'N')) and (
                (str(data[9]) == 'F') or (str(data[10]) == 'F') or (str(data[11]) == 'F')):
            return (True)
        else:
            return (False)
    else:
        return (False)


def IsUncertain(data):
    data = data.upper().replace(" ", "")

    n, f = False, False
    for i in range(len(data)):     
        if (i+1) < len(data):
            if (data[-1] == 'F') or (data[i] == 'F' and data[i+1] == '-') :
                f = True
                
            if (data[i] == 'N' and data[i+1] == ',') or  (data[i] == 'N' and data[i+1] == '-'):
                n = True

    if n and f:
        return True
    else:
        return False


def IsCertain(data):
    if len(data) <= 4:
        if data.__contains__('F'):
            return (True)
        else:
            return (False)
    elif len(data) <= 7:
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')):
            return (True)
        else:
            return (False)
    elif len(data) >= 12:
        if ((str(data[2]) == 'F') or (str(data[3]) == 'F')) and (
                (str(data[9]) == 'F') or (str(data[10]) == 'F') or (str(data[11]) == 'F')):
            return (True)
        else:
            return (False)
    else:
        return (False)


def IsNormal(data):
    data = data.upper()
    for each in data:
        if each == 'F':
            return False
    return True


def IsNotBad(data):
    if len(data) <= 7:
        x1 = len(data) - 1
        x2 = len(data) - 2
        if (str(data[x2]) == 'N') and (str(data[x1]) == 'B'):
            return (True)
        else:
            return (False)
    elif len(data) == 13:
        if (str(data[4] == 'N')) and ((str(data[5])) == 'B') and ((str(data[11])) == 'N') and ((str(data[12])) == 'B'):
            return (True)
        else:
            return (False)
    elif len(data) == 14:
        if (str(data[5] == 'N')) and ((str(data[6])) == 'B') and ((str(data[12])) == 'N') and ((str(data[13])) == 'B'):
            return (True)
        elif (str(data[4] == 'N')) and ((str(data[5])) == 'B') and ((str(data[12])) == 'N') and (
                (str(data[13])) == 'B'):
            return (True)
        else:
            return (False)
    elif len(data) == 15:
        if (str(data[5] == 'N')) and ((str(data[6])) == 'B') and ((str(data[13])) == 'N') and ((str(data[14])) == 'B'):
            return (True)
        else:
            return (False)
    else:
        return (False)


def IsOnlySelfloop(estado): 
    x = len(DiagnoserParser.Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = DiagnoserParser.Transition_Source_Table[n]
        if a == str(estado):
            positions.append(n)

    for each in positions:
        m = int(each)
        target = str(DiagnoserParser.Transition_Target_Table[m])
        if target == estado:
            targets.append(0)
        else:
            targets.append(1)

    if targets.__contains__(1) == True:
        return (0)  # return 0 means that is not only selfloop
    else:
        return (1)  # only selfloop


def GetPosition(name): 
    for n in range(0, len(DiagnoserParser.State_Name_Table)): 
        a = DiagnoserParser.State_Name_Table[n] 
        if a.__contains__(name): 
            return (n) 


def GetPositionId(id): 
    for n in range(0, len(DiagnoserParser.State_Id_Table)): 
        a = DiagnoserParser.State_Id_Table[n] 
        if a.__contains__(id): 
            return (n) 


def GetEventPosition(id): 
    positions = [] 
    for n in range(0, len(DiagnoserParser.Transition_Event_Table)): 
        a = DiagnoserParser.Transition_Event_Table[n] 
        if a == id: 
            positions.append(n) 

    return (positions) 


def GetEventNamePosition(name): 
    for n in range(0, len(DiagnoserParser.Event_Name_Table)):
        a = DiagnoserParser.Event_Name_Table[n]
        if a == name:
            positions = n
            return (positions)


def GetPositionTarget(state_id): 
    positions = []
    for n in range(0, len(DiagnoserParser.Transition_Target_Table)): 
        if str(state_id) == str(DiagnoserParser.Transition_Target_Table[n]): 
            positions.append(n) 

    return (positions) 


def GetPositionSource(state_id): 
    positions = [] 
    for n in range(0, len(DiagnoserParser.Transition_Source_Table)): 
        if str(state_id) == str(DiagnoserParser.Transition_Source_Table[n]): 
            positions.append(n) 

    return (positions) 


def GetNextStatesInID(state): 
    x = len(DiagnoserParser.Transition_Source_Table) 
    positions = [] 
    targets = [] 
    for n in range(0, x): 
        a = str(DiagnoserParser.Transition_Source_Table[n]) 
        if str(state) == a: 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = DiagnoserParser.Transition_Target_Table[m] 
        targets.append(target) 

    return (targets) 


def GetPrevisousStatesInID(state): 
    x = len(DiagnoserParser.Transition_Target_Table) 
    positions = [] 
    sources = [] 
    for n in range(0, x): 
        a = str(DiagnoserParser.Transition_Target_Table[n]) 
        if str(state) == a: 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        source = DiagnoserParser.Transition_Source_Table[m] 
        sources.append(source) 

    return (sources) 


def GetNextStatesInNames(targets):  # enter with return from GetNextStatesInID
    pos = [] 
    names = [] 
    for n in range(0, len(DiagnoserParser.State_Id_Table)): 
        b = DiagnoserParser.State_Id_Table[n] 
        if b == str(targets): 
            pos.append(n) 

    for each in pos: 
        m = int(each) 
        names = DiagnoserParser.State_Name_Table[m] 

    return (names)


def ToDoList(id): 
    vetor1 = [] 
    y = 0 
    for each in DiagnoserParser.Transition_Source_Table: 
        if id == each: 
            vetor1.append(y) 
        y = y + 1 
    return vetor1 


def ToDoTargetList(vetor): 
    vetor2 = [] 
    for each in vetor: 
        next = DiagnoserParser.Transition_Target_Table[each] 
        vetor2.append(next) 
    return (vetor2) 


def ToDoTargetPosition(vetor2): 
    vetor3 = [] 
    for each in vetor2: 
        position = GetPositionId(each) 
        vetor3.append(position) 
    return (vetor3) 


def ToDoStateNames(vetor3): 
    vetor4 = [] 
    for each in vetor3:
        todo = DiagnoserParser.State_Name_Table[each] 
        vetor4.append(todo) 
    return (vetor4) 


def GetTodoTable(position): 
    id = DiagnoserParser.State_Id_Table[position]  
    a = ToDoList(id) 
    b = ToDoTargetList(a) 
    c = ToDoTargetPosition(b) 
    d = ToDoStateNames(c) 
    return (d) 


def GetBS(state): 
    x = len(DiagnoserParser.Transition_Target_Table) - 1 
    positions = [] 
    sources = [] 

    for n in range(0, x):  
        a = DiagnoserParser.Transition_Target_Table[n] 
        if str(a) == str(state): 
            positions.append(n) 

    for each in positions: 
        m = int(each) 
        source = DiagnoserParser.Transition_Source_Table[m] 
        sources.append(source)

    return (sources) 


def EventIsControllable(eventid): 
    event_position = 0 

    for n in range(0, len(DiagnoserParser.Event_Id_Table)): 
        if str(eventid) == str(DiagnoserParser.Event_Id_Table[n]): 
            event_position = n 
    if DiagnoserParser.ControllableTable[event_position] == str(1): 
        return (True) 
    else:
        return (False) 


def EventIsObservable(eventid): 
    n = 0 

    for n in range(0, len(DiagnoserParser.Event_Id_Table)): 
        if str(eventid) == str(DiagnoserParser.Event_Id_Table[n]): 
            event_position = n 

    if DiagnoserParser.ObservableTable[event_position] == str(1): 
        return (True) 
    else:
        return (False) 


def GetBackwardsStatesInID(table): 
    x = len(DiagnoserParser.Transition_Target_Table)  
    positions = [] 
    targets = [] 

    for cada in table: 
        for n in range(0, x): 
            a = DiagnoserParser.Transition_Target_Table[n] 
            if a == str(cada): 
                positions.append(n) 

    for each in positions: 
        m = int(each) 
        target = DiagnoserParser.Transition_Source_Table[m] 
        targets.append(target) 

    return (targets) 


def GetStateId(name): 
    x = 0 
    while x <= ((len(DiagnoserParser.State_Name_Table)) - 1): 
        if name == DiagnoserParser.State_Name_Table[x]:
            return (DiagnoserParser.State_Id_Table[x]) 
        x = x + 1


def GetStateName(id): 
    x = 0 
    while x <= ((len(DiagnoserParser.State_Id_Table)) - 1): 
        if id == DiagnoserParser.State_Id_Table[x]: 
            return (DiagnoserParser.State_Name_Table[x]) 
        x = x + 1 


def GetEventName(id):
    x = 0 
    while x <= ((len(DiagnoserParser.Event_Id_Table)) - 1): 
        if id == DiagnoserParser.Event_Id_Table[x]: 
            return (DiagnoserParser.Event_Name_Table[x]) 
        x = x + 1 


def GetNextState(actual_state, event):  
    source_table = DiagnoserParser.Transition_Source_Table 
    event_table = DiagnoserParser.Transition_Event_Table 
    target_table = DiagnoserParser.Transition_Target_Table 
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


def GetEquivalentDiagEventFromAut(event_id): 
    x = 0 
    while x <= ((len(AutomataParser.Aut_Event_Id_Table)) - 1): 
        if event_id == AutomataParser.Aut_Event_Id_Table[x]: 
            name = AutomataParser.Aut_Event_Name_Table[x] 
            break
        x = x + 1 
    x = 0 
    while x <= ((len(DiagnoserParser.Event_Name_Table)) - 1): 
        if name == DiagnoserParser.Event_Name_Table[x]: 
            ret = DiagnoserParser.Event_Id_Table[x] 
            break 
        x = x + 1 
    return ret 


def GetEquivalentAutEventFromDiag(event_id):  # returns the equivalent diagnoser event for a given automata event
    x = 0 
    while x <= ((len(DiagnoserParser.Event_Name_Table)) - 1): 
        if event_id == DiagnoserParser.Event_Id_Table[x]: 
            name = DiagnoserParser.Event_Name_Table[x] 
            break 
        x = x + 1 
    x = 0 
    while x <= ((len(AutomataParser.Aut_Event_Id_Table)) - 1): 
        if name == AutomataParser.Aut_Event_Name_Table[x]:
            ret = AutomataParser.Aut_Event_Id_Table[x] 
            break 
        x = x + 1 
    return ret 



def GetEventBetween(sourceID, targetID):  # returns direct events between two consecutive states
    events = [] 
    i = 0 
    while i < len(DiagnoserParser.Transition_Source_Table): 
        if (sourceID == DiagnoserParser.Transition_Source_Table[i]
                and targetID == DiagnoserParser.Transition_Target_Table[i]): 
            events.append(DiagnoserParser.Transition_Event_Table[i]) 
        i += 1 
    return events 


