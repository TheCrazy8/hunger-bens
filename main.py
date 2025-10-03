import random
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional

# -----------------------------
# Data Setup
# -----------------------------
# Added age so the original loop (if you keep it) won't break.
# You can expand this dictionary with more "bens" or other tributes.
dicty: Dict[str, Dict[str, str]] = {
    "ben1": {"name": "Ben", "gender": "male", "age": 19},
    "ben2": {"name": "Ben's Mom", "gender": "female", "age": 45},
    "ben3": {"name": "BenBot 3000", "gender": "object", "age": 2},  # Programmatic age :)
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
    alive: bool = True
    kills: int = 0
    inventory: List[str] = field(default_factory=list)

    def __str__(self):
        status = "Alive" if self.alive else "Fallen"
        return f"{self.name} ({status}, Kills: {self.kills})"


# -----------------------------
# Arena Events Configuration
# -----------------------------
# Event functions take (alive_tributes, rng) and return a narrative string list.
# They are responsible for marking tributes dead or modifying state.
def event_find_supplies(tributes: List[Tribute], rng: random.Random) -> List[str]:
    t = rng.choice(tributes)
    item = rng.choice(["rope", "knife", "medical kit", "berries", "canteen"])
    t.inventory.append(item)
    return [f"{t.name} finds a {item}."]

def event_small_skirmish(tributes: List[Tribute], rng: random.Random) -> List[str]:
    if len(tributes) < 2:
        return []
    a, b = rng.sample(tributes, 2)
    winner, loser = (a, b) if rng.random() < 0.5 else (b, a)
    loser.alive = False
    winner.kills += 1
    return [f"{winner.name} ambushes {loser.name}. {loser.name} is eliminated."]

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
    hazard = rng.choice(["acid rain", "falling debris", "poison mist", "lava vent"])
    if rng.random() < 0.35:
        t.alive = False
        return [f"{t.name} is overcome by {hazard}."]
    return [f"{t.name} narrowly escapes a patch of {hazard}."]

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
            )
            for k, v in tribute_data.items()
        ]
        self.log: List[str] = []

    def alive_tributes(self) -> List[Tribute]:
        return [t for t in self.tributes if t.alive]

    def run(self):
        self._log_intro()
        while len(self.alive_tributes()) > 1 and self.day_count < self.max_days:
            self.day_count += 1
            self._simulate_day()
            if len(self.alive_tributes()) <= 1:
                break
            self._simulate_night()

        self._announce_winner()
        return self.log

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
            self._log(f"\nVICTOR: {w.name} (Kills: {w.kills})")
        else:
            self._log("\nNo victor emerged. The arena claims all.")

        self._log("\nFinal standings:")
        for t in sorted(self.tributes, key=lambda x: (-x.alive, -x.kills, x.name)):
            self._log(f" - {t}")

    def _log_intro(self):
        self._log("Welcome to the Hunger Bens Simulation!")
        self._log(f"Tributes entering the arena: {', '.join(t.name for t in self.tributes)}\n")

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

if __name__ == "__main__":
    # You can adjust the seed for reproducibility
    run_simulation(seed=None, max_days=25, verbose=True)