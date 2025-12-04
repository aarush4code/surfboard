import array, time
from machine import Pin
import rp2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(25))
sm.active(1)

NUM_LEDS = 3
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

for i in range(10):
    ar[0] = (0 << 16) | (8 << 8) | 0   
    ar[1] = (8 << 16) | (0 << 8) | 0  
    ar[2] = (0 << 16) | (0 << 8) | 8  
    sm.put(ar) 
    time.sleep_ms(300)

    ar[0] = ar[1] = ar[2] = 0
    sm.put(ar)
    time.sleep_ms(300)