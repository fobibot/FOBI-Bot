import RPi.GPIO as GPIO
import time
import pyaudio
import wave

CHUNK = 512#1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25,GPIO.HIGH)
time.sleep(1)
GPIO.output(25,GPIO.LOW)
try:
    while True:
        input_state = GPIO.input(23)
        if not input_state:
            print("Pushed")
            stream.start_stream()
            frames = []
            GPIO.output(25,GPIO.HIGH)
            while not input_state:
                input_state = GPIO.input(23)
                data = stream.read(CHUNK, exception_on_overflow = False)
                frames.append(data)
                #print("* recording")
            GPIO.output(25,GPIO.LOW)
            #print('Record Done')
            stream.stop_stream()
            #stream.close()
            #p.terminate()

            wf = wave.open('wav/'+str(int(time.time()))+'.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            wf = wave.open('wav/last.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
#except KeyboardInterrupt:
finally:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    wf.close()
    stream.stop_stream()
