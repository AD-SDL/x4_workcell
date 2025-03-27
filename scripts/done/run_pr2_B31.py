import time
from typing import Any, Dict

from wei.core.interfaces.rest_interface import RestInterface
from wei.types.module_types import Module, ModuleState, ModuleStatus
from wei.types.step_types import Step, StepStatus
from wei.core.notifications import send_email
from wei.config import Config
from datetime import datetime, timedelta


platereader_1 = Module(
    name="platereader_1", interface="wei_rest_node", config={"rest_node_address": "http://172.21.64.1:2000"}
)
platereader_2 = Module(
    name="platereader_2", interface="wei_rest_node", config={"rest_node_address": "http://172.21.64.1:2001"}
)

#########################
# CONFIGURE SCRIPT HERE #
#########################
gen5xpt_base = "C:\\Users\\Public\\Documents\\Plate Reader\\DATA\\Gen5 w WEI\\12-12-2024 32 solvents multi\\"

platereader = platereader_2
experiment_path = gen5xpt_base + "pr2_B31_multi_read_all96wells.xpt"

Config.smtp_server="mailgateway.anl.gov"
Config.smtp_port=25

print(f"Running experiment {experiment_path} on plate reader {platereader.name}")
start_time = datetime.now()

i = 0
result = ()
previous_run_failed = False
while True:
    i += 1
    try:
        try:
            state = ModuleState.model_validate(RestInterface.get_state(module=platereader))
            print(state)
            if state.status == ModuleStatus.ERROR:
                raise Exception(f"Module has an error, throwing: {state}")
            if state.status == ModuleStatus.IDLE:
                print(f"Running read {i}")
                step = Step(name="run_action",
                            module="module",
                            action="run_experiment",
                            args={
                                "experiment_file_path": experiment_path
                            }
                )
                result = RestInterface.send_action(step, platereader, run_dir=".")
                print(result)
                if result[0] == StepStatus.FAILED:
                    raise Exception(f"Run {i} failed on reader {platereader.name}")
                previous_run_failed = False
            else:
                # Module is paused or otherwise occupied, wait until it's available
                time.sleep(10)
        except KeyboardInterrupt:
            try:
                RestInterface.send_admin_command(platereader, "cancel")
            except:
                pass
            finally:
                break
        except Exception as e:
            if previous_run_failed:
                raise Exception(f"Multiple consecutive failed runs on {platereader.name}, need help!") from e
            previous_run_failed = True
            import traceback
            traceback.print_exc()
            # Do other error handling here, send emails etc.
            email_body = f"""
Result: {result}
Timestamp: {datetime.now()}
Time Elapsed: {datetime.now() - start_time}
traceback: {traceback.format_exc()}
            """
            for email in ["ryan.lewis@anl.gov"]:
                send_email(f"Error on {platereader.name}", email, email_body)

            # Reset the module and keep trying
            state = ModuleState.model_validate(RestInterface.get_state(module=platereader))
            if state.status == ModuleStatus.ERROR:
                RestInterface.send_admin_command(platereader, "reset")
            time.sleep(10)
    except Exception:
        traceback.print_exc()
        email_body = f"""
Result: {result}
Timestamp: {datetime.now()}
Time Elapsed: {datetime.now() - start_time}
traceback: {traceback.format_exc()}
            """
        for email in ["ryan.lewis@anl.gov", "Shkrob@anl.gov"]:
            send_email(f"CATASTROPHIC ALERT: Error during error handling on {platereader.name}", email, email_body)
        break
