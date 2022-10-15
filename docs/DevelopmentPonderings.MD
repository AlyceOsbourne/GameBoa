# Discussion about improvements and implementation techniques
This is a list of improvement and implementation ideas that me and PedanticHacker are currently discussing.

### Serial transfer timing issue in cable link emulation over network connection
We may be able to tackle this issue by tricking two linked games into
thinking they are in slave mode, in which an asynchronous master clock
keeps them both in perfect sync.

### ROM hell and in-memory IPS patching
It is required to individually load all the ROM patches to play games
bundled as a game collection. Therefore, a game collection of 101 games
requires all 101 ROM patches to be loaded, because loading just one huge
ROM patch currently doesn't work.

And to make this work, we will develop an in-memory IPS patcher that
produces a compatibility issue report for such game collection ROMs.
This patcher will enable mini patches to target specific parts of games
in game collections, allowing for *ROM patch packs* to be developed and
used.

Then, to solve some inevitable issues having such a patcher, we plan to
develop a jump system that accesses specific code of a ROM patch without
it needing to be a part of the ROM patch itself. This should allow for
the creation of the aforementioned compatibility issue reports as memory
jumps will be mapped to the same memory location, ultimately revealing a conflict, where some of which will be easily resolved with ordering,
while others deemed incompatible.
