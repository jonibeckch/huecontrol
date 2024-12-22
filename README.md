# simplehue
A simple Project to control your hue lights with a raspberrypi, by opening pages on your local network

# Running on Raspian Version 12
```
cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
```

Step 1:
pip install flask phue


### I used the following guidance created by chatgpt:

Certainly! Below is an example of Python code for a simple web server running on a Raspberry Pi that can turn off your Hue lights when you open a webpage. This solution uses Flask for the web server and the `phue` library to interact with your Philips Hue lights.

### Prerequisites

1. **Install Flask**: This web framework will create the webpage.
2. **Install phue**: This library will help control the Hue lights via the Hue API.

You can install these dependencies with:

```bash
pip install flask phue
```

### Steps:

1. **Connect to Hue Bridge**: Make sure your Raspberry Pi is connected to the same network as your Philips Hue bridge.
2. **Get the API key**: To communicate with your Hue lights, you'll need the API key for your Hue bridge. You can obtain it by following these steps:

    1. Press the button on the top of your Hue Bridge.
    2. Send a POST request to the bridge to generate the key. You can do this using `curl` or a Python script. Example command:

    ```bash
    curl -X POST -d '{"devicetype":"my_hue_app"}' http://<bridge_ip>/api
    ```

    This will return a JSON response with an API key.

### Python Code for Flask Server and Hue Control

```python
from flask import Flask, render_template_string
from phue import Bridge

# Configuration
HUE_BRIDGE_IP = '192.168.1.100'  # Replace with your Hue Bridge IP
API_KEY = 'your_api_key_here'  # Replace with the API key obtained from the Hue bridge

# Initialize the Flask app and Hue bridge connection
app = Flask(__name__)
bridge = Bridge(HUE_BRIDGE_IP)
bridge.connect()

# Function to turn off the lights
def turn_off_lights():
    lights = bridge.lights
    for light in lights:
        light.off()

@app.route('/')
def index():
    # Serve the HTML page
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Turn off Hue Lights</title>
        </head>
        <body>
            <h1>Welcome to the Hue Lights Controller</h1>
            <p>Click the button below to turn off all your Hue lights.</p>
            <form method="post" action="/turn_off">
                <button type="submit">Turn Off Lights</button>
            </form>
        </body>
        </html>
    """)

@app.route('/turn_off', methods=['POST'])
def turn_off():
    # Turn off the lights when the button is pressed
    turn_off_lights()
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lights Turned Off</title>
        </head>
        <body>
            <h1>All lights have been turned off!</h1>
            <a href="/">Go back</a>
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Open to all network interfaces on port 5000
```

### How it Works:

- **Flask Server**: Runs a basic web server on your Raspberry Pi. When you visit the server in a browser, it shows a button to turn off all Hue lights.
- **Button Action**: When the button is clicked, a POST request is sent to the server, which triggers the `turn_off_lights()` function, turning off all lights connected to your Hue Bridge.
- **HTML Page**: A simple web page with a button that sends a POST request to turn off the lights.

### Running the Code:

1. **Start the Flask Server**:
   Run the Python script on your Raspberry Pi:

   ```bash
   python3 your_script_name.py
   ```

2. **Access the Webpage**:
   Open a web browser and go to the Raspberry Pi's IP address:

   ```
   http://<raspberry_pi_ip>:5000
   ```

   For example: `http://192.168.1.50:5000`

3. **Turn Off the Lights**:
   When you click the "Turn Off Lights" button, the lights will be turned off.

### Additional Notes:
- If you only want to control specific lights, you can modify the `turn_off_lights()` function to target particular lights (e.g., by their index or name).
- The `Flask` server is running on port 5000 by default. You can change this in the `app.run()` call if needed.
  
This solution provides a basic way to control your Hue lights with a webpage. You can expand it further to include more controls (e.g., turning lights on/off, changing brightness, etc.).
