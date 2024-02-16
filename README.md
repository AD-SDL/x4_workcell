# X4 Workcell

This is the Workcell for the AD-SDL X4 exemplar experiment.

## Dependencies

- You'll need [docker installed](https://docs.docker.com/engine/install/)
    - Make sure to follow the [post installation steps](https://docs.docker.com/engine/install/linux-postinstall/) on Linux to enable non-root user access

## Configuration

As much as possible, this workcell is designed to be configured declaratively. This is done with:

- A `.env` file, created by copying the `example.env` to `.env` and setting the appropriate values for each variable
- The `compose.yaml` docker compose file, which defines a "stack" of containers that control your workcell
    - Note: whenever you see `${SOME_VARIABLE_NAME}` in the compose file, this value is being taken from the `.env`
- The Workcell Config in `workcell_defs/x4_workcell.yaml`, which allows you to define WEI specific configuration for your workcell

## Building, Running, and Managing your Workcell and Experiment Application

Here are some common commands you can use to manage this workcell:

- `docker compose up` to start the workcell (add `-d` to send it to the background after starting)
- `docker compose down` to stop it
