import time
from typing import Any, Dict

from wei.core.interfaces.rest_interface import RestInterface
from wei.types.module_types import Module, ModuleState, ModuleStatus
from wei.types.step_types import Step


platereader_1 = Module(
    name="platereader_1", interface="wei_rest_node", config={"rest_node_address": "http://172.21.64.1:2000"}
)
platereader_2 = Module(
    name="platereader_2", interface="wei_rest_node", config={"rest_node_address": "http://172.21.64.1:2001"}
)

gen5xpt_base = "C:\\Users\\Public\Documents\\Plate Reader\\DATA\\Gen5 w WEI\\7-25-2024 32 reagents\\"
gen5xpt_pr1 = gen5xpt_base + "pr1_B25_read_all384wells.xpt"
gen5xpt_pr2 = gen5xpt_base + "pr2_B26_read_all384wells.xpt"

try:
    for i in range(1000):
        state = ModuleState.model_validate(RestInterface.get_state(module=platereader_1))
        print(state)
        if state.status == ModuleStatus.ERROR:
            raise Exception(f"Module has an error, throwing: {state}")
        if state.status == ModuleStatus.IDLE:
            print(f"Running read {i}")
            step = Step(name="run_action",
                        module="module",
                        action="run_experiment",
                        args={
                            "experiment_file_path": gen5xpt_pr1
                        }
            )
            print(RestInterface.send_action(step, platereader_1, run_dir="."))
        else:
            time.sleep(10)
except Exception:
    import traceback
    traceback.print_exc()
    # Do other error handling here, send emails etc.
