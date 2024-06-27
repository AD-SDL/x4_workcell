#!/usr/bin/env python3
"""Runs an example of a WEI workflow"""

import json, os, sys
from pathlib import Path
import subprocess

from wei import ExperimentClient


def main() -> None:
    """Runs an example WEI workflow"""
    # This defines the Experiment object that will communicate with the WEI server
    exp = ExperimentClient("localhost", "8000", "X4_Experiment", email_addresses=["ryan.lewis@anl.gov", "Shkrob@anl.gov"])

    # The path to the Workflow definition yaml file
    wf_pr1 = Path(__file__).parent / "workflows" / "x4_test_platereader1.yaml"
    wf_pr2 = Path(__file__).parent / "workflows" / "x4_test_platereader2.yaml"

    # init_resources={}
    # resources = state_of_resources_now()

    # pscript= generate_eli_python_script()
    # protocol_file = convert_p2yaml()

    # def create_current_protocol(base_procotol, resources):        
    #     ##injest resources into script header
    #     pass

    # current_protocol = create_current_protocol(resources)

    gen5xpt_base = "C:\\Users\\Public\\Documents\\Plate Reader\\DATA\\Gen5 w WEI\\"
    gen5xpt_pr1 = gen5xpt_base + "6-20-2024 16 reagents\\pr1_B21_plate_read_all384wells.xpt"
    gen5xpt_pr2 = gen5xpt_base + "6-20-2024 16 reagents\\pr2_dummy_plate_read_all384wells.xpt"

    # This runs the workflow
    for i in range(1000):
        flow_info_1 = exp.start_run(
            wf_pr1.resolve(),
            payload={"experiment_file_path" : gen5xpt_pr1},
            blocking=False
        )
        flow_info_2 = exp.start_run(
            wf_pr2.resolve(),
            payload={"experiment_file_path" : gen5xpt_pr2},
            blocking=True
        )
        print(json.dumps(flow_info_2, indent=2))

    # The below line can be used to fetch the result and save it in our local directory
    # exp.get_file(
    #     flow_info["hist"]["Run OT2 Protocol"]["action_msg"],
    #     "./protocol_run_log.json",
    # )


if __name__ == "__main__":
    main()
