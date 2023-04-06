# otf_whisper
Some scripts for real-time transcription and translation using the whisper model.

## requirements
At present I am using the following packages at their latest version:

* [Speech Recognition](https://github.com/Uberi/speech_recognition) 
* [Faster Whisper](https://github.com/guillaumekln/faster-whisper)

(and all required dependencies)

## HOWTO

1. Install all the package and dependencies, plug in a microphone and have it recognized by pyaudio.
2. Edit the top of the otf_transcribe.py file.
3. Launch the script with python.

### 1. install packages and dependencies:

Usually, I recommend using the `pip3` command with the git repository.
```
pip3 install git+https://github.com/guillaumekln/faster-whisper.git
pip3 install git+https://github.com/Uberi/speech_recognition.git
```
The package can later be updated with:
```
pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/guillaumekln/faster-whisper.git
pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/Uberi/speech_recognition.git
```
That way should also bring up the correct dependencies.

Just in case make sure that the packages for microphone handling are installed: pyaudio and sounddevice (as far as I remember).


### 2. modifications to the script:

2.a. Use a proper model for your microphone:
```python
my_noise_duration = 5 # time to sort ambiant noise
my_phrase_time_limit = 4.5 # the most critical parameter
```
NOTE: removing the `adjust_for_ambient_noise` part will most certainly make your microphone fail.

The `phrase_time_limit` is also essential, if omitted, the script can produce "forever long" audio segment which will never be passed to the transcription engine. I recommend values from 3 seconds and higher.

2.b. Use a proper whisper model:
```python
my_model_size = "large-v2" # the model is downloaded on first time
my_language = "ja"
my_task = "translate"
my_beam_size = 6 # to limit the number of hallucinations
my_vad_filter = True # to limit the number of hallucinations
```
The parameter `my_model_size` really matters when performing translations. For Japanese, I recommend no less than the medium model.

Select the spoken language with `my_language`. Note that if you suddenly speak another language it will get translated to English too!

The parameter `my_task` dictates the behavior of the [Faster Whisper](https://github.com/guillaumekln/faster-whisper) engine: either a transcription or a translation, with `"translate"` or `"transcribe"`, respectively.

NOTE: Japanese transcriptions are on the spot for pronunciation, but Kanjis can be off! Believe me: I am not working in the field of fisherman's computer (漁師コンピュータ Ryōshi konpyūta) but on quantum computers (量子コンピューター Ryōshi konpyūtā)! :rofl:

The `my_beam_size` and `my_vad_filter` parameters are to fight against some audio problems and may be gone someday...

### 3. launch the script:

just do a simple:
```
python3 ./otf_transcribe.py
```

NOTE: the first time the script is launched it will download the corresponding model if it was not available.


## Work In Progress (future developments)

> "Currently I am fighting with hallucinations."

Ok, that sounds more dramatic than I wanted. What I mean is that the [whisper](https://github.com/openai/whisper) model produces imaginary text when its only input is background noise. This imaginary text is called hallucination.

There are several strategies to counter these hallucinations, but most fight on either eliminating noise or, in my case, removing empty segments.


## License

Dependencies have their own respective licensing.
Since the base is OpenAI's [whisper](https://github.com/openai/whisper) model and it is released under a MIT license, I will go for the same model for now.

otf_whisper is a collection of free script software released under the terms of the MIT license.
See the [License](LICENSE) file for more details.

