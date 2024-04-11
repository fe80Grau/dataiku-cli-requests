# Dataiku CLI Requests

A small Python script to call builds for Dataiku datasets via the command line interface. 
* You can generate crons with dataiku-cli-requests command to schedule your builds!!!
* At the moment it only works with NON RECURSIVE FORCED BUILD.


## Requirements

* Python3 [https://www.python.org/]

## Installation

```
pip install dataiku-cli-requests
```

## Getting started

* Command arguments:
- --host: The Dataiku instance URL.
- --user: Your Dataiku username.
- --password: Your Dataiku password. (This can also be set via an environment variable, see below)
- --project: The Dataiku project key.
- --dataset: The dataset to build.

## Using Environment Variables

For security reasons, it's recommended to use an environment variable to pass your Dataiku password instead of passing it directly as a command argument. To do this, you can set an environment variable named `DATAIKU_PASSWORD` before running the script.

Setting the Environment Variable
On Linux/macOS:
```
export DATAIKU_PASSWORD="yourpasswordhere"
```

On Windows (Command Prompt):
```
set DATAIKU_PASSWORD=yourpasswordhere
```

On Windows (PowerShell):
```
$env:DATAIKU_PASSWORD="yourpasswordhere"
```

After setting the environment variable, you can omit the `--password` argument when using the script. If both the environment variable and the `--password` argument are provided, the script will use the value provided as the argument.

## Example
```
dataiku-cli-requests --host https://dataiku.example.com:11000/ --user test --password p4$$w0rd --project PROJECTNAME --dataset mydataset
```
