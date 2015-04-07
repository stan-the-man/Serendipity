import numpy, librosa

filename = "test30.mp3"

y, sr = librosa.load(filename)

hop_length = 64
'''
print "separating harmonic component ..." 
y_harm = librosa.effects.harmonic(y)
tuning = librosa.feature.estimate_tuning(y=y_harm, sr=sr)

print('{:+0.2f} cents'.format(100 * tuning))
print tuning



mfcc = librosa.feature.mfcc(y=y, sr=sr)
mfcc_delta = librosa.feature.delta(mfcc)

print mfcc
print "\n\n----------delta---------\n\n"
print mfcc_delta
'''


print librosa.core.get_duration(y=y, sr=sr)
