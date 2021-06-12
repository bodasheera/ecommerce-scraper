def get_entity(base):

    class Entity(base):
        name: str;

        def __init__(self, name, path, data_type=None) -> None:
            super().__init__(path, data_type)
            self.name = name

    return Entity