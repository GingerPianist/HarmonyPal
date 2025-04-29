import os
import librosa
import argparse
import pandas as pd
import subprocess
import shutil
from pathlib import Path
from tones2notes.src.transcribe_and_play import PianoTranscription


def edit_csv_EMO_Harmonizer(filename, modifiedFilename, melodyKey):
    # Editing the CSVs with the filename
    # 1
    df = pd.read_csv('./EMO_Harmonizer/midi_data/EMOPIA/key_mode_tempo.csv')
    df.at[0, 'name'] = modifiedFilename
    df.at[0, 'keyname'] = melodyKey
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv('./EMO_Harmonizer/midi_data/EMOPIA/key_mode_tempo.csv', index=False)

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
        #"absolute",
        "transpose",
        "transpose_rule",
        "ablated",
        "functional"
    ]

    for representation in representations:
        subprocess.run([
            "python3",
            "representations/midi2events_emopia.py",
            f"--representation={representation}"
        ], check=True)
        # Print current working directory


def built_vocabulary():
    # 2nd - Build Vocabulary for 'functional' representation
    subprocess.run([
        "python3",
        "representations/events2words.py",
        "--representation=functional"
    ], check=True)

def build_data_splits():
    # 3rd - Build Data Splits
    subprocess.run([
        "python3",
        "representations/data_splits.py"
    ], check=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type=str, required=True, help='Path to audio file')
    parser.add_argument('--key', type=str, required=True, help='Key in which the harmonized song is')
    args = parser.parse_args()
    melodyKey = args.key
    audioFile = args.audio_file.split('/')[-1]
    filename = audioFile.split('.')[0]
    midiFile =  filename + '.mid'
    modifiedFilename = 'Q3_' + filename + '_3' # Adding classes for Emopia classification

    # videoFile = audioFile.split('.')[0] + '_transcripted.mp4'
    # vf = os.path.join(Path.cwd(), 'results', videoFile)


    #Tones2notes part - mp3 to midi
    print("Current working dir:", os.getcwd())
    tc = PianoTranscription('CRNN_Conditioning', device='cuda', checkpoint_path='./tones2notes/model_checkpoints/CRNN_Conditioning_regressedLoss.pth')
    audio, _ = librosa.core.load(args.audio_file, sr=16000)
    tc.transcribe(audio, midiFile)
    print("Successfully transcribed and written as: ", midiFile)

    print("Working dir:", os.getcwd())
    # EMO_Harmonizer part - midi with harmony
    edit_csv_EMO_Harmonizer(filename, modifiedFilename, melodyKey)
    print("CSV DONE")

    #Copy the file to EMO_Harmonizer/midi_data
    shutil.copy(filename+ ".mid", "EMO_Harmonizer/midi_data/EMOPIA/midis_chord11/" + modifiedFilename + ".mid")

    # Change working dir for EMO_Harmonizer fix
    print("Changing dir to EMO_Harmonizer, from:", os.getcwd())
    os.chdir('./EMO_Harmonizer')
    print("Working dir:", os.getcwd())

    build_event_representations()
    #built_vocabulary()
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

