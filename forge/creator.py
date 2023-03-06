import os
from typing import Optional, Union, Dict

from character import Body
from traits import Trait, load_options, PhysicalAppearance
from utils import read_yaml


class CharacterCreator:
    def __init__(self, data_dir: str = r"../data"):
        self.data_dir = data_dir
        self.races_dir = os.path.join(self.data_dir, 'races')

        self.fighting_classes_dir = os.path.join(self.data_dir, 'fighting_class')

    def get_race(self) -> Trait:
        races_file = os.path.join(self.races_dir, 'races_list.yaml')
        races_list = read_yaml(races_file)
        races_options = load_options(races_list)
        return races_options.choose_trait()

    def read_race_file(self, race) -> Dict:
        race_file = f"{race.name}.yaml"
        return read_yaml(os.path.join(self.races_dir, race_file))

    def get_physical_appearance(self, race_dict) -> PhysicalAppearance:
        physical_appearance = PhysicalAppearance()
        race_physical_appearance = PhysicalAppearance(race_dict['physical_appearance'])
        physical_appearance.update(race_physical_appearance)
        return physical_appearance

    def create_character(self, race: Optional[Union[str, Trait]] = None,
                         fighting_class: Optional[Union[str, Trait]] = None):
        race = Trait(name=race) if isinstance(race, str) else race or self.get_race()
        race_dict = self.read_race_file(race)
        physical_appearance = self.get_physical_appearance(race_dict)
        physical_traits = physical_appearance.choose_traits()
        body = Body(**physical_traits)
        return body


if __name__ == "__main__":
    folder = r"C:\Users\kashe\PycharmProjects\VillainForge\data"
    creator = CharacterCreator(folder)
    body = (creator.create_character(race='elf'))
    print(body)


