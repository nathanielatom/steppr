import argparse
import gpiozero
from mido import MidiFile
import librosa

stepper_pin = "GPIO12" # supports hardware PWM
direction_pin = "GPIO25"

parser = argparse.ArgumentParser(description='Play MIDI files on a stepper motor.')
parser.add_argument('filename', type=str, help="The MIDI file.")
parser.add_argument('--channel', '-ch', type=int, default=0, help="Which MIDI channel to play (in all tracks).")
parser.add_argument('--rests', '-r', action='store_true', default=False, help="Whether to play rests or not.")

if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.filename
    channel = args.channel
    rests = args.rests
    duty_cycle = 0.2

    midi = MidiFile(filename)
    director = gpiozero.DigitalOutputDevice(pin=direction_pin,
                                            initial_value=0)
    stepper = gpiozero.PWMOutputDevice(pin=stepper_pin,
                                       initial_value=0,
                                       frequency=100)

    for msg in midi.play():
        if msg.type == 'note_on' and msg.channel == channel:
            stepper.value = duty_cycle
            frequency = librosa.midi_to_hz(msg.note)
            stepper.frequency = frequency
            # duration = msg.time # s
            # amplitude = msg.velocity
        if rests and msg.type == 'note_off' and msg.channel == channel:
            stepper.value = 0
    stepper.value = 1
