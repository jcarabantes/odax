      ___  ____  _  _ __  __
     / _ \|  _ \| || |\ \/ /
    | | | | | | | || |_\  / 
    | |_| | |_| |__   _/  \ 
     \___/|____/   |_|/_/\_\
                        
    Odoo Dictionary Attack XMLRPC Tool
	Tested on Odoo v8, v9, v10

# Usage:
```
usage: odax.py [-h] [-v] [-q] [-vv] [--log logfile] [--enum-db]
               [--enum-version] [--db DB] [-u USERFILE] [-p PASSFILE] [-c]
               [-t Threads] [--tor TOR]
               host port

optional arguments:
  -h, --help            show this help message and exit
  -v                    Show current version
  -q                    Do not print the banner
  -vv                   Verbose mode (default false). Inaccurate using threads
  --log logfile         Log all output to the path (overwrite). Note: can be
                        used without -vv, verbose output will be included in
                        log

Enumeration:
  --enum-db             Enumerate, if possible, all databases
  --enum-version        Enumerate odoo's version

Options:
  --db DB               Target Odoo database. Example: --db=db1 or --db db1
  -u USERFILE, --users USERFILE
                        Path to USERNAMES wordlist
  -p PASSFILE, --pass PASSFILE
                        Path to PASSWORDS wordlist
  -c                    Continue the attack even after having found a valid
                        user and password
  -t Threads, --threads Threads
                        Number of threads, default 2 - max 64

Proxy:
  --tor TOR             Use tor proxy. Example: --tor=localhost:9050 or --tor
                        localhost:9050

Parameters:
  host                  Odoo server Hostname or IP Address
  port                  Odoo server Port to connect

Examples:
    Enumerate Databases without banner (-q):
    $ ./odax.py -q --enum-db <host_name/ip> <port>

    Enumerate Versions using TOR:
    $ ./odax.py --enum-version --tor localhost:9050 odoo-server-test.com 8069

    Dictionary attack using 10 threads:
    $ ./odax.py --threads=10 --db db1 -u <path> -p <path> odoo-server-test.com 8069

    Dictionary attack with verbose mode and logging:
    $ ./odax.py -vv --db=db1 --log=<path> --users <path> --pass <path> odoo-server-test.com 8069

    Dictionary attack and continue the attack using TOR:
    $ ./odax.py -c --db db1 --tor=localhost:9050 --users <path> --pass <path> odoo-server-test.com 8069
```

# Setup:

  <h3>Debian based systems:</h3>

```
$ sudo apt-get update && sudo apt-get install python-pip -y

$ git clone https://github.com/jcarabantes/odax.git

$ cd odax/

$ sudo apt-get install python-socksipy

$ python -m pip install -r requirements.txt
```

# Contribution:
  <h4>If you have any ideas about improvements in Odax, feel free to contribute.</h4>
  
  * Contact me through ([@javicarabantes](https://twitter.com/javicarabantes))

# Disclaimer:
  I'm not responsible for anything you do with this program, so please only use it for good and educational purposes.

