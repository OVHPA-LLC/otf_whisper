#!/usr/bin/env python3

from threading import Thread
from queue import Queue
import speech_recognition as sr
from faster_whisper import WhisperModel
from io import BytesIO

# speech_recognition parameters
my_noise_duration = 5 # time to sort ambiant noise
my_phrase_time_limit = 4.5 # the most critical parameter
# initialize speech_recognition
r = sr.Recognizer()
audio_queue = Queue()


# faster_whisper model
# the following are parameters
my_model_size = "large-v2" # the model is downloaded on first time
my_language = "ja"
my_task = "translate"
my_beam_size = 6 # to limit the number of hallucinations
my_vad_filter = True # to limit the number of hallucinations
# initialize faster_whisper model
model = WhisperModel(my_model_size, device="cuda", compute_type="int8_float16")

def recognize_worker():
  while True:
    audio = audio_queue.get()
#     speech_recognition implementation
#     (in case one wants to test it...)
#    push_text = r.recognize_whisper(audio,model=my_model_size,language=my_language,translate=True,beam_size=6)
#    print(">>> " + push_text)
#    audio_queue.task_done()

#    faster_whisper implementation
#    (more tunable, and faster...)
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = "SpeechRecognition_audio.wav"
    segments, _ = model.transcribe(wav_data,without_timestamps=True,language=my_language,task=my_task,beam_size=my_beam_size,vad_filter=my_vad_filter)
    for segment in segments:
      print(">>> " + segment.text)
    audio_queue.task_done()

# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
# Tuning the sample rate and chunk size has little  positive effect
#my_sample_rate = 16000
#my_chunk_size = 128
#with sr.Microphone(sample_rate=my_sample_rate,chunk_size=my_chunk_size) as source:
with sr.Microphone() as source:
    print(">>> ANALYSE NOISE <<<")
    # 5s noise analysis is not necessary (1 is enough) but in my case...
    r.adjust_for_ambient_noise(source,duration=my_noise_duration)
    print(">>> DONE! PROCESSING <<<")
    try:
        while True:
            audio_queue.put(r.listen(source,phrase_time_limit=my_phrase_time_limit))
    except KeyboardInterrupt:
        # interrupt using [ctrl]+C
        pass
# audio thread processing
audio_queue.join()
audio_queue.put(None)
recognize_thread.join()

