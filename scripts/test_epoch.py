import requests
import os

experiment_path = "C:\\Users\\Public\\Documents\\Plate Reader\\tests\\Gen5 tests\\for Ryan 5-2-2024\\basic_read\\basic_read_384wells.xpt"
hostname = "172.21.64.1"
port = 2000

print(f"Running {experiment_path}")
response = requests.post(f"http://{hostname}:{port}/action", params={
    "action_handle": "run_experiment",
    "action_vars": str({
        "experiment_file_path": experiment_path
    })
})

print(response.json())
