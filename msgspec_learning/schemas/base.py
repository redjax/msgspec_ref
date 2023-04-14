from msgspec import Struct


class BaseStruct(Struct):
    """
    Base msgpack Struct object. Defines functions &
    common defaults for inherited classes.

    Has functions like to_dict(), which returns the class
    instance as a Python dict.
    """

    def to_dict(self) -> dict:
        """
        Return struct as dict object.

        _self_dict is created by an inline for loop. The loop
        works by iterating over fields in self.__struct_fields__,
        which are class vars (i.e. self.name, self.id, etc).

        As the loop runs, dict items are created by using the attribute
        name as the key, and accessing that attribute's value from self.

        Outputs a dict.
        """
        ## Oneliner for loop. Define f as the self.x attribute.
        #  Loops over self.__struct_fields__ (class vars), then
        #  accesses k,v pair. Output of loop is a dict.
        _self_dict = {f: getattr(self, f) for f in self.__struct_fields__}

        return _self_dict
