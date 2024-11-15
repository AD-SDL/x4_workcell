import time
from typing import Any, Dict

from wei.core.interfaces.rest_interface import RestInterface
from wei.types.module_types import Module, ModuleState, ModuleStatus
from wei.types.step_types import Step
from wei.core.notifications import send_email
from wei.config import Config

from argparse import ArgumentParser


platereader_1 = Module(
    name="platereader_1", interface="wei_rest_node", config={"rest_node_address": "http://172.21.64.1:2000"}
)
platereader_2 = Module(
    name="platereader_2", interface="wei_rest_node", config={"rest_node_address": "http://172.21.64.1:2001"}
)

argparser = ArgumentParser()
argparser.add_argument("--command", "-c", type=str, default="reset")
argparser.add_argument("--platereader", "-p", type=int, default=1)
args = argparser.parse_args()

# Supported commands: reset, shutdown, pause, resume, cancel
command = args.command
supported_commands = ["reset", "shutdown", "cancel"]
if command not in supported_commands:
    raise Exception(f"Command not valid. Supported commmands: {supported_commands}")
platereader_number = args.platereader
if platereader_number == 1:
    platereader = platereader_1
elif platereader_number == 2:
    platereader = platereader_2
else:
    raise Exception("Invalid plate reader number")

RestInterface.send_admin_command(platereader, command)

print(f"Sent command {command}")
