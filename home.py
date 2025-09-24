from flask import Flask, render_template, jsonify, render_template_string
import phue  # Stelle sicher, dass du die Philips Hue Bridge Library installiert hast

app = Flask(__name__)

# Keep this simple function, to be able to have one link shortcurts to turn the lights off.

@app.route('/off')
def turn_offf():
    # Turn off the lights when the button is pressed
    turn_off_lights()
    return render_template_string("""
       <html lang="en">
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <body style="font-family: 'Roboto', sans-serif;">
            All lights turned off!<br><br><a href="/">Go back</a>
            </body>
        </html>
    """)
      
@app.route('/on')
def turn_onnn():
    # Turn off the lights when the button is pressed
    turn_on_lights()
    return render_template_string("""
       <html lang="en">
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <body style="font-family: 'Roboto', sans-serif;">
            All lights turned on!<br><br><a href="/">Go back</a>
        </body>
        </html>
    """)

# Function to turn off the lights
def turn_off_lights():
	bridge.set_group(1, 'on', False)
	bridge.set_group(2, 'on', False)
	bridge.set_group(3, 'on', False)
        
# Function to turn on the lights
def turn_on_lights():
	bridge.set_group(1, 'on', True)
	bridge.set_group(2, 'on', True)
	bridge.set_group(3, 'on', True)

# Gruppenkonfiguration
GROUPS = {
    'all': {'id': None, 'name': 'Alle'},
    'erdgeschoss': {'id': 2, 'name': 'Erdgeschoss'},
    'flur': {'id': 3, 'name': 'Flur'},
    'wohnzimmer': {'id': 1, 'name': 'Wohnzimmer'}
}

# Steuerbare Steckdosen
PLUGS = {
    'bett': {'id': 13, 'name': 'Drucker'},
    'wlan_repeater': {'id': 15, 'name': 'WLAN Repeater'}
}

# Initialisiere Hue Bridge
bridge = phue.Bridge('192.168.178.33')

@app.route('/')
def index():
    # Hole aktuellen Status für Gruppen
    group_status = {}
    for group_key, group_info in GROUPS.items():
        if group_info['id'] is not None:
            try:
                group_status[group_key] = bridge.get_group(group_info['id'], 'on')
            except Exception as e:
                print(f"Fehler beim Abrufen des Status für {group_key}: {e}")
                group_status[group_key] = False
        else:
            group_status[group_key] = False

    # Hole Status für steuerbare Steckdosen
    plug_status = {}
    for plug_key, plug_info in PLUGS.items():
        try:
            plug_status[plug_key] = bridge.get_light(plug_info['id'], 'on')
        except Exception as e:
            print(f"Fehler beim Abrufen des Status für {plug_key}: {e}")
            plug_status[plug_key] = False

    return render_template('room_control.html', 
                           groups=GROUPS, 
                           plugs=PLUGS,
                           group_status=group_status,
                           plug_status=plug_status)

@app.route('/toggle/<group>')
def toggle_group(group):
    try:
        if group == 'all':
            # Toggele Gruppen 1, 2 und 3
            all_off = all(not bridge.get_group(g['id'], 'on') for g in GROUPS.values() if g['id'] is not None and g['id'] in [1, 2, 3])
            
            for group_id in [1, 2, 3]:
                bridge.set_group(group_id, 'on', all_off)
        elif group in GROUPS:
            # Toggele spezifische Gruppe
            group_config = GROUPS[group]
            current_state = bridge.get_group(group_config['id'], 'on')
            bridge.set_group(group_config['id'], 'on', not current_state)
        elif group in PLUGS:
            # Toggele steuerbare Steckdose
            plug_config = PLUGS[group]
            current_state = bridge.get_light(plug_config['id'], 'on')
            bridge.set_light(plug_config['id'], 'on', not current_state)
        else:
            return jsonify({'error': 'Ungültige Gruppe oder Steckdose'}), 400
        
        return jsonify({'success': True})
    
    except Exception as e:
        print(f"Fehler beim Toggeln der Gruppe/Steckdose {group}: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
