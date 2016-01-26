# Safe set
    * I need a better way to set registers values. I suppose it needs to be agnostic as to how it is stored internally and then just choose how to display or use them at will. Any addition will just truncate to 8 bits.
    * Oh, swaggy. intToBits already truncates, so I can just always use `util.intToBits(n, b)` to keep it at `b` bits internally. This should work alright.
    * This means I just need to have a couple functions added for interpreting bit values in twos complement and floating point (which also needs a helper function for excess notation).

# Mass storage
    * This will (to be "nice") require a full bus for peripheral communication. This will definitely require a bit more reading and studying. A much simpler solution would to just have mass storage be a dictionary of infinite size that I can write to. However, this wouldn't be very helpful as time moves on. Ideally I would have a number of classes implementing various storage devices, each having their own timing and everything. This would be useful as the project continues.

# Peripherals
    * Peripherals will go along with the above. I'll need a bus and device drivers and everything for this. This will probably be a lot of work, but would be very interesting.

# Operating system
    * A full blown (well, not really; "A very simplistic" would be a better description) operating system would be pretty sweet. I would start to need to either write reasonably complex systems for a dispatcher or scheduler to have any use, or I could have quantums based on some amount of machine cycles instead, but this also comes with it's fair share of problems.
