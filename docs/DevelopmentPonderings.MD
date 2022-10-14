# Ponderings on improvements and implementations
___
###Tackling the serial transfer timing problem to allow for link cable over network connection
I feel that we may be able to tackle this issue by tricking both games into thinking they are in slave mode
and then having an asynchronous master clock that keeps them both in sync.
___
###IPS Patching and Rom hell
The fact that its 2022 and we still need 101 roms to play any collection of rom hacks is absurd. 
my proposal is a mod loader style patcher with compatibility reports et
I am hope this will allow for mini patches that target specific parts of the games allowing for "Mod packs" to be made
To solve some of the inevitable problems, I plan to implement a jump system, so it can access the appropriate patched code
without it needing to be a part of the rom itself. this in turn hopefully should allow for the creation of the 
compatibility reports, as we would be mapping jumps to the same location, ultimately revealing a conflict, 
some of which can be resolved with ordering, others will be incompatible.
___