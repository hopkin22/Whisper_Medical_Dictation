# %% [markdown]
# Output File Path Define

# %%
#recorded_file='/Users/Ben/Desktop/New Recording 6.m4a'

import datetime
import os
import fnmatch
import json
from pydub import AudioSegment
import pyperclip

class CaseInsensitiveDict(dict):
                @classmethod
                def _k(cls, key):
                    return key.lower() if isinstance(key, str) else key

                def __init__(self, *args, **kwargs):
                    super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
                    self._convert_keys()
                def __getitem__(self, key):
                    return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
                def __setitem__(self, key, value):
                    super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
                def __delitem__(self, key):
                    return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
                def __contains__(self, key):
                    return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
                def has_key(self, key):
                    return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
                def pop(self, key, *args, **kwargs):
                    return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
                def get(self, key, *args, **kwargs):
                    return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
                def setdefault(self, key, *args, **kwargs):
                    return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
                def update(self, E={}, **F):
                    super(CaseInsensitiveDict, self).update(self.__class__(E))
                    super(CaseInsensitiveDict, self).update(self.__class__(**F))
                def _convert_keys(self):
                    for k in list(self.keys()):
                        v = super(CaseInsensitiveDict, self).pop(k)
                        self.__setitem__(k, v)


output_file='Untitled.mp3'
start = datetime.datetime.now()
import whisper
print("Current Time is %s" % start)
print("Loading Model....")
model = whisper.load_model("large-v2")
print("Model Loaded Successfully")

# %% [markdown]
# Find Recent Voice Recording

# %%

try:
    while True:
        trigger=input('Type "go" to run:\n------------------')

        if trigger=='go': 
            print("\nAnalyzing Audio...\n\n")
            # Opening JSON file
            with open('path_vars.json') as json_file:
                path_vars = json.load(json_file)

            PATH=path_vars["Recording_Path"]
            files=[PATH+'/'+j for j in os.listdir(PATH) if j != ".DS_Store"]

            files.sort(key=os.path.getctime,reverse=True)

            recorded_file=PATH+str('/'+os.listdir(PATH)[0])

            #print(files)

            mp4s=[]
            for file in files:
                if fnmatch.fnmatch(file, '*.m4a'):
                    mp4s.append(file)

            mp4s.sort(key=os.path.getmtime,reverse=True)




            recorded_file=(mp4s[0])
            print('Loading File Found:'+ recorded_file)

            # %% [markdown]
            # Convert to mp3 And put in Output File Destination

            # %%

            sound=AudioSegment.from_file(recorded_file)
            sound.export(output_file, format="mp3", bitrate="320k")

            # %% [markdown]
            # Load Large Model

            # %%



            # %%
            # load audio
            # audio = whisper.load_audio(output_file)
            # audio = whisper.pad_or_trim(audio)
            # # make log-Mel spectrogram and move to the same device as the model
            # mel = whisper.log_mel_spectrogram(audio).to(model.device)

            # # detect the spoken language
            # _, probs = model.detect_language(mel)
            # print(f"Detected language: {max(probs, key=probs.get)}")


            # language = 'english'

            # %% [markdown]
            # Decode Audio (HIDDEN)

            # %%

            # decode the audio
            #options = whisper.DecodingOptions(fp16 = False, temperature=0.1)
            #result = whisper.decode(model, mel, options)

            # print the recognized text
            #text=result.text
            #print(result.text)




            # %% [markdown]
            # Transcribe Whole Audio AND COPY

            # %%
            result=model.transcribe(output_file,fp16=False)
            text_output=result["text"]
            #print(result["text"])
            
            pyperclip.copy(text_output)

            os.remove(output_file)

            # %% [markdown]
            # IMPORT JSON OF VARIABLE SUBSTITUTIONS FOR PHRASES

            # %%

            
            # Opening JSON file
            with open('variables.json') as json_file:
                data = json.load(json_file)

            # %% [markdown]
            # CREATE CASE INSENSITIVE DICT

            # %%
            

            # %% [markdown]
            # CONVERT JSON DICT TO CASE INSENSITIVE

            # %%
            data=CaseInsensitiveDict(data)

            # %% [markdown]
            # Function to Substitute Keywords defined AND copy the substitutions to the clipboard

            # %%


            def substitute_keywords(dictionary,input_string):
                for j in dictionary:
                    position=1
                    while position>0:
                        position=input_string.lower().find(j)
                        if position >0:
                            input_string=input_string[0:position]+data[j]+input_string[position+len(j):]
                        else:
                            continue
                return input_string
                
            substituted_string=substitute_keywords(data,text_output)

            print(substituted_string)
            pyperclip.copy(substituted_string)
            trigger='_'
            print('\n')
        else:
            continue
except KeyboardInterrupt:
    pass

        
        



