import random
import json
import sys
import argparse
import os
import importlib.util
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Callable, Optional, Set, Tuple, Any
from datetime import datetime
def tryimporttheme():
    try: import sv_ttk
    except ImportError: 
        os.system("pip install sv_ttk")
        if os.system("pip install sv_ttk") == 1: # if installed successfully
            # Check if GUI was initially requested
            if "--gui" in sys.argv:
                os.system("python main.py --gui")
            else:
                os.system("python main.py")
            os._exit(0)
        else: # if failed to install
            tryimporttheme()

if os.name == "nt":
    import tkinter
    import tkinter.ttk as ttk
    from tkinter import scrolledtext, messagebox, filedialog
    tryimporttheme()
    import sv_ttk
else:
    pass

# -----------------------------
# Persistent Config (plugins, etc.)
# -----------------------------
_CONFIG: Dict[str, Any] = {}

def _default_plugins_enabled() -> bool:
    return os.name == 'nt'

def get_config_path() -> str:
    # Prefer user roaming AppData on Windows; fallback to local file next to script
    if os.name == 'nt':
        base = os.environ.get('APPDATA') or os.environ.get('LOCALAPPDATA')
        if base:
            cfg_dir = os.path.join(base, 'HungerBens')
            try:
                os.makedirs(cfg_dir, exist_ok=True)
            except Exception:
                pass
            return os.path.join(cfg_dir, 'config.json')
    # Non-Windows or no appdata: store beside script
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, 'config.json')

def load_config() -> Dict[str, Any]:
    cfg = {"plugins_enabled": _default_plugins_enabled()}
    path = get_config_path()
    try:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    cfg.update(data)
    except Exception:
        # Ignore and use defaults
        pass
    return cfg

def save_config(cfg: Dict[str, Any]):
    try:
        path = get_config_path()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        # Best-effort only
        pass

# Initialize config cache
_CONFIG = load_config()
# Ensure the config file exists on first run by persisting defaults
try:
    save_config(_CONFIG)
except Exception:
    pass

# -----------------------------
# Base Tribute Data (can be replaced/extended by JSON roster)
# -----------------------------
dicty: Dict[str, Dict[str, Any]] = {
    "trib1": {"name": "Ben", "gender": "male", "age": 16, "district": 1},
    "trib2": {"name": "Ben's Mom", "gender": "female", "age": 45, "district": 2},
    "trib3": {"name": "BenBot 3000", "gender": "object", "age": 2, "district": 3},
    "trib4": {"name": "Ben's Twin", "gender": "male", "age": 16, "district": 1},
    # (Truncated comment: All original tributes retained below)
    "trib5": {"name": "Ben's Cousin", "gender": "male", "age": 18, "district": 4},
    "trib6": {"name": "Ben's Aunt", "gender": "female", "age": 40, "district": 5},
    "trib7": {"name": "Ben's Uncle", "gender": "male", "age": 42, "district": 6},
    "trib8": {"name": "Eggworth Von Strudenstein", "gender": "male", "age": 30, "district": 7},
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

# -----------------------------
# Weapons / Items / Hazards (original lists preserved)
# -----------------------------
WEAPON_VERBS = {
    "fists": "pummels", "rock": "bludgeons", "stick": "strikes", "knife": "slashes",
    "gun": "shoots", "bow": "shoots", "bow tie": "dazzles", "spear": "impales",
    "machete": "cleaves", "trident": "skewers", "slingshot": "snipes", "net": "ensnares",
    "pan": "clonks", "frying pan": "clonks", "taser": "zaps", "rubber chicken": "humiliates",
    "baguette": "wallops", "glitter bomb": "bedazzles", "garden gnome": "wallops",
    "foam sword": "bonks", "chainsaw": "rips", "umbrella": "jab-pokes", "yo-yo": "whips",
    "fish": "slaps", "harpoon": "skewers", "boomerang": "returns and whacks",
    "lute": "serenades then whacks", "meteor shard": "slices",
}
WEAPONS = set(WEAPON_VERBS.keys()) - {"fists", "rock", "stick"}
CORNUCOPIA_ITEMS = [
    "knife","gun","bow","medical kit","rope","canteen","map","compass",
    "flashlight","shield","spear","helmet","machete","trident","slingshot",
    "net","taser","pan","frying pan","chainsaw","harpoon","boomerang",
    "rubber chicken","baguette","glitter bomb","garden gnome",
    "foam sword","umbrella","yo-yo","fish","egg","lute",
]
SUPPLY_ITEMS = [
    "berries","egg","bandages","water pouch","protein bar","energy drink",
    "antidote","cloak","snare wire","fire starter","sleeping bag","binoculars",
    "adrenaline shot","moral support note","patch kit","duct tape"
]
HAZARDS = [
    "acid rain","falling debris","poison mist","lava vent","wild animal",
    "flash flood","earthquake","forest fire","quicksand","sandstorm",
    "swarm of insects","toxic spores","lightning strike","hail barrage",
    "rogue drone","mutant vines","radioactive plume","hypersonic gust",
    "magnetic storm","memory fog"
]
HAZARD_EFFECTS = {
    "acid rain":"burned","falling debris":"crushed","poison mist":"poisoned","lava vent":"scorched",
    "wild animal":"mauled","flash flood":"swept away","earthquake":"trampled","forest fire":"burned",
    "quicksand":"engulfed","sandstorm":"buried","swarm of insects":"overwhelmed","toxic spores":"choked",
    "lightning strike":"electrocuted","hail barrage":"bludgeoned","rogue drone":"laser‑tagged fatally",
    "mutant vines":"constricted","radioactive plume":"irradiated","hypersonic gust":"rag-dolled",
    "magnetic storm":"crushed by flying metal","memory fog":"forgot themselves and wandered off",
}

# -----------------------------
# Utility helpers
# -----------------------------
def _a_or_an(item: str) -> str:
    if item.startswith(("a ", "an ")):
        return item
    article = "an" if item[0].lower() in "aeiou" or item.startswith(("honest", "hour")) else "a"
    return f"{article} {item}"

# -----------------------------
# Status Variant System (adds descriptive variety)
# -----------------------------
# Certain status tags (non-critical ones) now have variant synonyms for flavor.
# We maintain a mapping of a canonical base tag to its possible variants. Critical tags
# like 'fallen' and 'wounded' remain unchanged for programmatic clarity.
STATUS_VARIANTS: Dict[str, List[str]] = {
    "frustrated": ["frustrated", "exasperated", "annoyed", "irritated"],
    "shaken": ["shaken", "rattled", "unnerved", "disturbed"],
    "singed": ["singed", "scorched", "charred"],
    "disoriented": ["disoriented", "confused", "dazed", "lost"],
}

VARIANT_LOOKUP: Dict[str, str] = {variant: base for base, arr in STATUS_VARIANTS.items() for variant in arr}

def add_status_variant(t: "Tribute", base_tag: str, rng: random.Random):
    """Add a status variant for the given base tag.

    - If the base tag has variants and the tribute does not already possess ANY variant
      from that group, choose one randomly.
    - If the tribute already has one variant from the group, do nothing (avoid clutter).
    - If the base tag has no variants registered, fall back to normal add_status.
    """
    variants = STATUS_VARIANTS.get(base_tag)
    if not variants:
        t.add_status(base_tag)
        return
    if any(v in t.status for v in variants):  # already has a variant of this group
        return
    choice = rng.choice(variants)
    t.add_status(choice)

# -----------------------------
# Data Models
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
    cause_of_death: Optional[str] = None

    def __str__(self):
        status_bits = f" [{','.join(self.status)}]" if self.status else ""
        status = "Alive" if self.alive else f"Fallen ({self.cause_of_death or 'unknown'})"
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
# Alliance tracking
# -----------------------------
class AllianceManager:
    def __init__(self):
        # Each alliance is a frozenset of tribute keys
        self.alliances: Set[frozenset[str]] = set()

    def form_alliance(self, a: Tribute, b: Tribute):
        if not a.alive or not b.alive or a.key == b.key:
            return
        # Merge if they already are indirectly connected
        existing = [al for al in self.alliances if a.key in al or b.key in al]
        group = {a.key, b.key}
        for al in existing:
            if group & set(al):
                group |= set(al)
                self.alliances.remove(al)
        self.alliances.add(frozenset(group))

    def breakup(self, tkeys: List[str]):
        to_remove = []
        for al in self.alliances:
            if any(k in al for k in tkeys):
                to_remove.append(al)
        for al in to_remove:
            self.alliances.remove(al)

    def members_of(self, tribute: Tribute) -> Set[str]:
        for al in self.alliances:
            if tribute.key in al:
                return set(al)
        return set()

    def is_allied(self, a: Tribute, b: Tribute) -> bool:
        if a.key == b.key:
            return True
        return any(a.key in al and b.key in al for al in self.alliances)

    def remove_dead(self, tributes: List[Tribute]):
        alive_keys = {t.key for t in tributes if t.alive}
        updated = set()
        for al in self.alliances:
            trimmed = al & alive_keys
            if len(trimmed) >= 2:
                updated.add(frozenset(trimmed))
        self.alliances = updated

    def to_dict(self):
        return [list(al) for al in self.alliances]

# -----------------------------
# Kill / death utility
# -----------------------------
def _kill(victim: Tribute, cause: str):
    victim.alive = False
    victim.add_status("fallen")
    victim.cause_of_death = cause

# ============================= EVENTS =============================
# Original event functions updated minimally to integrate new morale / notoriety dynamics.
# Some new events appended for alliance mechanics.

def event_find_supplies(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    item = rng.choice(SUPPLY_ITEMS + list(WEAPONS))
    t.inventory.append(item)
    t.adjust_morale(+1)
    if t.notoriety > 5 and rng.random() < 0.15:
        t.adjust_morale(+1)
        return [f"{t.name} finds {_a_or_an(item)}; sponsors applaud their infamous flair."]
    return [f"{t.name} finds {_a_or_an(item)} and looks pleased."]

def event_small_skirmish(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    if len(tributes) < 2: return []
    # Weighted targeting: higher notoriety more likely to be attacked
    weights = []
    for t in tributes:
        weights.append(1 + t.notoriety * 0.4)
    a = rng.choices(tributes, weights=weights, k=1)[0]
    b_candidates = [t for t in tributes if t != a]
    b = rng.choice(b_candidates)
    # Allies less likely to attack unless betrayal check triggers
    if sim.alliances.is_allied(a, b) and rng.random() < 0.75:
        return [f"{a.name} and {b.name} square up but recall their alliance and back off."]
    # Morale modifies success
    prob_a = 0.5 + (a.morale - b.morale) * 0.04
    prob_a = max(0.1, min(0.9, prob_a))
    winner, loser = (a, b) if rng.random() < prob_a else (b, a)
    usable = [it for it in winner.inventory if it in WEAPONS]
    weapon = rng.choice(usable) if usable else rng.choice(["fists", "rock", "stick"])
    verb = WEAPON_VERBS.get(weapon, "attacks")
    _kill(loser, f"defeated by {winner.name} ({weapon})")
    winner.kills += 1
    winner.notoriety += 1 + (1 if weapon in WEAPONS else 0)
    winner.adjust_morale(+1)
    with_part = f" with {_a_or_an(weapon)}" if weapon not in ["fists"] else ""
    return [f"{winner.name} {verb} {loser.name}{with_part}. {loser.name} is eliminated."]

def event_trap_failure(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    base = 0.18
    base -= (t.morale - 5) * 0.01  # morale reduces failure
    if rng.random() < base:
        _kill(t, "botched trap")
        return [f"{t.name} tinkers with an over‑complicated trap; a spring snaps and ends their run."]
    add_status_variant(t, "frustrated", rng)
    t.adjust_morale(-1)
    return [f"{t.name}'s elaborate trap collapses harmlessly."]

def event_alliance(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    if sim.alliances.is_allied(a, b):
        return [f"{a.name} and {b.name} reaffirm their alliance over shared rations."]
    sim.alliances.form_alliance(a, b)
    a.adjust_morale(+1); b.adjust_morale(+1)
    return [f"{a.name} and {b.name} form a wary alliance, exchanging nods and snacks."]

def event_environment(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    hazard = rng.choice(HAZARDS)
    effect = HAZARD_EFFECTS[hazard]
    chance = 0.28 - (t.morale - 5) * 0.015
    if rng.random() < chance:
        _kill(t, f"{effect} by {hazard}")
        return [f"{t.name} is {effect} by {hazard}."]
    add_status_variant(t, "shaken", rng)
    t.adjust_morale(-1)
    return [f"{t.name} narrowly avoids {hazard}."]

def event_heal(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    heal_items = {"medical kit": 3, "bandages": 2, "antidote": 2, "patch kit": 2, "adrenaline shot": 2}
    present = [i for i in t.inventory if i in heal_items]
    if present:
        use = rng.choice(present)
        if "wounded" in t.status:
            t.remove_status("wounded")
        t.adjust_morale(+2)
        return [f"{t.name} uses {use} to patch up and looks revitalized."]
    return [f"{t.name} improvises medical care with leaves. It doesn't help."]

def event_supply_drop(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    available = list(set(WEAPONS).union(SUPPLY_ITEMS))
    crate_items = rng.sample(available, rng.randint(1, 3))
    t.inventory.extend(crate_items)
    t.adjust_morale(+1)
    if t.notoriety > 6:
        bonus = rng.choice(available)
        t.inventory.append(bonus)
        return [f"A sponsor drone delivers a premium crate to {t.name}: {', '.join(crate_items+[bonus])}."]
    return [f"A sponsor drone delivers a crate to {t.name}: {', '.join(crate_items)}."]

def event_argument(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    topic = rng.choice([
        "who invented fire first","proper egg-boiling duration","ethical glitter deployment",
        "ideal camouflage color","if morale is real or a construct"
    ])
    a.adjust_morale(-1); b.adjust_morale(-1)
    # Chance of alliance fracture
    fractured = False
    if sim.alliances.is_allied(a, b) and rng.random() < 0.25:
        sim.alliances.breakup([a.key, b.key])
        fractured = True
    line = f"{a.name} and {b.name} argue about {topic}. Productivity plummets."
    if fractured:
        line += " Their alliance fractures."
    return [line]

def event_funny_business(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    gag = rng.choice([
        "holds a motivational seminar for moss","crowns a log 'Assistant Manager'",
        "practices autograph signatures","poses heroically to no audience",
        "attempts to train a butterfly","delivers a monologue about destiny",
        "gives their weapon a pep talk","trades secrets with a tree",
        "starts a one-tribute parade","drafts arena bylaws in dirt"
    ])
    if t.morale < 4 and rng.random() < 0.4:
        t.adjust_morale(+2)
        return [f"{t.name} {gag}. It oddly lifts their spirits."]
    return [f"{t.name} {gag}."]

def event_weapon_malfunction(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    armed = [t for t in tributes if any(it in WEAPONS for it in t.inventory)]
    if not armed: return []
    t = rng.choice(armed)
    w = rng.choice([it for it in t.inventory if it in WEAPONS])
    base = 0.12 + (t.notoriety * 0.01)  # flashy gear risk
    if rng.random() < base:
        _kill(t, f"{w} malfunction")
        return [f"{t.name}'s {w} misfires catastrophically. {t.name} is eliminated."]
    add_status_variant(t, "singed", rng)
    t.adjust_morale(-2)
    return [f"{t.name}'s {w} fizzles embarrassingly, leaving scorch marks."]

def event_scavenger_find(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    find = rng.choice(["abandoned bivouac","cryptic rune","half-eaten ration","rusted locker","mysterious hatch"])
    item = rng.choice(SUPPLY_ITEMS + list(WEAPONS))
    t.inventory.append(item)
    return [f"{t.name} investigates {find} and acquires {_a_or_an(item)}."]

def event_stealth_fail(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    mishap = rng.choice(["steps on ten twigs at once","sneezes thunderously","drops all gear noisily",
                         "laughs at own joke","waves at a hidden camera"])
    t.adjust_morale(-1)
    return [f"{t.name} attempts stealth but {mishap}."]

def event_sneak_attack(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    if len(tributes) < 2: return []
    attacker, victim = rng.sample(tributes, 2)
    if sim.alliances.is_allied(attacker, victim) and rng.random() < 0.8:
        return [f"{attacker.name} considers ambushing ally {victim.name} but hesitates."]
    usable = [w for w in attacker.inventory if w in WEAPONS]
    weapon = rng.choice(usable) if usable else None
    base = 0.48 + (attacker.morale - 5) * 0.04
    base = max(0.2, min(0.85, base))
    if rng.random() < base:
        _kill(victim, f"ambushed by {attacker.name}")
        attacker.kills += 1
        attacker.notoriety += 2
        attacker.adjust_morale(+2)
        if weapon:
            verb = WEAPON_VERBS.get(weapon, "eliminates")
            return [f"{attacker.name} ambushes {victim.name} with {_a_or_an(weapon)} and {verb} them. {victim.name} falls."]
        return [f"{attacker.name} executes a bare-handed ambush on {victim.name}. {victim.name} is eliminated."]
    attacker.adjust_morale(-1)
    return [f"{attacker.name}'s ambush on {victim.name} fails; {attacker.name} retreats."]

def event_dance_off(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    if len(tributes) < 2: return []
    a, b = rng.sample(tributes, 2)
    winner = rng.choice([a, b])
    loot = rng.choice(SUPPLY_ITEMS + list(WEAPONS))
    winner.inventory.append(loot)
    winner.adjust_morale(+2)
    return [f"{a.name} and {b.name} stage a sudden dance-off. {winner.name} wins flair rights and pockets {_a_or_an(loot)}."]

def event_meteor_shower(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    chance = 0.22 - (t.morale - 5)*0.01
    if rng.random() < chance:
        _kill(t, "micro-meteor strike")
        shard = "meteor shard"
        alive = [x for x in tributes if x.alive]
        if alive and rng.random() < 0.5:
            rng.choice(alive).inventory.append(shard)
        return [f"A micro-meteor strikes near {t.name}. {t.name} is vaporized."]
    return [f"{t.name} weaves through incandescent falling debris."]

def event_sponsor_message(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    msgs = ["TRY HARDER","STYLE MATTERS","LOOK WEST","WE BELIEVE (?)","STOP WAVING","EGGS?"]
    if t.notoriety > 5:
        msgs += ["INFAMY SELLS","KEEP THE DRAMA COMING"]
    msg = rng.choice(msgs)
    t.adjust_morale(+1)
    return [f"A drone beams a hologram at {t.name}: '{msg}'"]

def event_trap_success(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    setters = [t for t in tributes if "snare wire" in t.inventory or "net" in t.inventory]
    if not setters or len(tributes) < 2: return []
    trapper = rng.choice(setters)
    targets = [t for t in tributes if t != trapper]
    victim = rng.choice(targets)
    if sim.alliances.is_allied(trapper, victim) and rng.random() < 0.6:
        return [f"{trapper.name}'s trap nearly snares ally {victim.name}; they reset it carefully."]
    chance = 0.55 + (trapper.morale - 5)*0.02
    if random.random() < chance:
        _kill(victim, f"trap set by {trapper.name}")
        trapper.kills += 1
        trapper.notoriety += 1
        return [f"{trapper.name}'s concealed trap snaps and claims {victim.name}."]
    else:
        trapper.adjust_morale(-1)
        return [f"{trapper.name}'s trap is triggered prematurely by {victim.name}, who escapes."]

def event_camouflage(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    t.adjust_morale(+1)
    loot = rng.choice(["berries","protein bar","cloak","bandages"])
    t.inventory.append(loot)
    return [f"{t.name} spends time camouflaging and quietly acquires {loot}."]

def event_reckless_experiment(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    chance = 0.15 - (t.morale - 5)*0.01
    if rng.random() < chance:
        _kill(t, "chemical experiment explosion")
        return [f"{t.name} tests an improvised chemical mixture. It detonates violently."]
    t.add_status("wounded")
    t.adjust_morale(-2)
    return [f"{t.name} experiments with arena flora and suffers minor burns."]

def event_chain_hunt(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    if len(tributes) < 3: return []
    a, b, c = rng.sample(tributes, 3)
    lines = [f"{a.name} chases {b.name}; {b.name} runs into {c.name}. Chaos ensues."]
    r = rng.random()
    if r < 0.33:
        _kill(b, f"eliminated in chain hunt by {a.name}")
        a.kills += 1
        lines.append(f"{a.name} eliminates {b.name} while {c.name} vanishes.")
    elif r < 0.66:
        _kill(a, f"countered by {c.name}")
        c.kills += 1
        lines.append(f"{c.name} counters brilliantly and takes down {a.name}; {b.name} escapes.")
    else:
        _kill(c, f"used as distraction by {b.name}")
        b.kills += 1
        lines.append(f"{b.name} uses {c.name} as a distraction and eliminates them.")
    return lines

def event_spooked_flock(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    t = rng.choice(tributes)
    t.adjust_morale(-1)
    return [f"{t.name} startles a flock of metallic birds; the clatter rattles their nerves."]

# New alliance-centric events
def event_alliance_aid(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    allied_groups = [al for al in sim.alliances.alliances if len(al) >= 2]
    if not allied_groups: return []
    group = rng.choice(list(allied_groups))
    members = [t for t in tributes if t.key in group]
    if not members: return []
    helper = rng.choice(members)
    receiver_candidates = [m for m in members if m != helper]
    if not receiver_candidates: return []
    receiver = rng.choice(receiver_candidates)
    item = rng.choice(SUPPLY_ITEMS)
    receiver.inventory.append(item)
    helper.adjust_morale(+1); receiver.adjust_morale(+1)
    return [f"{helper.name} shares {item} with ally {receiver.name}; their cohesion strengthens."]

def event_alliance_betrayal(tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    # Low chance betrayal
    if len(sim.alliances.alliances) == 0: return []
    if rng.random() > 0.25: return []
    group = rng.choice(list(sim.alliances.alliances))
    if len(group) < 2: return []
    keys = list(group)
    attacker_key, victim_key = rng.sample(keys, 2)
    attacker = next(t for t in tributes if t.key == attacker_key)
    victim = next(t for t in tributes if t.key == victim_key)
    prob = 0.5 + (attacker.morale - victim.morale)*0.05
    prob = max(0.2, min(0.85, prob))
    if rng.random() < prob:
        _kill(victim, f"betrayed by {attacker.name}")
        attacker.kills += 1
        attacker.notoriety += 3
        sim.alliances.breakup([attacker.key, victim.key])
        return [f"Betrayal! {attacker.name} turns on ally {victim.name}, eliminating them."]
    attacker.adjust_morale(-2)
    sim.alliances.breakup([attacker.key, victim.key])
    return [f"{attacker.name} attempts to betray {victim.name} but fails; the alliance dissolves in distrust."]

# ============================= GLOBAL EVENTS =============================
def global_weather_shift(all_tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    weather = rng.choice(["frigid hail","sweltering humidity","dense fog","glitter drizzle","electrostatic haze"])
    lines = [f"A sudden arena-wide weather shift blankets the zone in {weather}."]
    for t in all_tributes:
        if not t.alive: continue
        if weather in ["dense fog","glitter drizzle"] and rng.random() < 0.25:
            add_status_variant(t, "disoriented", rng)
            lines.append(f"{t.name} becomes disoriented.")
        if weather == "frigid hail" and rng.random() < 0.15:
            t.add_status("wounded")
            t.adjust_morale(-1)
    return lines

def global_safe_zone_shrink(all_tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    lines = ["Loud klaxons blare: the safe zone contracts sharply toward the Cornucopia."]
    threatened = [t for t in all_tributes if t.alive and rng.random() < 0.25]
    for t in threatened:
        if rng.random() < 0.40 - (t.morale - 5)*0.02:
            _kill(t, "caught outside perimeter")
            lines.append(f"{t.name} is caught outside the new perimeter and collapses.")
        else:
            t.adjust_morale(-1)
            lines.append(f"{t.name} barely sprints inside the perimeter, shaken.")
    return lines

def global_supply_shortage(all_tributes: List[Tribute], rng: random.Random, sim) -> List[str]:
    lines = ["A scarcity protocol triggers: many food caches evaporate in a flash of light."]
    for t in all_tributes:
        if not t.alive: continue
        edible = [i for i in t.inventory if i in ["berries","protein bar","egg","water pouch","energy drink"]]
        if edible and rng.random() < 0.5:
            lost = rng.choice(edible)
            t.inventory.remove(lost)
            t.adjust_morale(-1)
            lines.append(f"{t.name} loses {lost}.")
    return lines

GLOBAL_EVENTS: List[Callable[[List[Tribute], random.Random, "HungerBensSimulator"], List[str]]] = [
    global_weather_shift,
    global_safe_zone_shrink,
    global_supply_shortage,
]

# Event pools (call signatures now expect sim)
DAY_EVENTS: List[Callable[[List[Tribute], random.Random, "HungerBensSimulator"], List[str]]] = [
    event_find_supplies, event_small_skirmish, event_trap_failure, event_alliance,
    event_supply_drop, event_argument, event_funny_business, event_scavenger_find,
    event_weapon_malfunction, event_stealth_fail, event_sneak_attack, event_dance_off,
    event_sponsor_message, event_trap_success, event_camouflage, event_reckless_experiment,
    event_chain_hunt, event_spooked_flock, event_alliance_aid, event_alliance_betrayal
]

NIGHT_EVENTS: List[Callable[[List[Tribute], random.Random, "HungerBensSimulator"], List[str]]] = [
    event_trap_failure, event_environment, event_small_skirmish, event_heal,
    event_funny_business, event_weapon_malfunction, event_stealth_fail, event_sneak_attack,
    event_meteor_shower, event_sponsor_message, event_trap_success, event_camouflage,
    event_reckless_experiment, event_spooked_flock, event_alliance_aid, event_alliance_betrayal
]

# Default weights baseline
BASE_EVENT_WEIGHTS = {
    event_find_supplies: 1.2,
    event_small_skirmish: 1.3,
    event_trap_failure: 0.9,
    event_alliance: 0.8,
    event_supply_drop: 0.7,
    event_argument: 0.9,
    event_funny_business: 0.7,
    event_scavenger_find: 1.0,
    event_weapon_malfunction: 0.5,
    event_stealth_fail: 0.6,
    event_sneak_attack: 1.1,
    event_dance_off: 0.4,
    event_sponsor_message: 0.6,
    event_trap_success: 0.8,
    event_camouflage: 0.8,
    event_reckless_experiment: 0.5,
    event_chain_hunt: 0.5,
    event_spooked_flock: 0.6,
    event_alliance_aid: 0.5,
    event_alliance_betrayal: 0.3,
    event_environment: 1.0,
    event_heal: 0.9,
    event_meteor_shower: 0.4,
}

# -----------------------------
# Windows-only Plugin System
# -----------------------------
# Plugin API (optional functions in each plugin module):
#   - get_custom_content() -> dict with keys like {"weapons": {...}, "items": [...], "hazards": {...}}
#   - get_events() -> {"day": [callables], "night": [callables], "global": [callables]}
#   - get_event_weights() -> {callable or callable.__name__: float}
# Any provided content/events will be merged into the simulator's registries.
#
# Search order (Windows):
#   1) HUNGER_BENS_PLUGIN_DIRS (os.pathsep-separated list)
#   2) Repo-relative: <repo>/docs/plugins
#   3) %LOCALAPPDATA%\HungerBens\plugins
#   4) %APPDATA%\HungerBens\plugins (Roaming)
#   5) %PROGRAMDATA%\HungerBens\plugins (machine-wide)

_PLUGINS_LOADED = False

def _log_plugin(line: str, log_fn: Optional[Callable[[str], None]] = None):
    try:
        if log_fn:
            log_fn(line)
        else:
            print(line)
    except Exception:
        pass

def _iter_plugin_paths() -> List[str]:
    here = os.path.dirname(os.path.abspath(__file__))
    repo_plugins = os.path.join(here, 'plugins')
    env_dirs_raw = os.environ.get('HUNGER_BENS_PLUGIN_DIRS', '')
    env_dirs = [p for p in env_dirs_raw.split(os.pathsep) if p]
    candidates: List[str] = []
    if env_dirs:
        candidates.extend(env_dirs)
    # Default search locations
    candidates.append(repo_plugins)
    if os.name == 'nt':
        lap = os.environ.get('LOCALAPPDATA')
        rap = os.environ.get('APPDATA')  # Roaming
        prog = os.environ.get('PROGRAMDATA')
        if lap:
            candidates.append(os.path.join(lap, 'HungerBens', 'plugins'))
        if rap:
            candidates.append(os.path.join(rap, 'HungerBens', 'plugins'))
        if prog:
            candidates.append(os.path.join(prog, 'HungerBens', 'plugins'))
    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for p in candidates:
        if p and p not in seen:
            seen.add(p)
            ordered.append(p)
    return [p for p in ordered if os.path.isdir(p)]

def scan_plugin_files() -> List[Tuple[str, str]]:
    """Return list of (plugin_id, absolute_path) for available plugin .py files without importing.
    Skips __init__.py.
    """
    results: List[Tuple[str, str]] = []
    for d in _iter_plugin_paths():
        try:
            for fname in os.listdir(d):
                if not fname.endswith('.py') or fname == '__init__.py':
                    continue
                fpath = os.path.join(d, fname)
                pid = os.path.splitext(fname)[0]
                results.append((pid, fpath))
        except Exception:
            continue
    # Dedup by id with first occurrence kept
    seen: Set[str] = set()
    unique: List[Tuple[str, str]] = []
    for pid, path in results:
        if pid in seen:
            continue
        seen.add(pid)
        unique.append((pid, path))
    return unique

def load_windows_plugins(log_fn: Optional[Callable[[str], None]] = None):
    global _PLUGINS_LOADED
    if _PLUGINS_LOADED:
        return
    if os.name != 'nt':
        return
    # Proactively ensure common plugin directories exist (per-user and machine-wide)
    try:
        lap = os.environ.get('LOCALAPPDATA')
        rap = os.environ.get('APPDATA')
        prog = os.environ.get('PROGRAMDATA')
        for base in (lap, rap, prog):
            if not base:
                continue
            pdir = os.path.join(base, 'HungerBens', 'plugins')
            try:
                os.makedirs(pdir, exist_ok=True)
            except Exception as e:
                _log_plugin(f"[Plugins] Could not create {pdir}: {e}", log_fn)
    except Exception:
        pass
    plugin_dirs = _iter_plugin_paths()
    if not plugin_dirs:
        _PLUGINS_LOADED = True
        return
    loaded_any = False
    # Integrate config for per-plugin enable/disable; discover new plugins
    cfg_plugins: Dict[str, Any] = _CONFIG.get('plugins', {}) if isinstance(_CONFIG.get('plugins'), dict) else {}
    discovered = scan_plugin_files()
    # Seed config entries for new plugins
    for pid, ppath in discovered:
        entry = cfg_plugins.get(pid)
        if not isinstance(entry, dict):
            cfg_plugins[pid] = {"enabled": True, "path": ppath}
        else:
            # Update path if changed
            if ppath and entry.get('path') != ppath:
                entry['path'] = ppath
    _CONFIG['plugins'] = cfg_plugins
    try:
        save_config(_CONFIG)
    except Exception:
        pass
    for d in plugin_dirs:
        try:
            for fname in os.listdir(d):
                if not fname.endswith('.py') or fname == '__init__.py':
                    continue
                fpath = os.path.join(d, fname)
                pid = os.path.splitext(fname)[0]
                # Respect per-plugin enable flag
                pen = cfg_plugins.get(pid, {}).get('enabled', True)
                if not pen:
                    _log_plugin(f"[Plugins] Skipped disabled plugin {fname}", log_fn)
                    continue
                mod_name = f"hb_plugin_{pid}"
                try:
                    spec = importlib.util.spec_from_file_location(mod_name, fpath)
                    if not spec or not spec.loader:
                        continue
                    mod = importlib.util.module_from_spec(spec)
                    sys.modules[mod_name] = mod
                    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
                    loaded_any = True
                    _log_plugin(f"[Plugins] Loaded {fname}", log_fn)
                    # Content
                    if hasattr(mod, 'get_custom_content'):
                        try:
                            cc = mod.get_custom_content()  # type: ignore[attr-defined]
                            if isinstance(cc, dict) and cc:
                                integrate_custom_content(cc)
                                _log_plugin(f"[Plugins] Integrated custom content from {fname}", log_fn)
                        except Exception as e:
                            _log_plugin(f"[Plugins] get_custom_content error in {fname}: {e}", log_fn)
                    # Events
                    plugin_events: Dict[str, List[Callable]] = {}
                    if hasattr(mod, 'get_events'):
                        try:
                            ev = mod.get_events()  # type: ignore[attr-defined]
                            if isinstance(ev, dict):
                                for k in ('day','night','global'):
                                    arr = ev.get(k, [])
                                    if isinstance(arr, list):
                                        plugin_events[k] = [f for f in arr if callable(f)]
                                    else:
                                        plugin_events[k] = []
                                if plugin_events.get('day'):
                                    DAY_EVENTS.extend(plugin_events['day'])
                                if plugin_events.get('night'):
                                    NIGHT_EVENTS.extend(plugin_events['night'])
                                if plugin_events.get('global'):
                                    GLOBAL_EVENTS.extend(plugin_events['global'])
                                _log_plugin(f"[Plugins] Registered events from {fname}", log_fn)
                        except Exception as e:
                            _log_plugin(f"[Plugins] get_events error in {fname}: {e}", log_fn)
                    # Event weights
                    if hasattr(mod, 'get_event_weights'):
                        try:
                            w = mod.get_event_weights()  # type: ignore[attr-defined]
                            if isinstance(w, dict):
                                for key, weight in w.items():
                                    if not isinstance(weight, (int, float)):
                                        continue
                                    func = None
                                    if callable(key):
                                        func = key
                                    elif isinstance(key, str):
                                        # Try to resolve by name among plugin events
                                        for arr in (plugin_events.get('day', []), plugin_events.get('night', []), plugin_events.get('global', [])):
                                            for f in arr:
                                                if getattr(f, '__name__', '') == key:
                                                    func = f
                                                    break
                                            if func:
                                                break
                                    if func:
                                        BASE_EVENT_WEIGHTS[func] = float(weight)
                                _log_plugin(f"[Plugins] Applied event weights from {fname}", log_fn)
                        except Exception as e:
                            _log_plugin(f"[Plugins] get_event_weights error in {fname}: {e}", log_fn)
                except Exception as e:
                    _log_plugin(f"[Plugins] Failed to load {fname}: {e}", log_fn)
        except Exception as e:
            _log_plugin(f"[Plugins] Directory error for {d}: {e}", log_fn)
    _PLUGINS_LOADED = True
    if loaded_any:
        _log_plugin("[Plugins] Windows plugins loaded.", log_fn)

# -----------------------------
# Simulator
# -----------------------------
class HungerBensSimulator:
    def __init__(
        self,
        tribute_data: Dict[str, Dict[str, Any]],
        seed: Optional[int] = None,
        max_days: int = 50,
        verbose: bool = True,
        export_log: Optional[str] = None,
        strict_shutdown: Optional[int] = None,
        log_callback: Optional[Callable[[str], None]] = None,
    ):
        self.rng = random.Random(seed)
        self.seed = seed
        self.max_days = max_days
        self.verbose = verbose
        self.day_count = 0
        self.strict_shutdown = strict_shutdown
        self._log_callback = log_callback
        self.tributes: List[Tribute] = [
            Tribute(
                key=k,
                name=v["name"],
                gender=v.get("gender","unknown"),
                age=int(v.get("age", 0)),
                district=int(v.get("district", 0)),
            )
            for k, v in tribute_data.items()
        ]
        self.log: List[str] = []
        self._cornucopia_run = False
        self.alliances = AllianceManager()
        self.history_stats = {
            "day_morale_avg": [],
            "events_run": 0,
        }
        self.export_log_path = export_log
        self.death_log: List[Dict[str, Any]] = []

    # --- Basic helpers ---
    def alive_tributes(self) -> List[Tribute]:
        return [t for t in self.tributes if t.alive]

    def _log(self, message: str):
        self.log.append(message)
        if self.verbose:
            print(message)
        if self._log_callback:
            try:
                self._log_callback(message)
            except Exception:
                # Fail silently so simulation continues even if GUI callback breaks
                pass

    # --- Simulation Control ---
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
            if self.strict_shutdown and self.day_count >= self.strict_shutdown and len(self.alive_tributes()) > 2:
                self._log("\nEARLY ARENA TERMINATION PROTOCOL TRIGGERED.")
                break
        self._announce_winner()
        self._output_stats()
        if self.export_log_path:
            self._export_run()
        return self.log

    # --- Phase Methods ---
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
                    # Morale impacts who wins initial struggle
                    prob_t = 0.5 + (t.morale - opp.morale) * 0.05
                    winner, loser = (t, opp) if self.rng.random() < prob_t else (opp, t)
                    loot = self.rng.choice(CORNUCOPIA_ITEMS)
                    winner.inventory.append(loot)
                    _kill(loser, f"bloodbath elimination by {winner.name}")
                    winner.kills += 1
                    winner.notoriety += 1
                    winner.adjust_morale(+1)
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

    def _simulate_day(self):
        self._log(f"\n--- Day {self.day_count} ---")
        self._run_event_block(DAY_EVENTS, "day")

    def _simulate_night(self):
        self._log(f"\n*** Night {self.day_count} ***")
        self._run_event_block(NIGHT_EVENTS, "night")

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
            prob_a = 0.5 + (a.morale - b.morale) * 0.04
            if self.rng.random() < 0.55:
                winner, loser = (a, b) if self.rng.random() < prob_a else (b, a)
                _kill(loser, f"Feast clash vs {winner.name}")
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

    # --- Event Loop ---
    def _run_event_block(self, event_pool, phase):
        alive = self.alive_tributes()
        if not alive: return
        # Track average morale
        avg_morale = sum(t.morale for t in alive)/len(alive)
        self.history_stats["day_morale_avg"].append(avg_morale)
        events_to_run = min(len(alive), self.rng.randint(3, 6))
        for _ in range(events_to_run):
            alive = self.alive_tributes()
            if len(alive) <= 1: break
            event_func = self._choose_weighted_event(event_pool)
            narrative = event_func(alive, self.rng, self)
            self.history_stats["events_run"] += 1
            for line in narrative:
                if line:
                    self._log(line)
            self._post_event_cleanup()
        self._maybe_global_event()
        fallen = [t for t in self.tributes if not t.alive and f"(Fallen logged {t.key})" not in t.__dict__]
        if fallen:
            self._log("\nFallen this phase:")
            for f in fallen:
                self._log(f" - {f.name}")
                f.__dict__[f"(Fallen logged {f.key})"] = True
                self.death_log.append({"name": f.name, "cause": f.cause_of_death, "day": self.day_count, "phase": phase})
        self.alliances.remove_dead(self.tributes)

    def _choose_weighted_event(self, pool):
        # Base weights + dynamic scaling
        weights = []
        alive_count = len(self.alive_tributes())
        for ev in pool:
            base = BASE_EVENT_WEIGHTS.get(ev, 0.7)
            # More aggressive events when fewer tributes
            if alive_count < 10 and ev in [event_small_skirmish, event_sneak_attack, event_trap_success]:
                base *= 1.3
            # Less comedic late game
            if alive_count < 6 and ev in [event_funny_business, event_dance_off]:
                base *= 0.5
            # Betrayal more likely mid-late
            if ev == event_alliance_betrayal and 6 < alive_count < 20:
                base *= 1.4
            weights.append(base)
        return self.rng.choices(pool, weights=weights, k=1)[0]

    def _maybe_global_event(self):
        # Scale frequency as days progress (capped)
        base = 0.30 + (self.day_count * 0.01)
        if self.rng.random() < min(0.55, base):
            ge = self.rng.choice(GLOBAL_EVENTS)
            lines = ge(self.alive_tributes(), self.rng, self)
            for l in lines:
                self._log(l)

    def _post_event_cleanup(self):
        # Remove duplicate clutter items (optional logic: keep only one of repeated 'moral support note')
        for t in self.tributes:
            if not t.alive: continue
            # Example dedup for moral support note
            filtered = []
            seen_note = False
            for it in t.inventory:
                if it == "moral support note":
                    if seen_note:
                        continue
                    seen_note = True
                filtered.append(it)
            t.inventory = filtered

    # --- Finalization ---
    def _announce_winner(self):
        winners = self.alive_tributes()
        if winners:
            if len(winners) > 1 and self.day_count >= self.max_days:
                self._log("\nARENA FORCED SHUTDOWN: Multiple survivors remain!")
                for w in winners:
                    self._log(f"Survivor: {w.name} (District {w.district}, Kills: {w.kills}, Notoriety:{w.notoriety})")
            elif len(winners) > 1 and self.strict_shutdown and self.day_count >= self.strict_shutdown:
                self._log("\nEARLY SHUTDOWN: Multiple survivors extracted!")
                for w in winners:
                    self._log(f"Extracted: {w.name} (District {w.district}, Kills: {w.kills}, Notoriety:{w.notoriety})")
            else:
                w = winners[0]
                self._log(f"\nVICTOR: {w.name} (District {w.district}, Kills: {w.kills}, Notoriety:{w.notoriety})")
        else:
            self._log("\nNo victor emerged. The arena claims all.")
        self._log("\nFinal standings:")
        for t in sorted(self.tributes, key=lambda x: (-x.alive, -x.kills, -x.notoriety, x.name)):
            self._log(f" - {t}")

    def _output_stats(self):
        self._log("\n=== Statistics Summary ===")
        kills_sorted = sorted(self.tributes, key=lambda t: t.kills, reverse=True)
        top_killers = [t for t in kills_sorted if t.kills > 0][:5]
        if top_killers:
            self._log("Top Killers:")
            for t in top_killers:
                self._log(f"  {t.name}: {t.kills} kills (Notoriety {t.notoriety})")
        avg_morale_series = self.history_stats["day_morale_avg"]
        if avg_morale_series:
            self._log(f"Average Morale Trend: {', '.join(f'{m:.1f}' for m in avg_morale_series)}")
        death_causes = {}
        for d in self.death_log:
            death_causes[d["cause"]] = death_causes.get(d["cause"], 0) + 1
        if death_causes:
            self._log("Death Causes:")
            for cause, count in sorted(death_causes.items(), key=lambda x: -x[1]):
                self._log(f"  {cause}: {count}")
        self._log(f"Total Events Run: {self.history_stats['events_run']}")

        if self.seed is not None:
            self._log(f"Reproducible with seed {self.seed}")
        else:
            self._log("A random seed was used (not provided).")

    def _log_intro(self):
        self._log("Welcome to the Hunger Bens Simulation (Enhanced Edition)!")
        self._log(
            f"Total Tributes: {len(self.tributes)}\n"
            "Tributes entering the arena: "
            + ", ".join(f"{t.name} (D{t.district})" for t in self.tributes)
            + "\n"
        )

    def _export_run(self):
        data = {
            "timestamp": datetime.utcnow().isoformat()+"Z",
            "seed": self.seed,
            "max_days": self.max_days,
            "final_day": self.day_count,
            "alliances": self.alliances.to_dict(),
            "tributes": [self._tribute_to_dict(t) for t in self.tributes],
            "death_log": self.death_log,
            "log": self.log,
            "stats": self.history_stats,
        }
        try:
            with open(self.export_log_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self._log(f"\nRun exported to {self.export_log_path}")
        except Exception as e:
            self._log(f"Failed to export log: {e}")

    def _tribute_to_dict(self, t: Tribute):
        d = asdict(t)
        return d

# -----------------------------
# Roster / Input Utilities
# -----------------------------
def load_roster_json(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Accept list or dict
    roster: Dict[str, Dict[str, Any]] = {}
    if isinstance(data, list):
        for idx, entry in enumerate(data, start=1):
            if not isinstance(entry, dict): continue
            key = entry.get("key") or f"cust{idx}"
            roster[key] = {
                "name": entry.get("name", f"Custom {idx}"),
                "gender": entry.get("gender", "unknown"),
                "age": entry.get("age", 18),
                "district": entry.get("district", (idx % 12) + 1)
            }
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                roster[k] = {
                    "name": v.get("name", k),
                    "gender": v.get("gender", "unknown"),
                    "age": v.get("age", 18),
                    "district": v.get("district", 1)
                }
    return roster

def addnomen(dicty_ref: Dict[str, Dict[str, Any]]):
    print("Add custom tributes (blank key to stop).")
    while True:
        key = input("Enter a unique key for the tribute (e.g., tribX) or blank to finish: ").strip()
        if not key:
            break
        if key in dicty_ref:
            print("Key already exists. Choose a different key.")
            continue
        name = input("Enter the tribute's name: ").strip()
        if not name:
            print("Name cannot be empty."); continue
        gender = input("Enter the tribute's gender: ").strip() or "unspecified"
        age = input("Enter the tribute's age (number): ").strip()
        if not age.isdigit():
            print("Age must be a number."); continue
        district = input("Enter the tribute's district (1-12): ").strip()
        if not district.isdigit() or not (1 <= int(district) <= 12):
            print("District must be a number 1-12."); continue
        dicty_ref[key] = {
            "name": name,
            "gender": gender,
            "age": int(age),
            "district": int(district),
        }
        if input("Add more tributes? (y/n): ").lower() != 'y':
            break

# -----------------------------
# Custom Content Loader (Weapons / Hazards / Events)
# -----------------------------
# Supported JSON schema (any field optional):
# {
#   "weapons": {"laser spoon": "zaps"},             # weapon name -> verb
#   "items": ["force field", "decoy duck"],         # extra supply items
#   "hazards": {"gravity well": "crushed"},        # hazard -> effect keyword
# }
# or separate flags per file.

def load_custom_content(path: str):
    """Load custom content definitions from JSON.
    Returns dict with potential keys: weapons, items, hazards
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Custom content JSON must be an object.")
        return data
    except Exception as e:
        print(f"Failed to load custom content: {e}")
        return {}

def load_custom_content_from_string(s: str) -> Dict[str, Any]:
    """Parse custom content JSON from a raw string without using files.
    Returns an empty dict on failure.
    """
    try:
        data = json.loads(s)
        if not isinstance(data, dict):
            raise ValueError("Custom content JSON must be an object.")
        return data
    except Exception as e:
        print(f"Failed to parse custom content JSON: {e}")
        return {}

def integrate_custom_content(content: Dict[str, Any]):
    """Mutate global registries with user-provided extensions."""
    # Weapons
    new_weapons = content.get('weapons', {})
    if isinstance(new_weapons, dict):
        for w, verb in new_weapons.items():
            if not isinstance(w, str) or not isinstance(verb, str):
                continue
            WEAPON_VERBS[w] = verb
        # Update WEAPONS set (exclude base non-weapons)
        global WEAPONS
        WEAPONS = set(WEAPON_VERBS.keys()) - {"fists", "rock", "stick"}
    # Items
    extra_items = content.get('items', [])
    if isinstance(extra_items, list):
        for it in extra_items:
            if isinstance(it, str) and it not in SUPPLY_ITEMS and it not in CORNUCOPIA_ITEMS:
                SUPPLY_ITEMS.append(it)
    # Hazards
    new_hazards = content.get('hazards', {})
    if isinstance(new_hazards, dict):
        for hz, effect in new_hazards.items():
            if not isinstance(hz, str) or not isinstance(effect, str):
                continue
            if hz not in HAZARDS:
                HAZARDS.append(hz)
            HAZARD_EFFECTS[hz] = effect

# -----------------------------
# Convenience Runner
# -----------------------------
def run_simulation(
    seed: Optional[int] = None,
    max_days: int = 30,
    verbose: bool = True,
    export_log: Optional[str] = None,
    roster: Optional[Dict[str, Dict[str, Any]]] = None,
    strict_shutdown: Optional[int] = None,
    log_callback: Optional[Callable[[str], None]] = None,
    enable_plugins: Optional[bool] = None,
):
    tribute_source = roster if roster else dicty
    # Windows-only plugin activation (default comes from config unless explicitly overridden)
    try:
        if enable_plugins is None:
            enable = bool(_CONFIG.get('plugins_enabled', _default_plugins_enabled())) and (os.name == 'nt')
        else:
            enable = bool(enable_plugins) and (os.name == 'nt')
        if enable:
            load_windows_plugins(log_callback)
    except Exception:
        # Never fail simulation due to plugins
        pass
    sim = HungerBensSimulator(
        tribute_source,
        seed=seed,
        max_days=max_days,
        verbose=verbose,
        export_log=export_log,
        strict_shutdown=strict_shutdown,
        log_callback=log_callback,
    )
    sim.run()
    return sim

# -----------------------------
# Windows-only Tkinter GUI
# -----------------------------
if os.name == 'nt':
    class HungerBensGUI:
        def __init__(self, root):
            self.root = root
            root.title("Hunger Bens Simulator")
            self._build_widgets()
            self.current_sim: Optional[HungerBensSimulator] = None
            self.roster_override: Optional[Dict[str, Dict[str, Any]]] = None
            self.plugins_var = tkinter.BooleanVar(value=bool(_CONFIG.get('plugins_enabled', _default_plugins_enabled())))
            # Persist when toggled
            try:
                self.plugins_var.trace_add('write', lambda *args: self._on_plugins_toggle())
            except Exception:
                pass

        def _build_widgets(self):
            frm = ttk.Frame(self.root, padding=10)
            frm.grid(row=0, column=0, sticky='nsew')
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(1, weight=1)

            # Inputs
            ttk.Label(frm, text="Seed:").grid(row=0, column=0, sticky='w')
            self.seed_entry = ttk.Entry(frm, width=12)
            self.seed_entry.grid(row=0, column=1, sticky='w')

            ttk.Label(frm, text="Max Days:").grid(row=0, column=2, sticky='w')
            self.days_entry = ttk.Entry(frm, width=6)
            self.days_entry.insert(0, '30')
            self.days_entry.grid(row=0, column=3, sticky='w')

            ttk.Label(frm, text="Strict Shutdown Day:").grid(row=1, column=0, sticky='w')
            self.strict_entry = ttk.Entry(frm, width=12)
            self.strict_entry.grid(row=1, column=1, sticky='w')

            self.verbose_var = tkinter.BooleanVar(value=True)
            ttk.Checkbutton(frm, text="Verbose", variable=self.verbose_var).grid(row=1, column=2, columnspan=2, sticky='w')

            ttk.Label(frm, text="Export Log File:").grid(row=2, column=0, sticky='w')
            self.export_entry = ttk.Entry(frm, width=25)
            self.export_entry.grid(row=2, column=1, columnspan=2, sticky='we')
            ttk.Button(frm, text="Browse", command=self._browse_export).grid(row=2, column=3, sticky='w')

            # Roster load
            ttk.Label(frm, text="Custom Roster JSON:").grid(row=3, column=0, sticky='w')
            self.roster_entry = ttk.Entry(frm, width=25)
            self.roster_entry.grid(row=3, column=1, columnspan=2, sticky='we')
            ttk.Button(frm, text="Load", command=self._load_roster).grid(row=3, column=3, sticky='w')

            ttk.Label(frm, text="Content JSON:").grid(row=4, column=0, sticky='w')
            self.content_entry = ttk.Entry(frm, width=25)
            self.content_entry.grid(row=4, column=1, columnspan=2, sticky='we')
            ttk.Button(frm, text="Load", command=self._load_content).grid(row=4, column=3, sticky='w')

            # Inline JSON for content (no external files)
            ttk.Label(frm, text="Inline Content JSON:").grid(row=5, column=0, sticky='w')
            self.inline_content_entry = ttk.Entry(frm, width=25)
            self.inline_content_entry.grid(row=5, column=1, columnspan=2, sticky='we')
            ttk.Button(frm, text="Apply", command=self._apply_inline_content).grid(row=5, column=3, sticky='w')

            # Plugins (Windows only)
            ttk.Checkbutton(frm, text="Enable Plugins (Windows)", variable=self.plugins_var).grid(row=6, column=0, columnspan=2, sticky='w')

            # Run controls
            btn_frame = ttk.Frame(frm)
            btn_frame.grid(row=7, column=0, columnspan=4, pady=(8,4), sticky='we')
            ttk.Button(btn_frame, text="Run Simulation", command=self._run).grid(row=0, column=0, padx=4)
            ttk.Button(btn_frame, text="Clear Output", command=self._clear_output).grid(row=0, column=1, padx=4)
            ttk.Button(btn_frame, text="Settings", command=self._open_settings).grid(row=0, column=2, padx=4)
            ttk.Button(btn_frame, text="Quit", command=self.root.quit).grid(row=0, column=3, padx=4)

            # Output area
            self.output = scrolledtext.ScrolledText(self.root, wrap='word', height=30)
            self.output.grid(row=1, column=0, sticky='nsew')
            self.root.rowconfigure(1, weight=1)
            self.root.columnconfigure(0, weight=1)

        def _browse_export(self):
            path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON','*.json')])
            if path:
                self.export_entry.delete(0, 'end')
                self.export_entry.insert(0, path)

        def _load_roster(self):
            path = filedialog.askopenfilename(filetypes=[('JSON','*.json')])
            if not path:
                return
            try:
                data = load_roster_json(path)
                self.roster_override = data
                self.roster_entry.delete(0,'end')
                self.roster_entry.insert(0, path)
                messagebox.showinfo("Roster Loaded", f"Loaded {len(data)} tributes")
            except Exception as e:
                messagebox.showerror("Roster Error", f"Failed to load roster: {e}")

        def _load_content(self):
            path = filedialog.askopenfilename(filetypes=[('JSON','*.json')])
            if not path:
                return
            try:
                cc = load_custom_content(path)
                integrate_custom_content(cc)
                self.content_entry.delete(0,'end')
                self.content_entry.insert(0, path)
                messagebox.showinfo("Content Loaded", "Custom content integrated")
            except Exception as e:
                messagebox.showerror("Content Error", f"Failed to load content: {e}")

        def _apply_inline_content(self):
            raw = self.inline_content_entry.get().strip()
            if not raw:
                messagebox.showwarning("No JSON", "Please paste JSON into the Inline Content JSON field.")
                return
            data = load_custom_content_from_string(raw)
            if not data:
                messagebox.showerror("Invalid JSON", "Failed to parse custom content JSON. Check format.")
                return
            try:
                integrate_custom_content(data)
                messagebox.showinfo("Content Applied", "Inline custom content integrated")
            except Exception as e:
                messagebox.showerror("Content Error", f"Failed to integrate content: {e}")

        def _append_log(self, line: str):
            self.output.insert('end', line + '\n')
            self.output.see('end')

        def _clear_output(self):
            self.output.delete('1.0', 'end')

        def _run(self):
            # Parse inputs
            seed_txt = self.seed_entry.get().strip()
            seed = int(seed_txt) if seed_txt.isdigit() else None
            days_txt = self.days_entry.get().strip()
            try:
                max_days = int(days_txt) if days_txt else 30
            except ValueError:
                messagebox.showerror("Input Error", "Max Days must be an integer.")
                return
            strict_txt = self.strict_entry.get().strip()
            strict = int(strict_txt) if strict_txt.isdigit() else None
            export_file = self.export_entry.get().strip() or None
            verbose = self.verbose_var.get()

            self._clear_output()
            self._append_log("Launching simulation...")
            try:
                self.current_sim = run_simulation(
                    seed=seed,
                    max_days=max_days,
                    verbose=verbose,
                    export_log=export_file,
                    roster=self.roster_override,
                    strict_shutdown=strict,
                    log_callback=self._append_log,
                    enable_plugins=self.plugins_var.get(),
                )
                self._append_log("Simulation complete.")
            except Exception as e:
                messagebox.showerror("Run Error", f"Simulation failed: {e}")

        def _on_plugins_toggle(self):
            val = bool(self.plugins_var.get())
            try:
                _CONFIG['plugins_enabled'] = val
                save_config(_CONFIG)
            except Exception:
                pass

        def _compute_plugin_paths(self):
            here = os.path.dirname(os.path.abspath(__file__))
            repo_plugins = os.path.join(here, 'plugins')
            lap = os.environ.get('LOCALAPPDATA')
            rap = os.environ.get('APPDATA')
            prog = os.environ.get('PROGRAMDATA')
            paths = []
            if lap:
                paths.append(("LocalAppData", os.path.join(lap, 'HungerBens', 'plugins')))
            if rap:
                paths.append(("AppData (Roaming)", os.path.join(rap, 'HungerBens', 'plugins')))
            if prog:
                paths.append(("ProgramData (All Users)", os.path.join(prog, 'HungerBens', 'plugins')))
            paths.append(("Repo (docs/plugins)", repo_plugins))
            return paths

        def _open_folder(self, path: str):
            try:
                os.makedirs(path, exist_ok=True)
                os.startfile(path)  # type: ignore[attr-defined]
            except Exception as e:
                messagebox.showerror("Open Folder", f"Failed to open/create folder:\n{path}\n\n{e}")

        def _open_settings(self):
            win = tkinter.Toplevel(self.root)
            win.title("Settings")
            win.geometry("560x360")
            c = ttk.Frame(win, padding=10)
            c.pack(fill='both', expand=True)

            # Section: Plugins
            ttk.Label(c, text="Plugins", font=(None, 12, 'bold')).pack(anchor='w')
            desc = "Manage plugin folders and enable/disable individual plugins."
            ttk.Label(c, text=desc).pack(anchor='w', pady=(0,8))

            paths = self._compute_plugin_paths()
            # Scrollable area if many rows
            canvas = tkinter.Canvas(c, highlightthickness=0)
            scroll_y = ttk.Scrollbar(c, orient='vertical', command=canvas.yview)
            row_frame = ttk.Frame(canvas)
            row_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0,0), window=row_frame, anchor='nw')
            canvas.configure(yscrollcommand=scroll_y.set, height=180)
            canvas.pack(side='left', fill='both', expand=True)
            scroll_y.pack(side='right', fill='y')

            for i, (label, p) in enumerate(paths):
                row = ttk.Frame(row_frame)
                row.grid(row=i, column=0, sticky='we', pady=3)
                row.columnconfigure(1, weight=1)
                exists = os.path.isdir(p)
                text = f"{label}: {p}"
                ttk.Label(row, text=text, wraplength=420, justify='left').grid(row=0, column=0, sticky='w')
                state = "Exists" if exists else "(will be created)"
                ttk.Label(row, text=state, foreground=("#8f8" if exists else "#ff8")).grid(row=0, column=1, padx=8, sticky='e')
                ttk.Button(row, text="Open", command=lambda path=p: self._open_folder(path)).grid(row=0, column=2, padx=6)

            # Other settings placeholders (future)
            ttk.Separator(c).pack(fill='x', pady=10)
            # Plugin enable/disable list
            ttk.Label(c, text="Installed Plugins", font=(None, 12, 'bold')).pack(anchor='w')
            list_frame = ttk.Frame(c)
            list_frame.pack(fill='both', expand=True)
            inner = ttk.Frame(list_frame)
            inner.pack(fill='both', expand=True)

            def refresh_plugins():
                for w in inner.winfo_children():
                    w.destroy()
                plugins = scan_plugin_files()
                cfg_pl = _CONFIG.get('plugins', {}) if isinstance(_CONFIG.get('plugins'), dict) else {}
                rowi = 0
                for pid, path in plugins:
                    entry = cfg_pl.get(pid, {"enabled": True, "path": path})
                    var = tkinter.BooleanVar(value=bool(entry.get('enabled', True)))
                    def make_cb(p_id: str, v: tkinter.BooleanVar):
                        def _cb(*_):
                            cfg = _CONFIG.get('plugins')
                            if not isinstance(cfg, dict):
                                _CONFIG['plugins'] = {}
                                cfg = _CONFIG['plugins']
                            ent = cfg.get(p_id)
                            if not isinstance(ent, dict):
                                ent = {}
                                cfg[p_id] = ent
                            ent['enabled'] = bool(v.get())
                            ent['path'] = path
                            save_config(_CONFIG)
                        return _cb
                    var.trace_add('write', make_cb(pid, var))
                    row = ttk.Frame(inner)
                    row.grid(row=rowi, column=0, sticky='we', pady=2)
                    row.columnconfigure(1, weight=1)
                    ttk.Checkbutton(row, text=pid, variable=var).grid(row=0, column=0, sticky='w')
                    ttk.Label(row, text=path, wraplength=360).grid(row=0, column=1, sticky='w', padx=6)
                    rowi += 1

            btns = ttk.Frame(c)
            btns.pack(fill='x', pady=(6,0))
            ttk.Button(btns, text="Refresh", command=refresh_plugins).pack(side='left')
            ttk.Button(btns, text="Close", command=win.destroy).pack(side='right')

            # Initial population
            refresh_plugins()


def askagain(roster):
    while True:
        again = input("Run another simulation? (y/n): ").lower()
        if again == 'y':
            mainloop(roster_override=roster)
        elif again == 'n':
            break
        else:
            print("Please enter 'y' or 'n'.")
    print("Thank you for using the Hunger Bens Simulator!")

def mainloop(roster_override=None, clear_screen: bool = True):
    seedin = input("Enter a seed (or leave blank for random): ").strip()
    seedin = int(seedin) if seedin.isdigit() else None
    maxday = input("Enter max days (default 30): ").strip()
    maxday = int(maxday) if maxday.isdigit() else 30
    strict = input("Enter strict shutdown day (optional, blank=none): ").strip()
    strict = int(strict) if strict.isdigit() else None
    verb = input("Verbose output? (y/n, default y): ").lower() != 'n'
    working_dicty = dict(dicty) if roster_override is None else dict(roster_override)
    if input("Add custom tributes? (y/n): ").lower() == 'y':
        addnomen(working_dicty)
    # Inline custom content JSON (no file required)
    if input("Add custom content via JSON? (y/n): ").lower() == 'y':
        print("Paste a JSON object with optional keys: 'weapons', 'items', 'hazards'. One line recommended.")
        raw = input("Content JSON (blank to skip): ").strip()
        if raw:
            cc = load_custom_content_from_string(raw)
            if cc:
                integrate_custom_content(cc)
                print("Custom content integrated.")
            else:
                print("Invalid JSON; skipping custom content.")
    export_q = input("Export run to JSON? (filename or blank): ").strip()
    export_file = export_q if export_q else None
    if clear_screen:
        # Clear screen so the simulation output starts at top of terminal for readability
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        except Exception:
            pass
    run_simulation(seed=seedin, max_days=maxday, verbose=verb, export_log=export_file, roster=working_dicty, strict_shutdown=strict)
    print("\nSimulation complete.")
    print("You can rerun with the same seed for identical results.")
    print(seedin if seedin is not None else "Random seed used.")
    askagain(working_dicty)

# -----------------------------
# CLI Argument Parsing
# -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Hunger Bens Simulator (Enhanced)")
    parser.add_argument("--seed", type=int, help="Random seed (int)")
    parser.add_argument("--max-days", type=int, default=30, help="Maximum days to simulate")
    parser.add_argument("--quiet", action="store_true", help="Suppress live output (still logs internally)")
    parser.add_argument("--export-log", type=str, help="Export full run JSON to file")
    parser.add_argument("--roster", type=str, help="Path to JSON roster file")
    parser.add_argument("--content", type=str, help="Path to JSON custom content file (weapons/hazards/events)")
    parser.add_argument("--content-json", type=str, help="Inline JSON string for custom content (no file)")
    parser.add_argument("--strict-shutdown", type=int, help="Force terminate after given day if multiple alive")
    parser.add_argument("--interactive", action="store_true", help="Use interactive loop instead of single run")
    parser.add_argument("--no-clear", action="store_true", help="Disable clearing the screen before interactive simulation output")
    if os.name == 'nt':
        parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI (Windows only)")
        parser.add_argument("--no-plugins", action="store_true", help="Disable Windows plugin loader")
        parser.add_argument("--plugin-dir", type=str, help="Directory for Windows plugins (overrides default)")
        parser.add_argument("--plugins", action="store_true", help="Enable Windows plugin loader (overrides config)")
    return parser.parse_args()

def cli_entry():
    args = parse_args()
    roster_data = None
    if args.roster:
        if not os.path.isfile(args.roster):
            print(f"Roster file not found: {args.roster}")
            return
        try:
            roster_data = load_roster_json(args.roster)
            print(f"Loaded {len(roster_data)} custom tributes from {args.roster}")
        except Exception as e:
            print(f"Failed to load roster: {e}")
            return
    if args.content:
        if not os.path.isfile(args.content):
            print(f"Custom content file not found: {args.content}")
        else:
            cc = load_custom_content(args.content)
            integrate_custom_content(cc)
            print(f"Custom content integrated from {args.content}")
    if getattr(args, 'content_json', None):
        cc2 = load_custom_content_from_string(args.content_json)
        if cc2:
            integrate_custom_content(cc2)
            print("Inline custom content integrated from --content-json")
        else:
            print("Failed to parse --content-json; ignoring.")
    # GUI mode
    if os.name == 'nt' and getattr(args, 'gui', False):
        import tkinter
        root = tkinter.Tk()
        gui = HungerBensGUI(root)
        sv_ttk.set_theme("dark")
        root.mainloop()
        return
    if args.interactive:
        mainloop(roster_override=roster_data, clear_screen=not args.no_clear)
    else:
        # Configure plugin dirs if provided (Windows only)
        if os.name == 'nt':
            if getattr(args, 'plugin_dir', None):
                os.environ['HUNGER_BENS_PLUGIN_DIRS'] = args.plugin_dir
        # Determine plugin enablement: CLI overrides config; default uses config
        enable_plugins = None
        if os.name == 'nt':
            if getattr(args, 'no_plugins', False):
                enable_plugins = False
            elif getattr(args, 'plugins', False):
                enable_plugins = True
        run_simulation(
            seed=args.seed,
            max_days=args.max_days,
            verbose=not args.quiet,
            export_log=args.export_log,
            roster=roster_data,
            strict_shutdown=args.strict_shutdown,
            enable_plugins=enable_plugins,
        )

if __name__ == "__main__":
    # If launched without arguments, fallback to prior behavior (interactive)
    import sys
    # Allow suppression of interactive mode when imported in Pyodide (web) context
    if os.environ.get("HUNGER_BENS_NO_INTERACTIVE") == "1":
        cli_entry()
    else:
        if len(sys.argv) > 1:
            cli_entry()
        else:
            mainloop(clear_screen=True)