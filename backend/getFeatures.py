import librosa
import numpy

# make this into a class!


def getBeats(path):
#	import librosa, numpy
	y, sr = librosa.load(path)

	hop_length = 64
	tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)

	print 'Estimated tempo: %0.2f beats per minute' % tempo

	beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)

	#print 'Saving output to beat_times.csv'
	#librosa.output.times_csv('beat_times.csv', beat_times)
	#numpy.savetxt("beats.csv", beat_times, delimiter=",")
	print beat_times

def getTuning(filename):
	y, sr = librosa.load(filename)

	print "separating harmonic component ..." 
	y_harm = librosa.effects.harmonic(y)
	print "esimating tuning ..."
	tuning = librosa.feature.estimate_tuning(y=y_harm, sr=sr)

	print('{:+0.2f} cents'.format(100 * tuning))
	return tuning

def getMFCC(filename):
	y, sr = librosa.load(filename)
	
	mfcc = librosa.feature.mfcc(y=y, sr=sr)
	mfcc_delta = librosa.feature.delta(mfcc)
	mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

	r = [mfcc, mfcc_delta, mfcc_delta2]
	return r
	
def getDuration(filename):
	y, sr = librosa.load(filename)

	duration = librosa.core.get_duration(y=y, sr=sr)
	print duration
	return duration


# not working!!
def getPitch(filename):
	y, sr = librosa.load(filename)
	hopLen = 64

	pitch, magnitudes = librosa.core.piptrack(y=y, sr=sr, hop_length=hopLen)
	return pitch

"""
Name - string
duration
tempo
sampleRate
tatumsStart - array
sectionStart - array
sectionConfidence - array
keyConf
beatsStart - array
segmentLoudnessStart - array
tatumsConfidence - array
segmentLoudnessTime - array
segmentTimbre - array of tuples
key - int
beatsConfidence - array
barsConfidence - array
segmentStart - array
segmentConfidence - array
segmentPitches - array
segmentLoudness - array
simeSigConf 
barsStart - array
timeSig - int 


"""

