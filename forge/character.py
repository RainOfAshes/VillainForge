from dataclasses import dataclass
from traits import Trait


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
    def __init__(self, body: Body):
        self.body = body
