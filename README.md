# BrickAgent - Connecting Claude to your Mindstorms EV3 Robot

You may use the following technology stack to control your EV3 via agentic AI:

1. [https://www.ev3dev.org](https://www.ev3dev.org/docs/getting-started/) - start your EV3 from SD card flashed with ev3dev Linux
2. Equip your EV3 with a wifi dongle to make it accessible in your WLAN
3. Clone the MCP server here and
4. add it to your claude_desktop_config.json
   
        "mcpServers": {
             "ev3-robot": {
                "command": "<local-path>/ev3-env/bin/python",
                "args": ["<local-path>/ev3_mcp.py"]
        }
   
6. Use e.g. Claude Desktop/Code to control your EV3 robot

First fun thing to do is ask the agent to let your robot "drive" letters on the floor and let you guess which one.
But essentially you can now completely use the agentic planning capabilities of Claude for chaining operation to achieve ends.
Sensors give you a feedback-loop.


