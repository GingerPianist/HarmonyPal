#!/bin/bash

RawInputMelodyPath=$1
InputMelodyPath="${RawInputMelodyPath}.mp3"

echo Name of your file is: $InputMelodyPath

# 1st step TRANSCRIPT - mp3 to midi
cd ../tones2notes
source myenv3.10/bin/activate
python3 src/transcribe_and_play.py --audio_file $InputMelodyPath
deactivate
OutputMelodyPath="${RawInputMelodyPath}_transcribed.midi"

# 2nd step HARMONIZER - 1-track midi to 4-track midi 

cd ../Harmonizer
javac -cp jMusic1.6.5.jar -d out src/com/company/Harmonizer.java
java -cp .:jMusic1.6.5.jar:out com.company.Harmonizer

# 3rd step INTRO/OUTRO GENERATION (skip)


# 4th step SHEET MUSIC GENERATION
cd ../.midi-to-score
source myenv/bin/activate
python3 Midi_Converter.py
deactivate






