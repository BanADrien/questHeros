# events.py

# Dictionnaire global contenant les listeners
_events = {
    "deal_damage": [],
    "take_damage": [],
    "deal_damage_taken": [],
    "obtention_item": [],
    "start_turn": [],
    "end_turn": []
}

def register(event_name, func):
    if event_name not in _events:
        raise ValueError(f"Événement inconnu : {event_name}")
    _events[event_name].append(func)

def trigger(event_name, *args, **kwargs):
    if event_name not in _events:
        raise ValueError(f"Événement inconnu : {event_name}")
    
    for func in list(_events[event_name]):
        func(*args, **kwargs)
