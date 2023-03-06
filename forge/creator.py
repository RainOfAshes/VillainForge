import os
from typing import Optional, Union, Dict

from characters import Body, Character
from traits import Trait, load_options, PhysicalAppearance, TraitsOptions
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

    def get_fighting_class(self, race_dict: Dict) -> Trait:
        fighting_classes_file = os.path.join(self.fighting_classes_dir, 'classes_list.yaml')
        fighting_classes_list = read_yaml(fighting_classes_file)
        fighting_classes_options = load_options(fighting_classes_list)

        races_fighting_classes = load_options(race_dict['fighting_class'])
        fighting_classes_options.update(races_fighting_classes)

        return fighting_classes_options.choose_trait()

    def read_race_file(self, race) -> Dict:
        race_file = f"{race.name}.yaml"
        return read_yaml(os.path.join(self.races_dir, race_file))

    def get_special_features(self, race_dict: Dict) -> TraitsOptions:
        race_feature = load_options(race_dict['special_features']).choose_trait()
        features_file = os.path.join(self.data_dir, 'physical-appearance', 'special_features.yaml')
        neutral_feature = load_options(read_yaml(features_file)).choose_trait()
        return TraitsOptions([neutral_feature, race_feature])

    def get_physical_appearance(self, race_dict) -> PhysicalAppearance:
        physical_appearance = PhysicalAppearance()
        race_physical_appearance = PhysicalAppearance(race_dict['physical_appearance'])
        physical_appearance.update(race_physical_appearance)
        return physical_appearance

    def get_body(self, race_dict: Dict) -> Body:
        physical_appearance = self.get_physical_appearance(race_dict)
        physical_traits = physical_appearance.choose_traits()
        return Body(**physical_traits)

    def create_character(self, race: Optional[Union[str, Trait]] = None,
                         fighting_class: Optional[Union[str, Trait]] = None) -> Character:
        race = Trait(name=race) if isinstance(race, str) else race or self.get_race()
        race_dict = self.read_race_file(race)

        body = self.get_body(race_dict)

        special_features = self.get_special_features(race_dict)
        fighting_class = (Trait(name=fighting_class)
                          if isinstance(fighting_class, str)
                          else fighting_class or self.get_fighting_class(race_dict))

        character = Character(race=race, fighting_class=fighting_class,
                              body=body, special_features=special_features)
        return character


if __name__ == "__main__":
    folder = r"C:\Users\kashe\PycharmProjects\VillainForge\data"
    creator = CharacterCreator(folder)
    character = creator.create_character()

