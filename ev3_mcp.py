#!/usr/bin/env python3
"""
EV3 Mindstorms MCP Server for Mac
Connection: SSH over local network (192.168.178.x) → EV3 Brick running ev3dev
"""
  
import paramiko
from mcp.server.fastmcp import FastMCP

# ─── Configuration ────────────────────────────────────────────────
EV3_HOST = "192.168.178.166"
EV3_USER = "robot"
EV3_PASS = "maker"          # Default ev3dev password

WHEEL_DIAMETER_MM = 33.3    # Wheel diameter in mm (adjust if distance is off)
AXLE_TRACK_MM     = 186     # Axle track in mm (adjust if turn angles are off)
# ──────────────────────────────────────────────────────────────────

mcp = FastMCP("EV3 Mindstorms MCP")


def ssh_run(python_code: str) -> str:
    """Executes Python code on the EV3 via SSH and returns the output."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(EV3_HOST, username=EV3_USER, password=EV3_PASS, timeout=10)
        cmd = f'python3 -c "{python_code.replace(chr(34), chr(39))}"'
        _, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        return out if out else (err if err else "OK")
    except Exception as e:
        return "Error: {}".format(e)
    finally:
        client.close()


def ssh_script(script: str) -> str:
    """Uploads a multi-line Python script to the EV3 and executes it."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(EV3_HOST, username=EV3_USER, password=EV3_PASS, timeout=10)
        sftp = client.open_sftp()
        with sftp.open("/tmp/claude_cmd.py", "w") as f:
            f.write(script)
        sftp.close()
        _, stdout, stderr = client.exec_command("brickrun -r -- pybricks-micropython /tmp/claude_cmd.py")
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        return out if out else (err if err else "OK")
    except Exception as e:
        return "Error: {}".format(e)
    finally:
        client.close()


# ─── MCP Tools ────────────────────────────────────────────────────

@mcp.tool()
def drive_forward(distance_cm: float, speed: int = 300) -> str:
    """
    Drives the EV3 robot forward.

    Args:
        distance_cm: Distance to travel in centimeters
        speed: Motor speed (100–800, default: 300)
    """
    distance_mm = int(distance_cm * 10)
    script = (
        "from pybricks.hubs import EV3Brick\n"
        "from pybricks.ev3devices import Motor\n"
        "from pybricks.parameters import Port, Stop\n"
        "from pybricks.robotics import DriveBase\n"
        "from pybricks.tools import wait\n"
        "\n"
        "motor_left = Motor(Port.B)\n"
        "motor_right = Motor(Port.C)\n"
        "robot = DriveBase(motor_left, motor_right, wheel_diameter={}, axle_track={})\n".format(WHEEL_DIAMETER_MM, AXLE_TRACK_MM) +
        "robot.straight({})\n".format(distance_mm) +
        'print("Drove forward: {} cm")\n'.format(distance_cm)
    )
    return ssh_script(script)


@mcp.tool()
def drive_backward(distance_cm: float, speed: int = 300) -> str:
    """
    Drives the EV3 robot backward.

    Args:
        distance_cm: Distance to travel in centimeters
        speed: Motor speed (100–800, default: 300)
    """
    distance_mm = int(-distance_cm * 10)
    script = (
        "from pybricks.hubs import EV3Brick\n"
        "from pybricks.ev3devices import Motor\n"
        "from pybricks.parameters import Port, Stop\n"
        "from pybricks.robotics import DriveBase\n"
        "from pybricks.tools import wait\n"
        "\n"
        "motor_left = Motor(Port.B)\n"
        "motor_right = Motor(Port.C)\n"
        "robot = DriveBase(motor_left, motor_right, wheel_diameter={}, axle_track={})\n".format(WHEEL_DIAMETER_MM, AXLE_TRACK_MM) +
        "robot.straight({})\n".format(distance_mm) +
        'print("Drove backward: {} cm")\n'.format(distance_cm)
    )
    return ssh_script(script)


@mcp.tool()
def turn(angle_degrees: float) -> str:
    """
    Turns the robot by a given angle.

    Args:
        angle_degrees: Turn angle in degrees. Positive = right, negative = left.
                       Example: 90 = 90° right, -90 = 90° left, 180 = U-turn
    """
    direction = "right" if angle_degrees > 0 else "left"
    script = (
        "from pybricks.ev3devices import Motor\n"
        "from pybricks.parameters import Port\n"
        "from pybricks.robotics import DriveBase\n"
        "\n"
        "motor_left = Motor(Port.B)\n"
        "motor_right = Motor(Port.C)\n"
        "robot = DriveBase(motor_left, motor_right, wheel_diameter={}, axle_track={})\n".format(WHEEL_DIAMETER_MM, AXLE_TRACK_MM) +
        "robot.turn({})\n".format(angle_degrees) +
        'print("Turned: {}° {}")\n'.format(abs(angle_degrees), direction)
    )
    return ssh_script(script)


@mcp.tool()
def stop() -> str:
    """Stops all EV3 motors immediately."""
    script = (
        "from pybricks.ev3devices import Motor\n"
        "from pybricks.parameters import Port\n"
        "\n"
        "for port in [Port.A, Port.B, Port.C, Port.D]:\n"
        "    try:\n"
        "        Motor(port).stop()\n"
        "    except:\n"
        "        pass\n"
        'print("All motors stopped")\n'
    )
    return ssh_script(script)


@mcp.tool()
def beep(frequency: int = 440, duration_ms: int = 500) -> str:
    """
    Plays a tone on the EV3.

    Args:
        frequency: Frequency in Hz (200–2000, default: 440 = concert A)
        duration_ms: Duration in milliseconds (default: 500)
    """
    script = (
        "from pybricks.hubs import EV3Brick\n"
        "ev3 = EV3Brick()\n"
        "ev3.speaker.beep(frequency={}, duration={})\n".format(frequency, duration_ms) +
        'print("Played tone: {} Hz, {} ms")\n'.format(frequency, duration_ms)
    )
    return ssh_script(script)


@mcp.tool()
def speak(text: str) -> str:
    """
    Makes the EV3 read out a text (text-to-speech).

    Args:
        text: The text the robot should speak
    """
    safe_text = text.replace('"', '\\"')
    script = (
        "from pybricks.hubs import EV3Brick\n"
        "ev3 = EV3Brick()\n"
        'ev3.speaker.say("{}")\n'.format(safe_text) +
        'print("Said: {}")\n'.format(text)
    )
    return ssh_script(script)


@mcp.tool()
def measure_ir_distance() -> str:
    """
    Measures proximity to the nearest object using the infrared sensor.
    Sensor must be connected to port S4.

    Returns:
        Proximity value 0–100 (not a real cm value):
        0 = very close, 100 = no obstacle in range (~70 cm)
    """
    script = (
        "from pybricks.ev3devices import InfraredSensor\n"
        "from pybricks.parameters import Port\n"
        "\n"
        "sensor = InfraredSensor(Port.S4)\n"
        "value = sensor.distance()\n"
        'print("IR proximity: " + str(value) + "/100")\n'
    )
    return ssh_script(script)


@mcp.tool()
def read_color() -> str:
    """
    Reads the current color using the color sensor.
    Sensor must be connected to port S3.

    Returns:
        Detected color and brightness value
    """
    script = (
        "from pybricks.ev3devices import ColorSensor\n"
        "from pybricks.parameters import Port\n"
        "\n"
        "sensor = ColorSensor(Port.S3)\n"
        "color = sensor.color()\n"
        "brightness = sensor.reflection()\n"
        'print("Color: " + str(color) + ", Brightness: " + str(brightness) + "%")\n'
    )
    return ssh_script(script)


@mcp.tool()
def control_single_motor(port: str, angle: int, speed: int = 200) -> str:
    """
    Controls a single motor directly.

    Args:
        port: Motor port (A, B, C, or D)
        angle: Rotation angle in degrees (positive = forward, negative = backward)
        speed: Speed in °/sec (default: 200)
    """
    port_map = {"A": "Port.A", "B": "Port.B", "C": "Port.C", "D": "Port.D"}
    ev3_port = port_map.get(port.upper(), "Port.A")
    script = (
        "from pybricks.ev3devices import Motor\n"
        "from pybricks.parameters import Port\n"
        "\n"
        "motor = Motor({})\n".format(ev3_port) +
        "motor.run_angle({}, {})\n".format(speed, angle) +
        'print("Motor {}: rotated {}°")\n'.format(port, angle)
    )
    return ssh_script(script)


@mcp.tool()
def test_connection() -> str:
    """
    Tests the SSH connection to the EV3 and returns system information.
    Uses standard Python 3 (not pybricks), since os.uname() is available there.
    """
    code = (
        "import os; "
        "u = os.uname(); "
        'print("EV3 connected!"); '
        'print("Hostname: " + u.nodename); '
        'print("System: " + u.sysname + " " + u.release)'
    )
    return ssh_run(code)


# ─── Start server ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("EV3 MCP Server starting...")
    print("Connecting to EV3 at {} via SSH...".format(EV3_HOST))
    mcp.run(transport="stdio")