#!/usr/bin/env python3
"""Runs an example of a WEI workflow"""

import json, os, sys
from pathlib import Path
import subprocess

from wei import ExperimentClient


def main() -> None:
    """Runs an example WEI workflow"""
    # This defines the Experiment object that will communicate with the WEI server
    exp = ExperimentClient("localhost", "8000", "X4_Experiment")

    # The path to the Workflow definition yaml file
    wf_path = Path(__file__).parent / "workflows" / "x4_test_epoch2.yaml"


    # init_resources={}
    # resources = state_of_resources_now()

    # pscript= generate_eli_python_script()
    # protocol_file = convert_p2yaml()

    # def create_current_protocol(base_procotol, resources):        
    #     ##injest resources into script header
    #     pass

    # current_protocol = create_current_protocol(resources)

    gen5xpt = "C:\\Users\\Public\\Documents\\Plate Reader\\DATA\\Gen5 w WEI\\"
    gen5xpt += "6-20-2024 16 reagents\\B21_plate_read_all384wells.xpt"

    # This runs the workflow
    for i in range(1000):
        flow_info = exp.start_run(
            wf_path.resolve(),
            payload={"experiment_file_path" : gen5xpt},
        )
        print(json.dumps(flow_info, indent=2))

    # The below line can be used to fetch the result and save it in our local directory
    # exp.get_file(
    #     flow_info["hist"]["Run OT2 Protocol"]["action_msg"],
    #     "./protocol_run_log.json",
    # )


if __name__ == "__main__":
    main()
