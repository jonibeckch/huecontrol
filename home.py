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
    # Serve the HTML page
   return render_template('template.html')

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
