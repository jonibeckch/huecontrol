from flask import Flask, render_template_string, render_template
from phue import Bridge

# Configuration
HUE_BRIDGE_IP = '192.168.178.33'  # Replace with your Hue Bridge IP
API_KEY = 'k2YozSQaTc-aRGYNNTP9ifFHgX22zHK54uKAmg4f'  # Replace with the API key obtained from the Hue bridge


# Initialize the Flask app and Hue bridge connection
app = Flask(__name__)
bridge = Bridge(HUE_BRIDGE_IP)
bridge.connect()

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


@app.route('/')
def index():
    # Definieren Sie Ihre Buttons als Liste von Dictionaries
    buttons = [
        {"route": "/on", "label": "Alle an"},
        {"route": "/off", "label": "Alle aus"},
        {"route": "/egon", "label": "Erdgeschoss an"},
        {"route": "/egoff", "label": "Erdgeschoss aus"},
        {"route": "/fluron", "label": "Flur an"},
        {"route": "/fluroff", "label": "Flur aus"},
        {"route": "/wohnon", "label": "Wohnzimmer an"},
        {"route": "/wohnoff", "label": "Wohnzimmer aus"},

        # Hier können Sie weitere Buttons einfach hinzufügen
        # {"route": "/neue_route", "label": "Neuer Button"}
    ]
    return render_template('template.html', buttons=buttons)

#EG ein / aus
@app.route('/egon')
def eg_on():
    bridge.set_group(2, 'on', True)
    return render_template_string("""
        <!DOCTYPE html>
        <body>
            <h1>Erdgeschoss an</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)

@app.route('/egoff')
def eg_off():
    bridge.set_group(2, 'on', False)
    return render_template_string("""
        <!DOCTYPE html>
        <body>
            <h1>Erdgeschoss aus</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)


#Flur ein / aus
@app.route('/fluron')
def flur_on():
    bridge.set_group(3, 'on', True)
    return render_template_string("""
        <!DOCTYPE html>
        <body>
            <h1>Flur an</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)

@app.route('/fluroff')
def flur_off():
    bridge.set_group(3, 'on', False)
    return render_template_string("""
        <!DOCTYPE html>
        <body>
            <h1>Flur aus</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)

#Flur ein / aus
@app.route('/wohnon')
def wohn_on():
    bridge.set_group(1, 'on', True)
    return render_template_string("""
        <!DOCTYPE html>
        <body>
            <h1>Wohnzimmer an</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)

@app.route('/wohnoff')
def wohn_off():
    bridge.set_group(1, 'on', False)
    return render_template_string("""
        <!DOCTYPE html>
        <body>
            <h1>Wohnzimmer aus</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)


@app.route('/off')
def turn_offf():
    # Turn off the lights when the button is pressed
    turn_off_lights()
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="10; url=http://192.168.178.156:5000/" />
            <title>Lights Turned Off</title>
        </head>
        <body>
            <h1>All lights have been turned off!</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)
      
@app.route('/on')
def turn_onnn():
    # Turn off the lights when the button is pressed
    turn_on_lights()
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="10; url=http://192.168.178.156:5000/" />
            <title>Lights Turned On</title>
        </head>
        <body>
            <h1>All lights have been turned on!</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Open to all network interfaces on port 5000
