# openthrone
an open source throne-like game but its poorly written and made in python.

this is intended to be a skeleton frame to build a game with. i don't know game design so don't expect this to be a 'real' game.
this is also the first real thing i've done in python and have no knowledge of programming standard practice.
nuclear throne was too hard to mod due to it being closed source. i decided it would be easier to do this.

its buggy(graphically), its slow, but it does work.

right now the game has player classes, weapon classes, enemy classes, bullet classes. pickups still need to be added as well as
a level generator and levels themselves. the enemy also has no ai as i do not know how to do that yet. hit detection has not been
started but *should* be fairly easy to implement. there is also a built in system for projectiles to die as a form of memory 
management. menus also need to be added. the sprites are also temporary. the shooting mechanic works but it does not line up with
the mouse for some reason.

this project was started as a means to learn python and also because in the original nuclear throne, chickens time slow never
worked properly. it only actually changed the walk speed of enemies and did not slow their ai or slow the fuses on grenades. i
intend to have that mechanic work. i also intend to have this project be more easily modded by default.

this project has only ever been tested on my desktop and may or may not work on other boxes or operating systems. it works in
arch.

it has been uploaded for better version control and because i would appreciate some help in learning both python and github and 
with guidance on where to go from here.

EDIT #1: there is a simple framework being made for level generation. its going to be merged into the main script once it is done.
it is currently called level_gen_test.py and has some simple methods for making a 32x32 level with floors.
