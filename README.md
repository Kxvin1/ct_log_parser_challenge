Instructions for starting project locally

## Getting started

### 1. Clone this repository (main branch)

```bash
git clone https://github.com/Kxvin1/ct_log_parser_challenge.git
```

### 2. Install dependencies

To install dependencies, run the following command in the root directory
```bash
pip install requests pyyaml ua-parser user-agents
```

### 3. Run the app

To run the app, run the following command in the main directory in the CLI:

```bash
python main.py
```

### 4. How it works

```bash
At the bottom of the `main.py` file, the main function is called with the
parameters "log2.log" already input. It will create an output.csv from
all of the ip addresses in the log2.log file.
```

```bash
If you would like it to run a different log file of your own,
change both of the string parameters at the bottom of the `main.py` file.
It must have an extension of .log, example below:
```

Example:
```py
if __name__ == "__main__":
    export_to_csv(find_user_info(get_ips("name-of-log-file.log"), "name-of-log-file.log"))
```

### 5. Example images of what the csv files look like

##### The .csv file (after running the script)

![CSV File](https://i.imgur.com/T3GtKDj.png)

----

##### The same .csv file (in a table)
![CSV File](https://i.imgur.com/saeuPNz.png)
