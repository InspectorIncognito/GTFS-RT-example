# README

Project to generate GTFS-RT formatted files with Python.

# Configuration

## Python Configuration

The project has been used with Python 3.7, so it is recommended to use that version. Additionally, creating a virtual
environment for running the project is highly advisable.

```shell
# Create a virtual environment; you can use the --python parameter to reference a specific Python version
virtualenv venv --python /usr/bin/python3

# Activate the virtual environment
source venv/bin/activate
```

## Dependency Installation

The dependencies are listed in the `requirements.txt` file and can be installed directly using the
command `pip install -r requirements.txt`.

# Execution

To generate and read a GTFS-RT file with vehicle position data, execute the `python build_proto.py` file.

# Serve GTFS-RT File via URL

To obtain the file via a URL, you need to run a server, which can be achieved using the `server.py` file. You can access
the file through a URL with the format `http://localhost:5000/media/filename`. The server will look for the `filename`
in the `output` folder.