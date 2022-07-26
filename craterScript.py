import math
import random
import svgwrite
from miditime.miditime import MIDITime
from pycda import CDA, load_image

# *** DESIRED FILENAMES AND SETTINGS *** #
image_name = 'CratersVer305.png'
svg_name = "svgtest305.svg"
mymidi = MIDITime(60, 'ver305.mid', 5, 4, 2)

# ***  PYCDA - import image and convert to data  ***
cda = CDA()
image = load_image(image_name)
detections = cda.predict(image)
detections_dict = detections.to_dict()
detections_array = []

# detections_array is the main data
# it is an array of crater data in the form:
#     [
#       {'x': 100, y: 100, r: 100},
#       {'x': 120, y: 80, r: 50}
#     ]

# Populates detections_array with data from detection_dict
for key,val in detections_dict['lat'].items():
    detections_array.append({'x':detections_dict['long'][key], 'y':detections_dict['lat'][key], 'r':detections_dict['diameter'][key]/2})

for row in detections_array:
    print(row)

# Helper function - Finds maximum values of x y and z for an list of dicts
def find_max_values(data):
    max_values = {
        'x':0,
        'y':0,
        'r':0
    }
    for row in data:
        if row['x'] > max_values['x']:
            max_values['x'] = row['x']
        if row['y'] > max_values['y']:
            max_values['y'] = row['y']
        if row['r'] > max_values['r']:
            max_values['r'] = row['r']
    return max_values

# print(find_max_values(detections_array))

max_values = find_max_values(detections_array)
max_x = max_values['x']
max_y = max_values['y']
max_r = max_values['r']

def find_min_values(data):
    min_values = {
        'x': max_x,
        'y': max_y,
        'r': max_r
    }
    for row in data:
        if row['x'] < min_values['x']:
            min_values['x'] = row['x']
        if row['y'] < min_values['y']:
            min_values['y'] = row['y']
        if row['r'] < min_values['r']:
            min_values['r'] = row['r']
    return min_values

min_values = find_min_values(detections_array)
min_x = min_values['x']
min_y = min_values['y']
min_r = min_values['r']
print(min_x)

prediction = cda.get_prediction(image, verbose=True)
prediction.show()

# *** Create SVG processes ***
dwg = svgwrite.Drawing(svg_name, size=(math.ceil(max_x), math.ceil(max_y)), profile='tiny')

for row in detections_array:
    dwg.add(dwg.circle((row['x'], row['y']), row['r']))
dwg.save()

# Optional helper function which can generate fake data
def generate_fake_data(rows, maxX, maxY, maxR):
    fake_data = []
    for x in range(0, rows):
        fake_data.append({
            'x': random.randint(0,maxX),
            'y': random.randint(0,maxY),
            'r': random.randint(0,maxR)
        })
    return fake_data

# fake_data = generate_fake_data(1000, 2600, 4000, 120)

# ***    MIDITIME processes below here    ***
start_time = min_x

def mag_to_pitch_tuned(magnitude):
    # Where does this data point sit in the domain of your data? (I.E. the min magnitude is 3, the max in 5.6). In this case the optional 'True' means the scale is reversed, so the highest value will return the lowest percentage.
    scale_pct = mymidi.linear_scale_pct(0, max_y, magnitude)

    # Another option: Linear scale, reverse order
    # scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude, True)

    # Another option: Logarithmic scale, reverse order
    # scale_pct = mymidi.log_scale_pct(3, 5.7, magnitude, True)

    # Pick a range of notes. This allows you to play in a key.
    d_minor = ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']
    c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    e_major = ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']
    all = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    #Find the note that matches your data point
    note = mymidi.scale_to_note(scale_pct, c_major)

    #Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note)

    return midi_pitch

note_list = []

multiplier = 0.2

for d in detections_array:
    note_list.append([
        math.ceil((d['x'] - start_time) * multiplier),
        mag_to_pitch_tuned(d['y']),
        math.floor((d['r'] / max_r) * 100),  # velocity
		1  # duration
    ])

# Add a track with those notes
mymidi.add_track(note_list)

# Output the .mid file
mymidi.save_midi()
