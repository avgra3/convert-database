# Convert Database Tool

## How Does this Work?

This app uses multiple processes to run a set of alter scripts on all ARIA tables, making sure to skip views. You will receive logs in your terminal where the application starts and when an error occurs.

This application is **only** available here on Github.

## Setup

### Prerequisites

This application relies on the [MariaDB C Connector](https://mariadb.com/docs/connectors/mariadb-connector-c/install-mariadb-connector-c).

If you encounter any issues installing the app, please confirm your installation of the MariaDB Connector C package.

Optionally, you will neeed to have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed if you do not want to download this repository to insall the application.

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install "git+https://github.com/avgra3/convert-database.git@main"
```
or

```bash
git clone https://github.com/avgra3/convert-database.git
cd ./convert-database.git
python -m venv .venv
source .venv/bin/activate
python -m pip install .
```

### UV

Documentation on setting up [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv tool install "git+https://github.com/avgra3/convert-database.git@main"
```

Upgrading

```bash
uv tool upgrade "git+https://github.com/avgra3/convert-database.git@main"
```

### Pipx

How to [setup](https://pipx.pypa.io/stable/installation/).

```bash
pipx install convert-database-tool
```
## Running

```bash
# This prints out the help information for further commands that are needed
convert-database-tool --help
```

**Note:** This app assumes you are trying to update from your computer (localhost). To confirm your configuration is correct, run the following two commands and update those files as neccessary:

```bash
# Returns path to database configuration. Ensure username, password, hostname, and port are all correct.
convert-database-tool --dbConfig

# Returns path to the query that generates the needed alterations.
convert-database-tool --query
```

Run the following, making sure to use substitute `DB_NAME` with the database you want to update:

```bash
convert-database-tool --db DB_NAME
```

**Note:** This could take a while so **do not** restart MariaDB until it finishes. You will notice logging information while the application is running. You can also monitor the updates using your preferred MariaDB server monitoring software to see what is actually being run.

### Other Considerations

Before running, make sure the database configurations are correct. They are located in the [dbConfig.toml]("./src/convert_database_tool/configs/dbConfig.toml") file. If you have already installed the app, run `convert-database-tool --dbConfig` to get the path to the configuration file.

#### Database Configuration

The below is the default configuration. If you get errors connecting to a database the below may need to be changed.

```toml
[database_config]
database = "" # Update this field if you always want to default to a specific database (not reccomended).
local_infile = false
user = "USERNAME"
password = "PASSWORD"
host = "localhost" # If connecting to a different server than the one running the script on, you will need to change this.
port = 3306 # This is the default port and unlikely to change.
```

#### Errors

Errors may show in the terminal while the tool is running. Most errors will come from MariaDB and can include the following:

- Altering a field with VARCHAR set to the max size with message like "Row size too large. The maximum row size for the used ..."
    - As long as the app does not exit, you other tables will continue to be altered
- Incorrect username or password with message like "Access denied for user 'user'@'localhost'"
    - You will need to confirm the database configuration file is correct. Specifically you will need to verify the username, password, and hostname are correct.
    - The likely issue will be the password.
    - If the app is installed (see below), you can run the command `convert-database-tool --dbConfig` to get the config file location.

## Development Branch

If you would like to use the latest _(and likely unstable)_ version use the "dev" branch. Please note, this version has no gurantees to actually work.

