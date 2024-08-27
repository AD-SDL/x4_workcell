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

    gen5xpt_base = "C:\\Users\\Public\Documents\\Plate Reader\\DATA\\Gen5 w WEI\\7-25-2024 32 reagents\\"
    gen5xpt_pr1 = gen5xpt_base + "pr1_B25_read_all384wells.xpt"
    gen5xpt_pr2 = gen5xpt_base + "pr2_B26_read_all384wells.xpt"

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

if __name__ == "__main__":
    main()
