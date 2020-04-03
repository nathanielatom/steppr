import sys
import gpiozero
from mido import MidiFile
import librosa

stepper_pin = "GPIO12" # supports hardware PWM
direction_pin = "GPIO25"

if __name__ == '__main__':
    filename = sys.argv[-1]
    channel = 0
    duty_cycle = 0.2

    midi = MidiFile(filename)
    director = gpiozero.DigitalOutputDevice(pin=direction_pin,
                                            initial_value=0)
    stepper = gpiozero.PWMOutputDevice(pin=stepper_pin,
                                       initial_value=0,
                                       frequency=0)

    stepper.value = duty_cycle
    for msg in midi.play():
        if msg.type == 'note_on' and msg.channel == channel:
            frequency = librosa.midi_to_hz(msg.note)
            stepper.frequency = frequency
            # duration = msg.time # s
            # amplitude = msg.velocity
    stepper.value = 1
