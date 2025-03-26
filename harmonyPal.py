import os
import librosa
import argparse
from pathlib import Path
from tones2notes.src.transcribe import PianoTranscription

parser = argparse.ArgumentParser()
parser.add_argument('--audio_file', type=str, required=True, help='Path to audio file')
args = parser.parse_args()
audioFile = args.audio_file.split('/')[-1]
midiFile =  audioFile.split('.')[0] + '_transcipted.mid'
# videoFile = audioFile.split('.')[0] + '_transcripted.mp4'
# vf = os.path.join(Path.cwd(), 'results', videoFile)


#Tones2notes part
tc = PianoTranscription('CRNN_Conditioning', device='cuda', checkpoint_path='./tones2notes/model_checkpoints/CRNN_Conditioning_regressedLoss.pth')
audio, _ = librosa.core.load(args.audio_file, sr=16000)
tc.transcribe(audio, midiFile)


#Convert Midi to Xml


#Autoharmonizer part
# Load data from 'inputs'
data_corpus = convert_files(midiFile, fromDataset=False)

# Build harmonic rhythm and chord model
model = build_model(SEGMENT_LENGTH, RNN_SIZE, NUM_LAYERS, DROPOUT, WEIGHTS_PATH, training=False)

# Process each melody sequence
for idx in trange(len(data_corpus)):
    melody_data = data_corpus[idx][0]
    beat_data = data_corpus[idx][1]
    key_data = data_corpus[idx][2]
    score = data_corpus[idx][3]
    filename = data_corpus[idx][4]

    # Generate harmonic rhythm and chord data
    chord_data = generate_chord(model, melody_data, beat_data, key_data)

    # Export music file
    export_music(score, beat_data, chord_data, filename)

