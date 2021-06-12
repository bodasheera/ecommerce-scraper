from typing import List

def get_entity(base):

    class Entity(base):

        def __init__(self, name, path) -> None:
            super().__init__(path)
            self.name = name

    return Entity