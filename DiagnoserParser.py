from xml.dom.minidom import parse
doc = parse('G_d6.xml')
xml = doc.documentElement

data = xml.getElementsByTagName('data')

for info in data:
    states = info.getElementsByTagName('state')
    events = info.getElementsByTagName('event')
    transitions = info.getElementsByTagName('transition')

State_Id_Table = []
State_Name_Table = []
Event_Id_Table = []
Event_Name_Table = []
Transition_Id_Table = []
Transition_Event_Table = []
Transition_Target_Table = []
Transition_Source_Table = []
ObservableTable = []
ControllableTable = []


for state_id in states:
    if state_id.hasAttribute('id'):
        Id_State = state_id.getAttribute('id')
        State_Id_Table.append(Id_State)

for state_name in states:
    name_state = state_name.getElementsByTagName('name')
    state_name = name_state[0].childNodes[0].data
    State_Name_Table.append(state_name)

for state_initial in states:
    initial_state = state_initial.getElementsByTagName('initial')
    if initial_state:
        Initial_State_ID = state_initial.getAttribute('id')
        break

for event_id in events:
    if event_id.hasAttribute('id'):
        event_table_id = event_id.getAttribute('id')
        Event_Id_Table.append(event_table_id)

for event in events:
    try:
        properties = event.getElementsByTagName("properties")[0]
        if(properties.getElementsByTagName("observable")[0]):
            ObservableTable.append(str(1))
    except:
        ObservableTable.append(str(0))
        pass

for event in events:
    try:
        properties = event.getElementsByTagName("properties")[0]
        if(properties.getElementsByTagName("controllable")[0]):
            ControllableTable.append(str(1))
    except:
        ControllableTable.append(str(0))
        pass

for event_name in events:
    name_event = event_name.getElementsByTagName('name')
    event_table_name = name_event[0].childNodes[0].data
    Event_Name_Table.append(event_table_name)

for transition_id in transitions:
    if transition_id.hasAttribute('id'):
        transition_table_id = transition_id.getAttribute('id')
        Transition_Id_Table.append(transition_table_id)

for transition_event in transitions:
    if transition_event.hasAttribute('event'):
        transition_table_event = transition_event.getAttribute('event')
        Transition_Event_Table.append(transition_table_event)

for transition_target in transitions:
    if transition_target.hasAttribute('target'):
        transition_table_target = transition_target.getAttribute('target')
        Transition_Target_Table.append(transition_table_target)

for transition_source in transitions:
    if transition_source.hasAttribute('source'):
        transition_table_source = transition_source.getAttribute('source')
        Transition_Source_Table.append(transition_table_source)



diag_dict_states = dict()
for i in range(len(State_Name_Table)):
    diag_dict_states[State_Id_Table[i]] = State_Name_Table[i]
print(f'diag_dict_states = {diag_dict_states}')

diag_dict_events = dict()
for i in range(len(Event_Id_Table)):
    diag_dict_events[Event_Id_Table[i]] = Event_Name_Table[i]
print(f'diag_dict_events = {diag_dict_events}')