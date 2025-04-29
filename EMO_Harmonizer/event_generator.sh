#1st - BUILD EVENT REPRESENTATION for the audio file:
# REMI representation
python3 representations/midi2events_emopia.py --representation=absolute

# REMI representation (transpose to C major / c minor based on original keymode)
python3 representations/midi2events_emopia.py --representation=transpose

# REMI representation (transpose to C major / c minor based on emotion)
python3 representations/midi2events_emopia.py --representation=transpose_rule

# functional representation (ablated)
python3 representations/midi2events_emopia.py --representation=ablated

# functional representation
python3 representations/midi2events_emopia.py --representation=functional

#2nd - BUILD VOCABULARY
# functional representation (others are similar to EMOPIA)
python3 representations/events2words.py --representation=functional

#3rd - BUILD DATA SPLITS
python3 representations/data_splits.py
