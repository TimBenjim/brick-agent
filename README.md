# BrickAgent - Connecting Claude to your Mindstorms EV3 Robot

Use the following technology stack to control your EV3 via Claude:

1. [https://www.ev3dev.org](https://www.ev3dev.org/docs/getting-started/) - start your EV3 from SD card flashed with ev3dev Linux
2. Equip your EV3 with a wifi dongle to make it accessible in your WLAN
3. Clone the MCP server in this repo and
4. add it to your claude_desktop_config.json
   
        "mcpServers": {
             "ev3-robot": {
                "command": "<local-path>/ev3-env/bin/python",
                "args": ["<local-path>/ev3_mcp.py"]
        }
   
6. Use e.g. Claude Desktop to control your EV3 robot.
   Need to restart Claude, check in the chat input via clicking plus, _ev3-robot_ should show up under Connectors.

First fun thing to do is to ask the agent to let your robot "drive" letters on the floor and let you guess which one.
But essentially you can now completely use the agentic planning capabilities of Claude for chaining operation to achieve ends.
Sensors give you a feedback-loop.


