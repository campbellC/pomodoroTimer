import soundfile
import sounddevice
class Alarm:
    def playAlarm(self): #Currently this only plays one sound, options to come later
        data, fs = soundfile.read("/System/Library/Sounds/Glass.aiff")
        sounddevice.play(data, fs, blocking=True)
