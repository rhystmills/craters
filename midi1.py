from miditime.miditime import MIDITime
mymidi = MIDITime(120, 'myfile.mid', 5, 5, 1)

my_data = [
    {'event_date': <datetime object>, 'magnitude': 3.4},
    {'event_date': <datetime object>, 'magnitude': 3.2},
    {'event_date': <datetime object>, 'magnitude': 3.6},
    {'event_date': <datetime object>, 'magnitude': 3.0},
    {'event_date': <datetime object>, 'magnitude': 5.6},
    {'event_date': <datetime object>, 'magnitude': 4.0}
]
my_data_epoched = [{'days_since_epoch': mymidi.days_since_epoch(d['event_date']), 'magnitude': d['magnitude']} for d in my_data]

my_data_timed = [{'beat': mymidi.beat(d['days_since_epoch']), 'magnitude': d['magnitude']} for d in my_data_epoched]

start_time = my_data_timed[0]['beat']

def mag_to_pitch_tuned(magnitude):
    # Where does this data point sit in the domain of your data? (I.E. the min magnitude is 3, the max in 5.6). In this case the optional 'True' means the scale is reversed, so the highest value will return the lowest percentage.
    scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude)

    # Another option: Linear scale, reverse order
    # scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude, True)

    # Another option: Logarithmic scale, reverse order
    # scale_pct = mymidi.log_scale_pct(3, 5.7, magnitude, True)

    # Pick a range of notes. This allows you to play in a key.
    c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    #Find the note that matches your data point
    note = mymidi.scale_to_note(scale_pct, c_major)

    #Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note)

    return midi_pitch

note_list = []

for d in my_data_timed:
    note_list.append([
        d['beat'] - start_time,
        mag_to_pitch_tuned(d['magnitude']),
        100,  # velocity
        1  # duration, in beats
    ])

# Add a track with those notes
mymidi.add_track(note_list)

# Output the .mid file
mymidi.save_midi()