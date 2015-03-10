import sys
import getopt

# We'll need the os module for file path manipulation
import os

# And numpy for some mathematical operations
import numpy as np

# Librosa for audio
import librosa

# matplotlib for displaying the output
import matplotlib.pyplot as plt
#%matplotlib inline

# and IPython.display for audio output
import IPython.display

def process(filename):
    bpm_file = open("upload/out.txt", "w")
    y, sr = librosa.load(filename)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=sr, hop_length=64)
    outstring = 'Estimated tempo:        %.2f BPM' % tempo
    out = str(outstring) + "\n"
    bpm_file.write(out)

    # 4. Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=64)
    librosa.output.times_csv('upload/beat_times.csv', beat_times)


def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

if __name__ == "__main__":
    main()