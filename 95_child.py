import random
import time
from datetime import datetime, timedelta

class Child:
    """
    Represents a child with various attributes that change over time.
    The core logic for a child's needs and development is encapsulated here.
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hunger = 50  # 0 is full, 100 is starving
        self.energy = 50  # 0 is exhausted, 100 is full of energy
        self.happiness = 75  # 0 is miserable, 100 is ecstatic
        self.knowledge = 0  # Accumulated knowledge points
        self.trust_level = 75  # 0 is no trust, 100 is absolute trust

    def __str__(self):
        return f"--- {self.name} (Age: {self.age}) ---\nHunger: {self.hunger}%\nEnergy: {self.energy}%\nHappiness: {self.happiness}%\nKnowledge: {self.knowledge}\nTrust: {self.trust_level}%"

    def update_stats(self):
        """Simulates the passage of time and its effect on the child's stats."""
        self.hunger = min(100, self.hunger + random.randint(5, 15))
        self.energy = max(0, self.energy - random.randint(5, 15))
        self.happiness = max(0, self.happiness - random.randint(2, 8))
        # Trust can decay slowly if needs are not met
        if self.hunger > 80 or self.energy < 20:
            self.trust_level = max(0, self.trust_level - random.randint(5, 10))

class Parent:
    """
    Represents the user, the parent, trying to raise the child.
    Manages resources and makes decisions.
    """
    def __init__(self, name, patience=100, money=1000):
        self.name = name
        self.patience = patience  # 0 is stressed out, 100 is zen
        self.money = money
        self.energy = 75 # Parent's own energy

    def __str__(self):
        return f"--- {self.name} (Parent) ---\nPatience: {self.patience}%\nEnergy: {self.energy}%\nMoney: \${self.money}"

class Game:
    """
    The main game engine that orchestrates the simulation.
    """
    def __init__(self):
        print("Welcome to the 'Raising Kids' Simulator!")
        child_name = input("Enter your child's name: ")
        child_age = int(input(f"Enter {child_name}'s starting age: "))
        self.child = Child(child_name, child_age)
        self.parent = Parent(input("Enter your name (the parent's): "))
        self.game_over = False
        self.day = 1

    def display_status(self):
        """Prints the current status of parent and child."""
        print("\n" + "="*40)
        print(f"--- Day {self.day} ---")
        print(self.parent)
        print(self.child)
        print("="*40 + "\n")

    def handle_event(self):
        """Presents a random parenting event and handles the choice."""
        events = {
            "tantrum": {
                "description": f"{self.child.name} is throwing a tantrum in the middle of the grocery store!",
                "choices": {
                    "1": {"action": "Give in and buy the candy", "effect": lambda: self._apply_effect(child_happiness=20, parent_money=-10, parent_patience=-5)},
                    "2": {"action":
