from dataclasses import dataclass

from traits import Trait, TraitsOptions


@dataclass
class Body:
    gender: Trait
    eyes: Trait
    age: Trait
    eyes: Trait
    height: Trait
    skin: Trait
    physique: Trait
    hair: Trait
    hair_color: Trait
    seduction: Trait
    voice: Trait


class Character:
    def __init__(self, race: Trait,
                 fighting_class: Trait,
                 body: Body, special_features: TraitsOptions):
        self.race = race
        self.fighting_class = fighting_class
        self.body = body
        self.special_features = special_features
