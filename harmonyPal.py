import os
import librosa
import argparse
import pandas as pd
import subprocess
from pathlib import Path
from tones2notes.src.transcribe import PianoTranscription


def edit_csv_EMO_Harmonizer(audioFile):
    filename = audioFile[:-4]
    modifiedFilename = 'Q1_' + filename + '_1'
    # Editing the CSVs with the filename
    # 1
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/key_mode_tempo.csv')
    df.at[0, 'name'] = modifiedFilename
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/key_mode_tempo.csv', index=False)
    # ADD scale name too!
    # 2
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/test_clip.csv')
    df.at[0, 'clip_name'] = modifiedFilename + '.mid'
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/test_clip.csv', index=False)
    # 3
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/test_SL.csv')
    df.at[0, 'songID'] = filename
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/test_SL.csv', index=False)
    # 4
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/train_clip.csv')
    df.at[0, 'clip_name'] = modifiedFilename + '.mid'
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/train_clip.csv', index=False)
    # 5
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/train_SL.csv')
    df.at[0, 'songID'] = filename
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/train_SL.csv', index=False)
    # 6
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/val_clip.csv')
    df.at[0, 'clip_name'] = modifiedFilename + '.mid'
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/val_clip.csv', index=False)
    # 7
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/val_SL.csv')
    df.at[0, 'songID'] = filename
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/split/val_SL.csv', index=False)

def build_event_representations():
    representations = [
        "absolute",
        "transpose",
        "transpose_rule",
        "ablated",
        "functional"
    ]

    for representation in representations:
        subprocess.run([
            "python3",
            "EMO_Harmonizer/representations/midi2events_emopia.py",
            f"--representation={representation}"
        ], check=True)

def built_vocabulary():
    # 2nd - Build Vocabulary for 'functional' representation
    subprocess.run([
        "python3",
        "EMO_Harmonizer/representations/events2words.py",
        "--representation=functional"
    ], check=True)

def build_data_splits():
    # 3rd - Build Data Splits
    subprocess.run([
        "python3",
        "EMO_Harmonizer/representations/data_splits.py"
    ], check=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type=str, required=True, help='Path to audio file')
    args = parser.parse_args()
    audioFile = args.audio_file.split('/')[-1]
    filename = audioFile.split('.')[0]
    midiFile =  filename + '.mid'
    # videoFile = audioFile.split('.')[0] + '_transcripted.mp4'
    # vf = os.path.join(Path.cwd(), 'results', videoFile)


    # Tones2notes part - mp3 to midi
    tc = PianoTranscription('CRNN_Conditioning', device='cuda', checkpoint_path='./tones2notes/model_checkpoints/CRNN_Conditioning_regressedLoss.pth')
    audio, _ = librosa.core.load(args.audio_file, sr=16000)
    tc.transcribe(audio, midiFile)

    # EMO_Harmonizer part - midi with harmony
    edit_csv_EMO_Harmonizer(audioFile)
    build_event_representations()
    built_vocabulary()
    build_data_splits()

    # Run inference.py and harmonize the requested file
    command = [
        "python3", "inference.py",
        "--configuration=config/emopia_finetune.yaml",
        "--representation=functional",
        "--key_determine=rule",
        "--inference_params=emo_harmonizer_ckpt_functional/best_params.pt",
        "--output_dir=generation/emopia_functional_rule"
    ]
    subprocess.run(command, check=True)


    # Old harmonizing library
    # #Autoharmonizer part
    # # Load data from 'inputs'
    # data_corpus = convert_files(midiFile, fromDataset=False)
    #
    # # Build harmonic rhythm and chord model
    # model = build_model(SEGMENT_LENGTH, RNN_SIZE, NUM_LAYERS, DROPOUT, WEIGHTS_PATH, training=False)
    #
    # # Process each melody sequence
    # for idx in trange(len(data_corpus)):
    #     melody_data = data_corpus[idx][0]
    #     beat_data = data_corpus[idx][1]
    #     key_data = data_corpus[idx][2]
    #     score = data_corpus[idx][3]
    #     filename = data_corpus[idx][4]
    #
    #     # Generate harmonic rhythm and chord data
    #     chord_data = generate_chord(model, melody_data, beat_data, key_data)
    #
    #     # Export music file
    #     export_music(score, beat_data, chord_data, filename)

