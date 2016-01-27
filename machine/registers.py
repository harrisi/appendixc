import sys
from machine import util

class Registers(dict):
    # This should be a "safe" set; registers can't have values out of
    # range (-128, 127), and can only be 0x1-0xF
    def __setitem__(self, key, item):
        if type(key) is list:
            key = util.getValFromBits(key)
        if type(key) != int:
            sys.exit("""ERROR: Register must be integer value.
Value given: {}""".format(repr(key)))
        if not(0 <= key <= 0xF):
            sys.exit("ERROR: Register " + key + " out of range.")
        if not(-(2 ** 7) <= item <= ((2 ** 7) - 1)):
            print('*** WARNING: item out of range (overflow not yet implemented)')
        self.__dict__[key] = item

    def __getitem__(self, key):
        if type(key) is list:
            key = util.getValFromBits(key)
        return self.__dict__[key]

    # Would be nice to have a better display output for debugging.
    def __repr__(self):
        return repr(self.__dict__)

    # This could potentially always just show 15 for now.
    def __len__(self):
        return len(self.__dict__)

    # There's no real reason to allow deletion, I suppose.
    # This could just be a `pass`.
    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    # This could potentially be quicker to just see if 0 <= k <= 0xF?
    def has_key(self, k):
        return self.__dict__.has_key(k)

    def pop(self, k, d=None):
        return self.__dict__.pop(k, d)

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict):
        return cmp(self.__dict__, dict)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

    bits = 8
