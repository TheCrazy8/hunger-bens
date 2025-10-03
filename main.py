import random
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional

# -----------------------------
# Data Setup
# -----------------------------
# Expanded with ~50 pop culture / media inspired tributes (light parody use).
# Districts assigned cyclically 1-12. Ages are approximate / playful.
dicty: Dict[str, Dict[str, str]] = {
    "trib1": {"name": "Ben", "gender": "male", "age": 16, "district": 1},
    "trib2": {"name": "Ben's Mom", "gender": "female", "age": 45, "district": 2},
    "trib3": {"name": "BenBot 3000", "gender": "object", "age": 2, "district": 3},
    "trib4": {"name": "Ben's Twin", "gender": "male", "age": 16, "district": 1},
    "trib5": {"name": "Ben's Cousin", "gender": "male", "age": 18, "district": 4},
    "trib6": {"name": "Ben's Aunt", "gender": "female", "age": 40, "district": 5},
    "trib7": {"name": "Ben's Uncle", "gender": "male", "age": 42, "district": 6},
    "trib8": {"name": "Eggworth Von Strudenstein", "gender": "male", "age": 30, "district": 7},

    # New tributes (pop culture inspired)
    "trib9": {"name": "Harry Potter", "gender": "male", "age": 17, "district": 8},
    "trib10": {"name": "Hermione Granger", "gender": "female", "age": 17, "district": 9},
    "trib11": {"name": "Ron Weasley", "gender": "male", "age": 17, "district": 10},
    "trib12": {"name": "Katniss Everdeen", "gender": "female", "age": 17, "district": 11},
    "trib13": {"name": "Peeta Mellark", "gender": "male", "age": 17, "district": 12},
    "trib14": {"name": "Frodo Baggins", "gender": "male", "age": 50, "district": 1},
    "trib15": {"name": "Samwise Gamgee", "gender": "male", "age": 38, "district": 2},
    "trib16": {"name": "Gandalf the Grey", "gender": "male", "age": 2019, "district": 3},
    "trib17": {"name": "Aragorn", "gender": "male", "age": 87, "district": 4},
    "trib18": {"name": "Legolas", "gender": "male", "age": 2931, "district": 5},
    "trib19": {"name": "Gimli", "gender": "male", "age": 140, "district": 6},
    "trib20": {"name": "Lara Croft", "gender": "female", "age": 28, "district": 7},
    "trib21": {"name": "Master Chief", "gender": "male", "age": 41, "district": 8},
    "trib22": {"name": "Mario", "gender": "male", "age": 40, "district": 9},
    "trib23": {"name": "Luigi", "gender": "male", "age": 38, "district": 10},
    "trib24": {"name": "Princess Peach", "gender": "female", "age": 25, "district": 11},
    "trib25": {"name": "Link", "gender": "male", "age": 17, "district": 12},
    "trib26": {"name": "Zelda", "gender": "female", "age": 17, "district": 1},
    "trib27": {"name": "Samus Aran", "gender": "female", "age": 32, "district": 2},
    "trib28": {"name": "Solid Snake", "gender": "male", "age": 42, "district": 3},
    "trib29": {"name": "Kratos", "gender": "male", "age": 150, "district": 4},
    "trib30": {"name": "Geralt of Rivia", "gender": "male", "age": 95, "district": 5},
    "trib31": {"name": "Ciri", "gender": "female", "age": 21, "district": 6},
    "trib32": {"name": "Yennefer", "gender": "female", "age": 94, "district": 7},
    "trib33": {"name": "Sherlock Holmes", "gender": "male", "age": 40, "district": 8},
    "trib34": {"name": "Dr. Watson", "gender": "male", "age": 42, "district": 9},
    "trib35": {"name": "Tony Stark", "gender": "male", "age": 48, "district": 10},
    "trib36": {"name": "Steve Rogers", "gender": "male", "age": 102, "district": 11},
    "trib37": {"name": "Bruce Wayne", "gender": "male", "age": 38, "district": 12},
    "trib38": {"name": "Diana Prince", "gender": "female", "age": 5000, "district": 1},
    "trib39": {"name": "Clark Kent", "gender": "male", "age": 35, "district": 2},
    "trib40": {"name": "Peter Parker", "gender": "male", "age": 18, "district": 3},
    "trib41": {"name": "Ellen Ripley", "gender": "female", "age": 35, "district": 4},
    "trib42": {"name": "Sarah Connor", "gender": "female", "age": 33, "district": 5},
    "trib43": {"name": "Neo", "gender": "male", "age": 35, "district": 6},
    "trib44": {"name": "Trinity", "gender": "female", "age": 32, "district": 7},
    "trib45": {"name": "John Wick", "gender": "male", "age": 45, "district": 8},
    "trib46": {"name": "James Bond", "gender": "male", "age": 40, "district": 9},
    "trib47": {"name": "Indiana Jones", "gender": "male", "age": 42, "district": 10},
    "trib48": {"name": "Jack Sparrow", "gender": "male", "age": 39, "district": 11},
    "trib49": {"name": "Obi-Wan Kenobi", "gender": "male", "age": 57, "district": 12},
    "trib50": {"name": "Anakin Skywalker", "gender": "male", "age": 45, "district": 1},
    "trib51": {"name": "Luke Skywalker", "gender": "male", "age": 28, "district": 2},
    "trib52": {"name": "Leia Organa", "gender": "female", "age": 28, "district": 3},
    "trib53": {"name": "Han Solo", "gender": "male", "age": 38, "district": 4},
    "trib54": {"name": "Rey", "gender": "female", "age": 22, "district": 5},
    "trib55": {"name": "Finn", "gender": "male", "age": 24, "district": 6},
    "trib56": {"name": "Chell", "gender": "female", "age": 29, "district": 7},
    "trib57": {"name": "GLaDOS", "gender": "object", "age": 10, "district": 8},
    "trib58": {"name": "Ash Ketchum", "gender": "male", "age": 16, "district": 9},
    "trib59": {"name": "Pikachu", "gender": "object", "age": 7, "district": 10},
    "trib60": {"name": "Sonic the Hedgehog", "gender": "male", "age": 16, "district": 11},
    "trib61": {"name": "Tails", "gender": "male", "age": 8, "district": 12},
    "trib62": {"name": "Donkey Kong", "gender": "male", "age": 25, "district": 1},
    "trib63": {"name": "Kratos Junior", "gender": "male", "age": 12, "district": 2},
    "trib64": {"name": "Geralt Clone", "gender": "male", "age": 3, "district": 3},
    "trib65": {"name": "Portal Companion Cube", "gender": "object", "age": 1, "district": 4},
    "trib66": {"name": "Agent 47", "gender": "male", "age": 45, "district": 5},
    "trib67": {"name": "Chun-Li", "gender": "female", "age": 30, "district": 6},
    "trib68": {"name": "Ryu", "gender": "male", "age": 33, "district": 7},
    "trib69": {"name": "Sam Fisher", "gender": "male", "age": 48, "district": 8},
    "trib70": {"name": "Vault Dweller", "gender": "male", "age": 25, "district": 9},
    "trib71": {"name": "Dragonborn", "gender": "male", "age": 30, "district": 10},
    "trib72": {"name": "Aloy", "gender": "female", "age": 19, "district": 11},
    "trib73": {"name": "Ellie", "gender": "female", "age": 19, "district": 12},
    "trib74": {"name": "Joel", "gender": "male", "age": 52, "district": 1},
    "trib75": {"name": "Nathan Drake", "gender": "male", "age": 34, "district": 2},
    "trib76": {"name": "Commander Shepard", "gender": "female", "age": 32, "district": 3},
    "trib77": {"name": "Gordon Freeman", "gender": "male", "age": 37, "district": 4},
    "trib78": {"name": "Cortana", "gender": "object", "age": 8, "district": 5},
}

def addnomen():
    key = input("Enter a unique key for the tribute (e.g., tribX): ")
    if key in dicty:
        print("Key already exists. Please choose a different key.")
        return addnomen()
    name = input("Enter the tribute's name: ")
    if not name:
        print("Name cannot be empty.")
        return addnomen()
    gender = input("Enter the tribute's gender: ")
    if not gender:
        print("Gender cannot be empty.")
        return addnomen()
    age = input("Enter the tribute's age (number): ")
    if not age.isdigit():
        print("Age must be a number.")
        return addnomen()
    district = input("Enter the tribute's district (number 1-12): ")
    if not district.isdigit():
        print("District must be a number.")
        return addnomen()
    dicty[key] = {"name": name, "gender": gender, "age": int(age), "district": int(district)}
    if input("Add more tributes? (y/n): ").lower() == 'y':
        addnomen()

# -----------------------------
# Models
# -----------------------------
@dataclass
class Tribute:
    key: str
    name: str
    gender: str
    age: int
    district: int
    alive: bool = True
    kills: int = 0
    inventory: List[str] = field(default_factory=list)
    status: List[str] = field(default_factory=list)
    morale: int = 5
    notoriety: int = 0

    def __str__(self):
        status_bits = f" [{','.join(self.status)}]" if self.status else ""
        status = "Alive" if self.alive else "Fallen"
        return f"{self.name} (D{self.district}, {status}, Kills:{self.kills}, Morale:{self.morale}, Notoriety:{self.notoriety}{status_bits})"

    def adjust_morale(self, delta: int):
        self.morale = max(0, min(10, self.morale + delta))

    def add_status(self, tag: str):
        if tag not in self.status:
            self.status.append(tag)

    def remove_status(self, tag: str):
        if tag in self.status:
            self.status.remove(tag)

# -----------------------------
# Weapon / Flavor Configuration
# -----------------------------
WEAPON_VERBS = {
    "fists": "pummels",
    "rock": "bludgeons",
    "stick": "strikes",
    "knife": "slashes",
    "gun": "shoots",
    "bow": "shoots",
    "bow tie": "dazzles",
    "spear": "impales",
    "machete": "cleaves",
    "trident": "skewers",
    "slingshot": "snipes",
    "net": "ensnares",
    "pan": "clonks",
    "frying pan": "clonks",
    "taser": "zaps",
    "rubber chicken": "humiliates",
    "baguette": "wallops",
    "glitter bomb": "bedazzles",
    "garden gnome": "wallops",
    "foam sword": "bonks",
    "chainsaw": "rips",
    "umbrella": "jab-pokes",
    "yo-yo": "whips",
    "fish": "slaps",
    "harpoon": "skewers",
    "boomerang": "returns and whacks",
    "lute": "serenades then whacks",
    "meteor shard": "slices",
}

WEAPONS = set(WEAPON_VERBS.keys()) - {"fists", "rock", "stick"}

CORNUCOPIA_ITEMS = [
    "knife", "gun", "bow", "medical kit", "rope", "canteen", "map", "compass",
    "flashlight", "shield", "spear", "helmet", "machete", "trident", "slingshot",
    "net", "taser", "pan", "frying pan", "chainsaw", "harpoon", "boomerang",
    "rubber chicken", "baguette", "glitter bomb", "garden gnome",
    "foam sword", "umbrella", "yo-yo", "fish", "egg", "lute",
]

SUPPLY_ITEMS = [
    "berries", "egg", "bandages", "water pouch", "protein bar", "energy drink",
    "antidote", "cloak", "snare wire", "fire starter", "sleeping bag", "binoculars",
    "adrenaline shot", "moral support note", "patch kit", "duct tape"
]

HAZARDS = [
    "acid rain", "falling debris", "poison mist", "lava vent", "wild animal",
    "flash flood", "earthquake", "forest fire", "quicksand", "sandstorm",
    "swarm of insects", "toxic spores", "lightning strike", "hail barrage",
    "rogue drone", "mutant vines", "radioactive plume", "hypersonic gust",
    "magnetic storm", "memory fog"
]

HAZARD_EFFECTS = {
    "acid rain": "burned",
    "falling debris": "crushed",
    "poison mist": "poisoned",
    "lava vent": "scorched",
    "wild animal": "mauled",
    "flash flood": "swept away",
    "earthquake": "trampled",
    "forest fire": "burned",
    "quicksand": "engulfed",
    "sandstorm": "buried",
    "swarm of insects": "overwhelmed",
    "toxic spores": "choked",
    "lightning strike": "electrocuted",
    "hail barrage": "bludgeoned",
    "rogue drone": "laser‑tagged fatally",
    "mutant vines": "constricted",
    "radioactive plume": "irradiated",
    "hypersonic gust": "rag-dolled",
    "magnetic storm": "crushed by flying metal",
    "memory fog": "forgot themselves and wandered off",
}

# -----------------------------
# Helpers
# -----------------------------
def _a_or_an(item: str) -> str:
    if item.startswith(("a ", "an ")):
        return item
    article = "an" if item[0].lower() in "aeiou" or item.startswith(("honest", "hour")) else "a"
    return f"{article} {item}"

def _kill(victim: Tribute):
    victim.alive = False
    victim.add_status("fallen")

# -----------------------------
# (Events below are same as enhanced previous version)
# -----------------------------
def event_find_supplies(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    item = rng.choice(SUPPLY_ITEMS + list(WEAPONS))
    t.inventory.append(item)
    t.adjust_morale(+1)
    return [f"{t.name} finds {_a_or_an(item)} and looks pleased."]

def event_small_skirmish(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    winner, loser = (a, b) if rng.random() < 0.5 else (b, a)
    usable = [it for it in winner.inventory if it in WEAPONS]
    weapon = rng.choice(usable) if usable else rng.choice(["fists", "rock", "stick"])
    verb = WEAPON_VERBS.get(weapon, "attacks")
    _kill(loser)
    winner.kills += 1
    winner.notoriety += 1
    winner.adjust_morale(+1)
    with_part = f" with {_a_or_an(weapon)}" if weapon not in ["fists"] else ""
    return [f"{winner.name} {verb} {loser.name}{with_part}. {loser.name} is eliminated."]

def event_trap_failure(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    if rng.random() < 0.18:
        _kill(t)
        return [f"{t.name} tinkers with an over‑complicated trap; a spring snaps and ends their run."]
    t.add_status("frustrated")
    t.adjust_morale(-1)
    return [f"{t.name}'s elaborate trap collapses harmlessly."]

def event_alliance(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    a.adjust_morale(+1); b.adjust_morale(+1)
    return [f"{a.name} and {b.name} form a wary alliance, exchanging nods and snacks."]

def event_environment(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    hazard = rng.choice(HAZARDS)
    effect = HAZARD_EFFECTS[hazard]
    if rng.random() < 0.28:
        _kill(t)
        return [f"{t.name} is {effect} by {hazard}."]
    t.add_status("shaken")
    t.adjust_morale(-1)
    return [f"{t.name} narrowly avoids {hazard}."]

def event_heal(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    heal_items = {"medical kit": 3, "bandages": 2, "antidote": 2, "patch kit": 2, "adrenaline shot": 2}
    present = [i for i in t.inventory if i in heal_items]
    if present:
        use = rng.choice(present)
        t.remove_status("wounded")
        t.adjust_morale(+2)
        return [f"{t.name} uses {use} to patch up and looks revitalized."]
    return [f"{t.name} improvises medical care with leaves. It doesn't help."]

def event_supply_drop(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    available = list(set(WEAPONS).union(SUPPLY_ITEMS))
    crate_items = rng.sample(available, rng.randint(1, 3))
    t.inventory.extend(crate_items)
    t.adjust_morale(+1)
    return [f"A sponsor drone delivers a crate to {t.name}: {', '.join(crate_items)}."]

def event_argument(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    topic = rng.choice([
        "who invented fire first", "proper egg-boiling duration", "ethical glitter deployment",
        "ideal camouflage color", "if morale is real or a construct"
    ])
    a.adjust_morale(-1); b.adjust_morale(-1)
    return [f"{a.name} and {b.name} argue about {topic}. Productivity plummets."]

def event_funny_business(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    gag = rng.choice([
        "holds a motivational seminar for moss", "crowns a log 'Assistant Manager'",
        "practices autograph signatures", "poses heroically to no audience",
        "attempts to train a butterfly", "delivers a monologue about destiny",
        "gives their weapon a pep talk", "trades secrets with a tree",
        "starts a one-tribute parade", "drafts arena bylaws in dirt"
    ])
    return [f"{t.name} {gag}."]

def event_weapon_malfunction(tributes: List[Tribute], rng: random.Random) -> List[str]:
    armed = [t for t in tributes if any(it in WEAPONS for it in t.inventory)]
    if not armed: return []
    t = rng.choice(armed)
    w = rng.choice([it for it in t.inventory if it in WEAPONS])
    if rng.random() < 0.12:
        _kill(t)
        return [f"{t.name}'s {w} misfires catastrophically. {t.name} is eliminated."]
    t.add_status("singed")
    t.adjust_morale(-2)
    return [f"{t.name}'s {w} fizzles embarrassingly, leaving scorch marks."]

def event_scavenger_find(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    find = rng.choice(["abandoned bivouac", "cryptic rune", "half-eaten ration", "rusted locker", "mysterious hatch"])
    item = rng.choice(SUPPLY_ITEMS + list(WEAPONS))
    t.inventory.append(item)
    return [f"{t.name} investigates {find} and acquires {_a_or_an(item)}."]

def event_stealth_fail(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    mishap = rng.choice(["steps on ten twigs at once", "sneezes thunderously", "drops all gear noisily",
                         "laughs at own joke", "waves at a hidden camera"])
    return [f"{t.name} attempts stealth but {mishap}."]

def event_sneak_attack(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2: return []
    attacker, victim = rng.sample(tributes, 2)
    usable = [w for w in attacker.inventory if w in WEAPONS]
    weapon = rng.choice(usable) if usable else None
    if rng.random() < 0.48:
        _kill(victim)
        attacker.kills += 1
        attacker.notoriety += 2
        attacker.adjust_morale(+2)
        if weapon:
            verb = WEAPON_VERBS.get(weapon, "eliminates")
            return [f"{attacker.name} ambushes {victim.name} with {_a_or_an(weapon)} and {verb} them. {victim.name} falls."]
        return [f"{attacker.name} executes a bare-handed ambush on {victim.name}. {victim.name} is eliminated."]
    attacker.adjust_morale(-1)
    return [f"{attacker.name}'s ambush on {victim.name} fails; {attacker.name} retreats."]

def event_dance_off(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    winner = rng.choice([a, b])
    loot = rng.choice(SUPPLY_ITEMS + list(WEAPONS))
    winner.inventory.append(loot)
    winner.adjust_morale(+2)
    return [f"{a.name} and {b.name} stage a sudden dance-off. {winner.name} wins flair rights and pockets {_a_or_an(loot)}."]

def event_meteor_shower(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    if rng.random() < 0.22:
        _kill(t)
        shard = "meteor shard"
        if rng.random() < 0.5:
            alive = [x for x in tributes if x.alive]
            if alive:
                rng.choice(alive).inventory.append(shard)
        return [f"A micro-meteor strikes near {t.name}. {t.name} is vaporized."]
    return [f"{t.name} weaves through incandescent falling debris."]

def event_sponsor_message(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    msg = rng.choice(["TRY HARDER", "STYLE MATTERS", "LOOK WEST", "WE BELIEVE (?)", "STOP WAVING", "EGGS?"])
    t.adjust_morale(+1)
    return [f"A drone beams a hologram at {t.name}: '{msg}'"]

def event_trap_success(tributes: List[Tribute], rng: random.Random) -> List[str]:
    setters = [t for t in tributes if "snare wire" in t.inventory or "net" in t.inventory]
    if not setters or len(tributes) < 2: return []
    trapper = rng.choice(setters)
    targets = [t for t in tributes if t != trapper]
    victim = rng.choice(targets)
    if rng.random() < 0.55:
        _kill(victim)
        trapper.kills += 1
        trapper.notoriety += 1
        return [f"{trapper.name}'s concealed trap snaps and claims {victim.name}."]
    else:
        trapper.adjust_morale(-1)
        return [f"{trapper.name}'s trap is triggered prematurely by {victim.name}, who escapes."]

def event_camouflage(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    t.adjust_morale(+1)
    loot = rng.choice(["berries", "protein bar", "cloak", "bandages"])
    t.inventory.append(loot)
    return [f"{t.name} spends time camouflaging and quietly acquires {loot}."]

def event_reckless_experiment(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    if rng.random() < 0.15:
        _kill(t)
        return [f"{t.name} tests an improvised chemical mixture. It detonates violently."]
    t.add_status("wounded")
    t.adjust_morale(-2)
    return [f"{t.name} experiments with arena flora and suffers minor burns."]

def event_chain_hunt(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 3: return []
    a, b, c = rng.sample(tributes, 3)
    lines = [f"{a.name} chases {b.name}; {b.name} runs into {c.name}. Chaos ensues."]
    r = rng.random()
    if r < 0.33:
        _kill(b); a.kills += 1
        lines.append(f"{a.name} eliminates {b.name} while {c.name} vanishes.")
    elif r < 0.66:
        _kill(a); c.kills += 1
        lines.append(f"{c.name} counters brilliantly and takes down {a.name}; {b.name} escapes.")
    else:
        _kill(c); b.kills += 1
        lines.append(f"{b.name} uses {c.name} as a distraction and eliminates them.")
    return lines

def event_spooked_flock(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    t.adjust_morale(-1)
    return [f"{t.name} startles a flock of metallic birds; the clatter rattles their nerves."]

# Global events
def global_weather_shift(all_tributes: List[Tribute], rng: random.Random) -> List[str]:
    weather = rng.choice(["frigid hail", "sweltering humidity", "dense fog", "glitter drizzle", "electrostatic haze"])
    lines = [f"A sudden arena-wide weather shift blankets the zone in {weather}."]
    for t in all_tributes:
        if not t.alive: continue
        if weather in ["dense fog", "glitter drizzle"] and rng.random() < 0.25:
            t.add_status("disoriented")
            lines.append(f"{t.name} becomes disoriented.")
        if weather == "frigid hail" and rng.random() < 0.15:
            t.add_status("wounded")
            t.adjust_morale(-1)
    return lines

def global_safe_zone_shrink(all_tributes: List[Tribute], rng: random.Random) -> List[str]:
    lines = ["Loud klaxons blare: the safe zone contracts sharply toward the Cornucopia."]
    threatened = [t for t in all_tributes if t.alive and rng.random() < 0.25]
    for t in threatened:
        if rng.random() < 0.40:
            _kill(t)
            lines.append(f"{t.name} is caught outside the new perimeter and collapses.")
        else:
            t.adjust_morale(-1)
            lines.append(f"{t.name} barely sprints inside the perimeter, shaken.")
    return lines

def global_supply_shortage(all_tributes: List[Tribute], rng: random.Random) -> List[str]:
    lines = ["A scarcity protocol triggers: many food caches evaporate in a flash of light."]
    for t in all_tributes:
        if not t.alive: continue
        edible = [i for i in t.inventory if i in ["berries", "protein bar", "egg", "water pouch", "energy drink"]]
        if edible and rng.random() < 0.5:
            lost = rng.choice(edible)
            t.inventory.remove(lost)
            t.adjust_morale(-1)
            lines.append(f"{t.name} loses {lost}.")
    return lines

GLOBAL_EVENTS: List[Callable[[List[Tribute], random.Random], List[str]]] = [
    global_weather_shift,
    global_safe_zone_shrink,
    global_supply_shortage,
]

# Event pools
DAY_EVENTS: List[Callable[[List[Tribute], random.Random], List[str]]] = [
    event_find_supplies, event_small_skirmish, event_trap_failure, event_alliance,
    event_supply_drop, event_argument, event_funny_business, event_scavenger_find,
    event_weapon_malfunction, event_stealth_fail, event_sneak_attack, event_dance_off,
    event_sponsor_message, event_trap_success, event_camouflage, event_reckless_experiment,
    event_chain_hunt, event_spooked_flock,
]

NIGHT_EVENTS: List[Callable[[List[Tribute], random.Random], List[str]]] = [
    event_trap_failure, event_environment, event_small_skirmish, event_heal,
    event_funny_business, event_weapon_malfunction, event_stealth_fail, event_sneak_attack,
    event_meteor_shower, event_sponsor_message, event_trap_success, event_camouflage,
    event_reckless_experiment, event_spooked_flock,
]

# -----------------------------
# Simulator
# -----------------------------
class HungerBensSimulator:
    def __init__(
        self,
        tribute_data: Dict[str, Dict[str, str]],
        seed: Optional[int] = None,
        max_days: int = 50,
        verbose: bool = True,
    ):
        self.rng = random.Random(seed)
        self.max_days = max_days
        self.verbose = verbose
        self.day_count = 0
        self.tributes: List[Tribute] = [
            Tribute(
                key=k,
                name=v["name"],
                gender=v["gender"],
                age=int(v.get("age", 0)),
                district=int(v.get("district", 0)),
            )
            for k, v in tribute_data.items()
        ]
        self.log: List[str] = []
        self._cornucopia_run = False

    def alive_tributes(self) -> List[Tribute]:
        return [t for t in self.tributes if t.alive]

    def run(self):
        self._log_intro()
        self._cornucopia_phase()
        while len(self.alive_tributes()) > 1 and self.day_count < self.max_days:
            self.day_count += 1
            self._simulate_day()
            if len(self.alive_tributes()) <= 1:
                break
            self._simulate_night()
            if self.day_count == 3 and len(self.alive_tributes()) > 4:
                self._feast_event()
        self._announce_winner()
        return self.log

    def _cornucopia_phase(self):
        if self._cornucopia_run: return
        self._cornucopia_run = True
        self._log("--- Cornucopia (Bloodbath) ---")
        tribs = self.alive_tributes()
        self.rng.shuffle(tribs)
        actions_summary: List[str] = []
        engaged = set()

        for t in tribs:
            if not t.alive or t.key in engaged:
                continue
            roll = self.rng.random()
            if roll < 0.30 and len(self.alive_tributes()) > 1:
                opponents = [o for o in self.alive_tributes() if o.key != t.key and o.key not in engaged]
                if opponents:
                    opp = self.rng.choice(opponents)
                    engaged.add(t.key); engaged.add(opp.key)
                    winner, loser = (t, opp) if self.rng.random() < 0.5 else (opp, t)
                    loot = self.rng.choice(CORNUCOPIA_ITEMS)
                    winner.inventory.append(loot)
                    _kill(loser)
                    winner.kills += 1
                    winner.notoriety += 1
                    actions_summary.append(f"{winner.name} overpowers {loser.name} at the Cornucopia and claims {_a_or_an(loot)}.")
                else:
                    item = self.rng.choice(CORNUCOPIA_ITEMS)
                    t.inventory.append(item)
                    actions_summary.append(f"{t.name} hastily grabs {_a_or_an(item)}.")
            elif roll < 0.70:
                grabs = self.rng.randint(1, 3)
                items = self.rng.sample(CORNUCOPIA_ITEMS, grabs)
                t.inventory.extend(items)
                actions_summary.append(f"{t.name} secures {', '.join(items)} before retreating.")
            else:
                actions_summary.append(f"{t.name} flees the Cornucopia empty-handed.")
        for line in actions_summary:
            self._log(line)

        fallen = [t for t in self.tributes if not t.alive]
        if fallen:
            self._log("\nFallen in the Bloodbath:")
            for f in fallen:
                self._log(f" - {f.name}")
                f.__dict__[f"(Fallen logged {f.key})"] = True

    def _feast_event(self):
        self._log("\n=== The Feast is announced! ===")
        participants = [t for t in self.alive_tributes() if self.rng.random() < 0.65]
        if len(participants) < 2:
            self._log("No one risks attending the Feast.")
            return
        self.rng.shuffle(participants)
        loot_pool = SUPPLY_ITEMS + list(WEAPONS)
        for i in range(0, len(participants), 2):
            if i + 1 >= len(participants):
                p = participants[i]
                item = self.rng.choice(loot_pool)
                p.inventory.append(item)
                self._log(f"{p.name} sneaks in late and grabs {_a_or_an(item)} uncontested.")
                continue
            a, b = participants[i], participants[i + 1]
            if not (a.alive and b.alive):
                continue
            if self.rng.random() < 0.55:
                winner, loser = (a, b) if self.rng.random() < 0.5 else (b, a)
                _kill(loser)
                winner.kills += 1
                loot = self.rng.choice(loot_pool)
                winner.inventory.append(loot)
                self._log(f"{winner.name} defeats {loser.name} at the Feast and seizes {_a_or_an(loot)}.")
            else:
                loot_a = self.rng.choice(loot_pool)
                loot_b = self.rng.choice(loot_pool)
                a.inventory.append(loot_a)
                b.inventory.append(loot_b)
                self._log(f"{a.name} and {b.name} snatch {_a_or_an(loot_a)} and {_a_or_an(loot_b)} then disengage.")

    def _simulate_day(self):
        self._log(f"\n--- Day {self.day_count} ---")
        self._run_event_block(DAY_EVENTS, "day")

    def _simulate_night(self):
        self._log(f"\n*** Night {self.day_count} ***")
        self._run_event_block(NIGHT_EVENTS, "night")

    def _maybe_global_event(self):
        if self.rng.random() < 0.30:
            ge = self.rng.choice(GLOBAL_EVENTS)
            lines = ge(self.alive_tributes(), self.rng)
            for l in lines:
                self._log(l)

    def _run_event_block(self, event_pool, phase):
        alive = self.alive_tributes()
        if not alive: return
        events_to_run = min(len(alive), self.rng.randint(3, 6))
        for _ in range(events_to_run):
            alive = self.alive_tributes()
            if len(alive) <= 1: break
            event_func = self.rng.choice(event_pool)
            narrative = event_func(alive, self.rng)
            for line in narrative:
                if line:
                    self._log(line)
        self._maybe_global_event()
        fallen = [t for t in self.tributes if not t.alive and f"(Fallen logged {t.key})" not in t.__dict__]
        if fallen:
            self._log("\nFallen this phase:")
            for f in fallen:
                self._log(f" - {f.name}")
                f.__dict__[f"(Fallen logged {f.key})"] = True

    def _announce_winner(self):
        winners = self.alive_tributes()
        if winners:
            if len(winners) > 1 and self.day_count >= self.max_days:
                self._log("\nARENA FORCED SHUTDOWN: Multiple survivors remain!")
                for w in winners:
                    self._log(f"Survivor: {w.name} (District {w.district}, Kills: {w.kills}, Notoriety:{w.notoriety})")
            else:
                w = winners[0]
                self._log(f"\nVICTOR: {w.name} (District {w.district}, Kills: {w.kills}, Notoriety:{w.notoriety})")
        else:
            self._log("\nNo victor emerged. The arena claims all.")
        self._log("\nFinal standings:")
        for t in sorted(self.tributes, key=lambda x: (-x.alive, -x.kills, -x.notoriety, x.name)):
            self._log(f" - {t}")

    def _log_intro(self):
        self._log("Welcome to the Hunger Bens Simulation (Mega Roster)!")
        self._log(
            f"Total Tributes: {len(self.tributes)}\n"
            "Tributes entering the arena: "
            + ", ".join(f"{t.name} (D{t.district})" for t in self.tributes)
            + "\n"
        )

    def _log(self, message: str):
        self.log.append(message)
        if self.verbose:
            print(message)

# -----------------------------
# Convenience Runner
# -----------------------------
def run_simulation(seed: Optional[int] = None, max_days: int = 30, verbose: bool = True):
    sim = HungerBensSimulator(dicty, seed=seed, max_days=max_days, verbose=verbose)
    sim.run()
    return sim

def askagain():
    while True:
        again = input("Run another simulation? (y/n): ").lower()
        if again == 'y':
            mainloop()
        elif again == 'n':
            break
        else:
            print("Please enter 'y' or 'n'.")
    print("Thank you for using the Hunger Bens Simulator!")

def mainloop():
    seedin = input("Enter a seed (or leave blank for random): ")
    seedin = int(seedin) if seedin.isdigit() else None
    maxday = input("Enter max days (default 30): ")
    maxday = int(maxday) if maxday.isdigit() else 30
    verb = input("Verbose output? (y/n, default y): ").lower() != 'n'
    if input("Add custom tributes? (y/n): ").lower() == 'y':
        addnomen()
    run_simulation(seed=seedin, max_days=maxday, verbose=verb)
    print("\nSimulation complete.")
    print("You can rerun with the same seed for identical results.")
    print(seedin if seedin is not None else "Random seed used.")
    askagain()

if __name__ == "__main__":
    mainloop()