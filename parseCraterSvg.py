import math
import random
import svgwrite
from miditime.miditime import MIDITime
from pycda import CDA, load_image
from lxml import etree
    

# *** DESIRED FILENAMES AND SETTINGS *** #
# image_name = 'crater230621_001.png'
# svg_name = "crater230621_001.svg"
mymidi = MIDITime(120, 'crater230621_002.mid', 5, 4, 2)

svg_to_parse = "july21circles.svg"

logger = print

def load_svg_file(path, resolve_entities=False):
    parser = etree.XMLParser(
        remove_comments=True, recover=True, resolve_entities=resolve_entities
    )
    try:
        doc = etree.parse(path, parser=parser)
        svg_root = doc.getroot()
    except Exception as exc:
        logger.error("Failed to load input file! (%s)", exc)
    else:
        return svg_root


root = load_svg_file(svg_to_parse)
print(root)

detections_array = []
for child in root:
    # print(child)
    # print(child.tag)
    if child.tag == "{http://www.w3.org/2000/svg}g":
        for circle in child:
            props = circle.attrib
            detections_array.append({'x': float(props['cx']), 'y': float(props['cy']), 'r': float(props['r'])})

# print(detections_array)

# detections_array is the main data
# it is an array of crater data in the form:
#     [
#       {'x': 100, y: 100, r: 100},
#       {'x': 120, y: 80, r: 50}
#     ]

# for row in detections_array:
#     print(row)

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

def find_min_values(data):
    min_values = {
        'x':0,
        'y':0,
        'r':0
    }
    for row in data:
        if row['x'] < min_values['x']:
            min_values['x'] = row['x']
        if row['y'] < min_values['y']:
            min_values['y'] = row['y']
        if row['r'] < min_values['r']:
            min_values['r'] = row['r']
    return min_values

# print(find_max_values(detections_array))

max_values = find_max_values(detections_array)
max_x = max_values['x']
max_y = max_values['y']
max_r = max_values['r']

min_values = find_min_values(detections_array)
min_x = min_values['x']

# *** Create SVG processes ***
# dwg = svgwrite.Drawing(svg_name, size=(math.ceil(max_x), math.ceil(max_y)), profile='tiny')

# for row in detections_array:
#     dwg.add(dwg.circle((row['x'], row['y']), row['r']))
# dwg.save()

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
    scale_pct = mymidi.linear_scale_pct(0, max_x, magnitude)
    
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

    print(mymidi.scale_to_note(scale_pct, d_minor))
    note = mymidi.scale_to_note(scale_pct, c_major)

    #Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note)

    return midi_pitch

note_list = []

multiplier = 6

for d in detections_array:
    note_list.append([
        math.ceil((d['x'] - start_time) * multiplier),
        mag_to_pitch_tuned(d['y']),
        math.floor((math.log(d['r']+1) / math.log(max_r+1)) * 100),  # velocity
		1  # duration
    ])
exit()

# Add a track with those notes
mymidi.add_track(note_list)

# Output the .mid file
mymidi.save_midi()
