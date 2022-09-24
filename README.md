----
## Access Docker Repo Here: https://hub.docker.com/r/kevinzy/logger_dockerize
----

## Instructions for starting project locally

### 1. Clone this repository (main branch)

```bash
git clone https://github.com/Kxvin1/log_parser.git
```

### 2. Install dependencies

To install dependencies, run the following command in the root directory
```bash
pip install requests pyyaml ua-parser user-agents pytest
```

### 3. Run the app

To run the app, run the following command in the main directory in the CLI:

```bash
python main.py
```

### 4. Check file validity - How to run tests

- First, add your file to the "log_files" directory and change the 'log_file' (in main.py) variable to the name of your file

- Then if you would like to test if your log file is accepted, run the following command in the root directory

```bash
pytest
```

### 5. How it works

```bash
At the bottom of the `main.py` file, the main function is called with the
parameters "log2.log" as the default log file. It will create an output.csv from
all of the ip addresses from that file.
```

```bash
If you would like it to run a different log file of your own,
change the variable 'log_file' near the bottom of the `main.py` file.

Example below:

# change this:
### EDIT LOG FILE HERE
log_file = "./log_files/log2.log"


# to something like this (after adding your file to "./log_files" directory of the project):
### EDIT LOG FILE HERE
log_file = "./log_files/your-log-file.log"
```

### 6. Example images of what the csv files look like

##### The .csv file (after running the script)

![CSV File](https://i.imgur.com/T3GtKDj.png)

----

##### The same .csv file (in a table)
![CSV File](https://i.imgur.com/saeuPNz.png)

----

### Planned Changes/Additions

- Refactor the read_file function to use regex - makes it so the file content order don't matter. 
  - This will also make adding/removing different columns to the csv easier in a situation where the format of the log file is completely different than expected
- Create classes for some of the functions in main.py
