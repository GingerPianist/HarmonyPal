import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split


def split_emopia(output_dir):
    # make dir
    os.makedirs(output_dir, exist_ok=True)

    # data split by running provided file: scripts/prepare_split.ipynb
    train = pd.read_csv("midi_data/EMOPIA/split/train_clip.csv", index_col=0)
    valid = pd.read_csv("midi_data/EMOPIA/split/val_clip.csv", index_col=0)
    test = pd.read_csv("midi_data/EMOPIA/split/test_clip.csv", index_col=0)

    # --- training dataset (train + valid) --- #
    train_set = []
    for i in range(len(train)):
        train_set.append(train.iloc[i].clip_name[:-4] + '.pkl')
    for i in range(len(valid)):
        train_set.append(valid.iloc[i].clip_name[:-4] + '.pkl')
    pickle.dump(train_set, open(os.path.join(output_dir, 'train.pkl'), 'wb'))

    # --- valid dataset (test) --- #
    valid_set = []
    for i in range(len(test)):
        valid_set.append(test.iloc[i].clip_name[:-4] + '.pkl')
    pickle.dump(valid_set, open(os.path.join(output_dir, 'valid.pkl'), 'wb'))

    print('Emopia: ', len(train_set) + len(valid_set))
    print('train, valid:', len(train_set), len(valid_set))


def split_hooktheory(output_dir):
    os.makedirs(output_dir, exist_ok=True)

    data_home = 'hooktheory_events/lead_sheet_chord11_functional/events'
    pkl_files = os.listdir(data_home)
    train_set, valid_set = train_test_split(pkl_files, test_size=0.1, random_state=42)

    pickle.dump(train_set, open(os.path.join(output_dir, 'train.pkl'), 'wb'))
    pickle.dump(valid_set, open(os.path.join(output_dir, 'valid.pkl'), 'wb'))

    print('HookTheory: ', len(train_set) + len(valid_set))
    print('train, valid:', len(train_set), len(valid_set))


if __name__ == '__main__':
    split_emopia('emopia_events/data_splits')
    #split_hooktheory('hooktheory_events/data_splits')
