import random
from dataclasses import dataclass
from typing import Dict, Optional, List, Union

from utils import read_yaml


@dataclass
class Trait:
    name: str
    weight: Optional[float] = 1
    bonus: Optional[str] = None
    status: Optional[Dict] = None
    description: Optional[str] = None
    flavor_text: Optional[str] = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Trait) and self.name == other.name

    def __contains__(self, item_name: str):
        return item_name == self.name


class TraitsOptions(list):
    def __init__(self, traits_list: List[Trait], unique=True):
        traits_dict = {trait.name: trait for trait in traits_list}
        super().__init__(traits_dict.values() if unique else traits_list)
        self.traits_dict = traits_dict
        self.is_locked = False

    def __getitem__(self, name: str) -> Optional[Trait]:
        return self.traits_dict.get(name)

    def __contains__(self, trait_name: str) -> bool:
        return trait_name in self.traits_dict

    def lock(self):
        self.is_locked = True

    def append(self, element):
        if self.is_locked:
            return
        assert isinstance(element, Trait)
        super().append(element)
        self.traits_dict[element.name] = element

    def update(self, other, lock: bool = True):
        if self.is_locked:
            return
        for trait in other:
            self.traits_dict[trait.name] = trait
        self.clear()
        self.extend(self.traits_dict.values())
        if lock:
            self.lock()

    def get_options_probabilities(self):
        options = []
        for trait in self:
            weight = trait.weight
            if weight >= 1:
                options.extend([trait] * weight)
            else:
                t = random.uniform(0.0, 1.0)
                if t <= weight:
                    options.append(trait)

        return TraitsOptions(options, unique=False)

    def choice(self) -> Trait:
        return random.sample(self, 1)[0]

    def choose_trait(self) -> Trait:
        return self.get_options_probabilities().choice()

    def get_bonuses(self) -> List[str]:
        return [trait.bonus for trait in self if trait.bonus is not None]


def parse_trait(trait: Union[str, Dict]) -> Trait:
    if isinstance(trait, str):
        return Trait(name=trait)
    name = list(trait.keys())[0]
    return Trait(name=name, **trait[name])


def load_options(traits_list: List[Union[str, Dict]]) -> TraitsOptions:
    return TraitsOptions(list(map(lambda l: parse_trait(l), traits_list)))


class PhysicalAppearance:
    def __init__(self, data: Union[str, Dict] = r"..\data\physical-appearance\basics.yaml"):
        data_dict = read_yaml(data) if isinstance(data, str) else data
        self.__dict__ = {key: load_options(values) for key, values in data_dict.items()}

    def update(self, other):
        for key, traits_options in other.__dict__.items():
            self.__dict__[key] = traits_options

    def choose_traits(self) -> Dict:
        return {
            trait: trait_options.choose_trait()
            for trait, trait_options in self.__dict__.items()
        }
