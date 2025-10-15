# Example plugin for Hunger Bens (Windows-only loader)

def get_custom_content():
    return {
        "items": ["mystery snack"],
        "weapons": {"confetti cannon": "stuns"},
        "hazards": {"bubble storm": "slipped"},
    }

# Optional events

def event_bubble_fun(tributes, rng, sim):
    t = rng.choice(tributes)
    t.adjust_morale(+1)
    return [f"{t.name} enjoys a spontaneous bubble storm and feels cheerful."]


def get_events():
    return {
        "day": [event_bubble_fun],
        "night": [],
        "global": [],
    }


def get_event_weights():
    return {event_bubble_fun: 0.6}
