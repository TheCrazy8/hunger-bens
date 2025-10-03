import random
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional

# -----------------------------
# Data Setup
# -----------------------------
# Added age so the original loop (if you keep it) won't break.
# Added district per user request.
# You can expand this dictionary with more "bens" or other tributes.
dicty: Dict[str, Dict[str, str]] = {
    "trib1": {"name": "Ben", "gender": "male", "age": 16, "district": 1},
    "trib2": {"name": "Ben's Mom", "gender": "female", "age": 45, "district": 2},
    "trib3": {"name": "BenBot 3000", "gender": "object", "age": 2, "district": 3},  # Programmatic age :)
    "trib4": {"name": "Ben's Twin", "gender": "male", "age": 16, "district": 1},
    "trib5": {"name": "Ben's Cousin", "gender": "male", "age": 18, "district": 4},
    "trib6": {"name": "Ben's Aunt", "gender": "female", "age": 40, "district": 5},
    "trib7": {"name": "Ben's Uncle", "gender": "male", "age": 42, "district": 6},
    "trib8": {"name": "Eggworth Von Strudenstein", "gender": "male", "age": 30, "district": 7},
}

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

    def __str__(self):
        status = "Alive" if self.alive else "Fallen"
        return f"{self.name} (D{self.district}, {status}, Kills: {self.kills})"


# -----------------------------
# Arena Events Configuration
# -----------------------------
# Event functions take (alive_tributes, rng) and return a narrative string list.
# They are responsible for marking tributes dead or modifying state.

def event_find_supplies(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    item = rng.choice([
        "rope", "knife", "medical kit", "berries", "canteen", "gun",
        "bow", "bow tie", "egg", "lighter", "flashlight", "map", "compass"
    ])
    t.inventory.append(item)
    return [f"{t.name} finds a {item}."]

def event_small_skirmish(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2:
        return []
    a, b = rng.sample(tributes, 2)
    winner, loser = (a, b) if rng.random() < 0.5 else (b, a)
    usable_weapons = [item for item in winner.inventory if item in ["knife", "gun", "bow", "bow tie", "spear"]]
    if usable_weapons:
        weapon = rng.choice(usable_weapons)
    else:
        weapon = rng.choice(["fists", "rock", "stick"])
    verb = {
        "fists": "pummels",
        "rock": "bludgeons",
        "stick": "strikes",
        "knife": "slashes",
        "gun": "shoots",
        "bow": "shoots",
        "bow tie": "dazzles",
        "spear": "impales",
    }[weapon]
    loser.alive = False
    winner.kills += 1
    return [f"{winner.name} {verb} {loser.name} with {('a ' if weapon not in ['fists'] else '')}{weapon}. {loser.name} is eliminated."]

def event_trap_failure(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    # Low probability of death
    if rng.random() < 0.25:
        t.alive = False
        return [f"{t.name} triggers a faulty trap and is eliminated."]
    else:
        return [f"{t.name} sets a trap but it malfunctions harmlessly."]

def event_alliance(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2:
        return []
    a, b = rng.sample(tributes, 2)
    return [f"{a.name} and {b.name} form a shaky temporary alliance."]

def event_environment(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    hazard = rng.choice(["acid rain", "falling debris", "poison mist", "lava vent", "wild animal", "flash flood", "earthquake", "forest fire"])
    effectofhazard = {
        "acid rain": "burned",
        "falling debris": "crushed",
        "poison mist": "poisoned",
        "lava vent": "scorched",
        "wild animal": "attacked",
        "flash flood": "swept away",
        "earthquake": "trampled",
        "forest fire": "burned",
    }[hazard]
    # Moderate probability of death
    if rng.random() < 0.35:
        t.alive = False
        return [f"{t.name} is {effectofhazard} by {hazard}."]
    return [f"{t.name} narrowly escapes a patch of {hazard}."]

def event_heal(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    if "medical kit" in t.inventory:
        return [f"{t.name} uses a medical kit to heal minor wounds."]
    return [f"{t.name} looks for ways to heal but finds nothing."]


DAY_EVENTS: List[Callable[[List[Tribute], random.Random], List[str]]] = [
    event_find_supplies,
    event_small_skirmish,
    event_trap_failure,
    event_alliance,
]

NIGHT_EVENTS: List[Callable[[List[Tribute], random.Random], List[str]]] = [
    event_trap_failure,
    event_environment,
    event_small_skirmish,
    event_heal,
]

# Items available at the Cornucopia (Bloodbath)
CORNUCOPIA_ITEMS = [
    "knife", "gun", "bow", "medical kit", "rope", "canteen", "berries",
    "map", "compass", "flashlight", "shield", "spear", "helmet"
]

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
        self._cornucopia_run = False  # ensure it only runs once

    def alive_tributes(self) -> List[Tribute]:
        return [t for t in self.tributes if t.alive]

    def run(self):
        self._log_intro()
        self._cornucopia_phase()  # Bloodbath at the start
        while len(self.alive_tributes()) > 1 and self.day_count < self.max_days:
            self.day_count += 1
            self._simulate_day()
            if len(self.alive_tributes()) <= 1:
                break
            self._simulate_night()

        self._announce_winner()
        return self.log

    # -----------------------------
    # Cornucopia / Bloodbath Phase
    # -----------------------------
    def _cornucopia_phase(self):
        if self._cornucopia_run:
            return
        self._cornucopia_run = True
        self._log("--- Cornucopia (Bloodbath) ---")
        tribs = self.alive_tributes()
        self.rng.shuffle(tribs)

        # Each tribute chooses an action: fight, grab, flee
        actions_summary: List[str] = []
        # Track those already engaged in fights to avoid double-processing
        engaged = set()

        for t in tribs:
            if not t.alive or t.key in engaged:
                continue
            roll = self.rng.random()
            if roll < 0.30 and len(self.alive_tributes()) > 1:
                # Attempt fight
                opponents = [o for o in self.alive_tributes() if o.key != t.key and o.key not in engaged]
                if opponents:
                    opp = self.rng.choice(opponents)
                    engaged.add(t.key)
                    engaged.add(opp.key)
                    # Decide winner
                    winner, loser = (t, opp) if self.rng.random() < 0.5 else (opp, t)
                    # Winner may grab an item
                    loot = self.rng.choice(CORNUCOPIA_ITEMS)
                    winner.inventory.append(loot)
                    loser.alive = False
                    winner.kills += 1
                    actions_summary.append(f"{winner.name} overpowers {loser.name} at the Cornucopia and claims a {loot}.")
                else:
                    # fallback to grab
                    item = self.rng.choice(CORNUCOPIA_ITEMS)
                    t.inventory.append(item)
                    actions_summary.append(f"{t.name} hastily grabs a {item}.")
            elif roll < 0.70:
                # Grab supplies
                grabs = self.rng.randint(1, 2)
                items = self.rng.sample(CORNUCOPIA_ITEMS, grabs)
                for it in items:
                    t.inventory.append(it)
                items_str = ", ".join(items)
                actions_summary.append(f"{t.name} secures {items_str} before retreating.")
            else:
                # Flee
                actions_summary.append(f"{t.name} flees the Cornucopia empty-handed.")
        for line in actions_summary:
            self._log(line)

        fallen = [t for t in self.tributes if not t.alive]
        if fallen:
            self._log("\nFallen in the Bloodbath:")
            for f in fallen:
                self._log(f" - {f.name}")

    # -----------------------------
    # Day/Night Simulation
    # -----------------------------
    def _simulate_day(self):
        self._log(f"\n--- Day {self.day_count} ---")
        self._run_event_block(DAY_EVENTS, "day")

    def _simulate_night(self):
        self._log(f"\n*** Night {self.day_count} ***")
        self._run_event_block(NIGHT_EVENTS, "night")

    def _run_event_block(self, event_pool, phase):
        # Determine number of events to attempt (bounded)
        alive = self.alive_tributes()
        if not alive:
            return
        events_to_run = min(len(alive), self.rng.randint(1, 3))
        for _ in range(events_to_run):
            alive = self.alive_tributes()
            if len(alive) <= 1:
                break
            event_func = self.rng.choice(event_pool)
            narrative = event_func(alive, self.rng)
            for line in narrative:
                if line:
                    self._log(line)
        # Fallen tributes recap
        fallen = [t for t in self.tributes if not t.alive and f"(Fallen logged {t.key})" not in t.__dict__]
        if fallen:
            self._log("\nFallen this phase:")
            for f in fallen:
                self._log(f" - {f.name}")
                # mark that we logged them so they don't repeat
                f.__dict__[f"(Fallen logged {f.key})"] = True

    def _announce_winner(self):
        winners = self.alive_tributes()
        if winners:
            w = winners[0]
            self._log(f"\nVICTOR: {w.name} (District {w.district}, Kills: {w.kills})")
        else:
            self._log("\nNo victor emerged. The arena claims all.")

        self._log("\nFinal standings:")
        for t in sorted(self.tributes, key=lambda x: (-x.alive, -x.kills, x.name)):
            self._log(f" - {t}")

    def _log_intro(self):
        self._log("Welcome to the Hunger Bens Simulation!")
        self._log(
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
            run_simulation(seed=seedin, max_days=maxday, verbose=verb)
            print("\nSimulation complete.")
        elif again == 'n':
            break
        else:
            print("Please enter 'y' or 'n'.")
    print("Thank you for using the Hunger Bens Simulator!")

if __name__ == "__main__":
    # You can adjust the seed for reproducibility
    seedin = input("Enter a seed (or leave blank for random): ")
    seedin = int(seedin) if seedin.isdigit() else None
    maxday = input("Enter max days (default 30): ")
    maxday = int(maxday) if maxday.isdigit() else 30
    verb = input("Verbose output? (y/n, default y): ").lower() != 'n'
    run_simulation(seed=seedin, max_days=maxday, verbose=verb)
    print("\nSimulation complete.")
    print("You can rerun with the same seed for identical results.")
    print(seedin if seedin is not None else "Random seed used.")
    askagain()