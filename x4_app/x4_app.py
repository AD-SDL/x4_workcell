#!/usr/bin/env python3
"""Runs an example of a WEI workflow"""

import json
from pathlib import Path

from wei import ExperimentClient


def main() -> None:
    """Runs an example WEI workflow"""
    # This defines the Experiment object that will communicate with the WEI server
    exp = ExperimentClient("localhost", "8000", "X4_Experiment")

    # The path to the Workflow definition yaml file
    wf_path = Path(__file__).parent / "workflows" / "x4_run_ot2_protocol.yaml"


    # init_resources={}
    # resources = state_of_resources_now()

    # pscript= generate_eli_python_script()
    # protocol_file = convert_p2yaml()

    # def create_current_protocol(base_procotol, resources):        
    #     ##injest resources into script header
    #     pass

    # current_protocol = create_current_protocol(resources)
    
    # This runs the workflow
    flow_info = exp.start_run(
        wf_path.resolve(),
        payload={
            "protocol_file": current_protocol
        },
    )
    print(json.dumps(flow_info, indent=2))

    # The below line can be used to fetch the result and save it in our local directory
    exp.get_file(
        flow_info["hist"]["Run OT2 Protocol"]["action_msg"],
        "./protocol_run_log.json",
    )


if __name__ == "__main__":
    main()
