# Web adaptation of Hunger Bens Simulator for Pyodide
# Minimal extraction: import classes from main if available, else fallback (dup minimal run_simulation).
# NOTE: In GitHub Pages Pyodide environment, we load this file after pyodide initialization.

import json
from typing import Optional, Dict, Any
from datetime import datetime
import random

# We cannot rely on OS-specific code; re-define minimal Tribute and simulator subset.
class Tribute:
    def __init__(self, key: str, name: str, gender: str, age: int, district: int):
        self.key = key
        self.name = name
        self.gender = gender
        self.age = age
        self.district = district
        self.alive = True
        self.kills = 0
        self.inventory = []
        self.status = []
        self.morale = 5
        self.notoriety = 0
        self.cause_of_death = None
    def adjust_morale(self, delta: int):
        self.morale = max(0, min(10, self.morale + delta))
    def add_status(self, tag: str):
        if tag not in self.status:
            self.status.append(tag)

# Simplified event set for web (keep core flavor, fewer branches for size)
SUPPLY_ITEMS = ["berries","bandages","water pouch","protein bar","egg"]
WEAPONS = ["knife","bow","spear","machete","trident"]

WEAPON_VERBS = {"knife": "slashes", "bow": "shoots", "spear": "impales", "machete": "cleaves", "trident": "skewers"}

DEFAULT_ROSTER = {
    "trib1": {"name": "Ben", "gender": "male", "age": 16, "district": 1},
    "trib2": {"name": "BenBot", "gender": "object", "age": 2, "district": 3},
    "trib3": {"name": "Katniss", "gender": "female", "age": 17, "district": 11},
    "trib4": {"name": "Peeta", "gender": "male", "age": 17, "district": 12},
}

class WebSimulator:
    def __init__(self, tribute_data: Dict[str, Dict[str, Any]], seed: Optional[int], max_days: int, strict_shutdown: Optional[int], log_callback):
        self.rng = random.Random(seed)
        self.seed = seed
        self.max_days = max_days
        self.strict_shutdown = strict_shutdown
        self.log_callback = log_callback
        self.day_count = 0
        self.tributes = [Tribute(k, v.get("name", k), v.get("gender", "unknown"), int(v.get("age", 18)), int(v.get("district", 1))) for k,v in tribute_data.items()]
        self.log = []

    def alive(self):
        return [t for t in self.tributes if t.alive]

    def _log(self, msg: str):
        self.log.append(msg)
        if self.log_callback:
            self.log_callback(msg)

    def run(self):
        self._log(f"Web Simulation start: tributes={len(self.tributes)}")
        while len(self.alive()) > 1 and self.day_count < self.max_days:
            self.day_count += 1
            self._log(f"--- Day {self.day_count} ---")
            self._run_day_events()
            if self.strict_shutdown and self.day_count >= self.strict_shutdown and len(self.alive()) > 2:
                self._log("Early shutdown triggered.")
                break
        self._announce()
        return self.log

    def _run_day_events(self):
        events = self.rng.randint(2,4)
        for _ in range(events):
            alive = self.alive()
            if len(alive) <= 1: break
            choice = self.rng.random()
            if choice < 0.35:
                self._event_find_supplies(alive)
            elif choice < 0.65:
                self._event_skirmish(alive)
            else:
                self._event_environment(alive)

    def _event_find_supplies(self, alive):
        t = self.rng.choice(alive)
        item = self.rng.choice(SUPPLY_ITEMS + WEAPONS)
        t.inventory.append(item)
        t.adjust_morale(+1)
        self._log(f"{t.name} finds a {item}.")

    def _event_skirmish(self, alive):
        if len(alive) < 2: return
        a,b = self.rng.sample(alive,2)
        prob_a = 0.5 + (a.morale - b.morale)*0.04
        prob_a = max(0.1, min(0.9, prob_a))
        winner, loser = (a,b) if self.rng.random() < prob_a else (b,a)
        weapon = None
        usable = [it for it in winner.inventory if it in WEAPONS]
        if usable:
            weapon = self.rng.choice(usable)
        verb = WEAPON_VERBS.get(weapon,"defeats") if weapon else "overpowers"
        loser.alive = False
        loser.cause_of_death = f"defeated by {winner.name}"
        winner.kills += 1
        winner.adjust_morale(+1)
        if weapon:
            self._log(f"{winner.name} {verb} {loser.name} with a {weapon}. {loser.name} falls.")
        else:
            self._log(f"{winner.name} {verb} {loser.name}. {loser.name} falls.")

    def _event_environment(self, alive):
        t = self.rng.choice(alive)
        hazard = self.rng.choice(["quicksand","acid rain","wild animal","flash flood"]) 
        chance = 0.25 - (t.morale - 5)*0.02
        if self.rng.random() < chance:
            t.alive = False
            t.cause_of_death = f"{hazard}"
            self._log(f"{t.name} is lost to {hazard}.")
        else:
            t.adjust_morale(-1)
            self._log(f"{t.name} evades {hazard}.")

    def _announce(self):
        winners = self.alive()
        if winners:
            if len(winners) > 1:
                self._log("Multiple survivors remain.")
            else:
                w = winners[0]
                self._log(f"VICTOR: {w.name} (Kills {w.kills})")
        else:
            self._log("All tributes have fallen.")
        self._log("Standings:")
        for t in sorted(self.tributes, key=lambda x: (-x.alive, -x.kills, x.name)):
            status = "Alive" if t.alive else f"Fallen ({t.cause_of_death})"
            self._log(f" - {t.name}: {status}, Kills {t.kills}")


def run_simulation_web(seed: Optional[int], max_days: int, strict_shutdown: Optional[int], roster_json: Optional[str], log_callback):
    tribute_data = DEFAULT_ROSTER
    if roster_json:
        try:
            data = json.loads(roster_json)
            roster: Dict[str, Dict[str, Any]] = {}
            if isinstance(data, list):
                for idx, entry in enumerate(data, start=1):
                    if not isinstance(entry, dict): continue
                    k = entry.get("key") or f"cust{idx}"
                    roster[k] = {
                        "name": entry.get("name", k),
                        "gender": entry.get("gender","unknown"),
                        "age": entry.get("age",18),
                        "district": entry.get("district", (idx % 12)+1)
                    }
            elif isinstance(data, dict):
                for k,v in data.items():
                    if isinstance(v, dict):
                        roster[k] = {
                            "name": v.get("name", k),
                            "gender": v.get("gender","unknown"),
                            "age": v.get("age",18),
                            "district": v.get("district",1)
                        }
            if roster:
                tribute_data = roster
        except Exception as e:
            log_callback(f"Roster parse error: {e}; using default roster.")
    sim = WebSimulator(tribute_data, seed, max_days, strict_shutdown, log_callback)
    return sim.run()
