from abstract.event_manager import EventManager, Mods
from pygame import locals as const
from ship import Ship

# Missing Mouse button constants
const.MOUSEKEY_LEFT = 1
const.MOUSEKEY_MIDDLE = 2
const.MOUSEKEY_RIGHT = 3

const.MOUSEKEY_SCROLLUP = 4
const.MOUSEKEY_SCROLLDOWN = 5


# Start up our pause_handler
pause_handler = EventManager()

# Start up our game_handler
game_handler = EventManager()



@pause_handler.quit
@pause_handler.shortcut(Mods.META, const.K_q)
@pause_handler.shortcut(Mods.ALT, const.K_q)
@game_handler.quit
@game_handler.shortcut(Mods.META, const.K_q)
@game_handler.shortcut(Mods.ALT, const.K_q)
def quit(context):
    raise context.mediator.PopEvent()

@game_handler.keydown(const.K_SPACE)
def pause(context):
    context.mediator.pause()

@pause_handler.keydown(const.K_SPACE)
def unpause(context):
    raise context.mediator.ResumeEvent()


#################################################
# Ship Controls

# Player 1
@game_handler.keydown(const.K_d, const={'player': 1})
@game_handler.keydown(const.K_l, const={'player': 2})
@game_handler.keydown(const.K_RIGHT, const={'player': 3})
@game_handler.keydown(const.K_h, const={'player': 4})
def rotate_right(context, player):
    context.mediator.players[player].rotate(Ship.ROT_RIGHT)

@game_handler.keyup(const.K_d, const={'player': 1})
@game_handler.keyup(const.K_l, const={'player': 2})
@game_handler.keyup(const.K_RIGHT, const={'player': 3})
@game_handler.keyup(const.K_h, const={'player': 4})
def rotate_right_stop(context, player):
    context.mediator.players[player].rotate(Ship.ROT_RIGHT, stop=True)

@game_handler.keydown(const.K_a, const={'player': 1})
@game_handler.keydown(const.K_j, const={'player': 2})
@game_handler.keydown(const.K_LEFT, const={'player': 3})
@game_handler.keydown(const.K_f, const={'player': 4})
def rotate_left(context, player):
    context.mediator.players[player].rotate(Ship.ROT_LEFT)

@game_handler.keyup(const.K_a, const={'player': 1})
@game_handler.keyup(const.K_j, const={'player': 2})
@game_handler.keyup(const.K_LEFT, const={'player': 3})
@game_handler.keyup(const.K_f, const={'player': 4})
def rotate_left_stop(context, player):
    context.mediator.players[player].rotate(Ship.ROT_LEFT, stop=True)

@game_handler.keydown(const.K_w, const={'player': 1})
@game_handler.keydown(const.K_i, const={'player': 2})
@game_handler.keydown(const.K_UP, const={'player': 3})
@game_handler.keydown(const.K_t, const={'player': 4})
def move_up(context, player):
    context.mediator.players[player].move(Ship.MOV_FORWARDS)

@game_handler.keyup(const.K_w, const={'player': 1})
@game_handler.keyup(const.K_i, const={'player': 2})
@game_handler.keyup(const.K_UP, const={'player': 3})
@game_handler.keyup(const.K_t, const={'player': 4})
def move_up_stop(context, player):
    context.mediator.players[player].move(Ship.MOV_FORWARDS, stop=True)

@game_handler.keydown(const.K_s, const={'player': 1})
@game_handler.keydown(const.K_k, const={'player': 2})
@game_handler.keydown(const.K_DOWN, const={'player': 3})
@game_handler.keydown(const.K_g, const={'player': 4})
def move_down(context, player):
    context.mediator.players[player].move(Ship.MOV_BACKWARDS)

@game_handler.keyup(const.K_s, const={'player': 1})
@game_handler.keyup(const.K_k, const={'player': 2})
@game_handler.keyup(const.K_DOWN, const={'player': 3})
@game_handler.keyup(const.K_g, const={'player': 4})
def move_down_stop(context, player):
    context.mediator.players[player].move(Ship.MOV_BACKWARDS, stop=True)



#################################################
# Debug only code

DEBUG = False
if DEBUG:
    def locate_key(val):
        for key, value in const.__dict__.iteritems():
            if value == val and (key.startswith('K_') or key.startswith('KMOD')):
                print key

    @game_handler.event(const.KEYDOWN)
    def debug_keys(context):
        print '-' * 15
        print '-- Key'
        locate_key(context.event.key)
        print '-- Mod'
        locate_key(context.event.mod)
        print '-' * 15
