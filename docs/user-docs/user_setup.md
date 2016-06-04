# User Setup Guide

### Basic system requirements
MaLT is developed in Ubuntu and should be able to run on any machine with `python3`,
`cron` and an internect connection.

### Clone this repository
First thing first, clone this repository to a location say `<malt>`.

### Create account with OANDA
At the moment, MaLT works only with OANDA's trading API, so to use/develop/test MaLT,
you need to set up an account with OANDA. You can start by opening a free practice
account and trade with virtual money. Simply sign up on www.oanda.com.

Once you have an account, sign in from www.oanda.com, go to the 'Manage API Access'
section, generate and record an API access token for your user account.

### Installation and setup
- Make a new environment variable named `MALT` to be the path of `<malt>`.
- Add `MALT` to your `PYTHONPATH` environment variable.
- Run `<malt>/install.sh` file: `sh <malt>/install.sh`.
- Go to `<malt>/account.info` and `<malt>/cron_setup` files and fill in your actual
OANDA account and `<malt>` path details.
- Run: `python3 <malt>/malt/exec/daily_train.py` to serialize the initial models
(not on a Friday or Saturday).

### Test and deploy MaLT
To test everything works, go under `<malt>` directory and run `nosetests -v malt`
between Sunday 17:00 and Friday 17:00 America/New York time. This should run all the
tests in the project. Activities should be logged under the `<malt>/logs` directory.

To deploy MaLT, simply run `crontab <malt>/cron_setup` and MaLT should be on.
Make sure your machine is on and online around the time the cron jobs are scheduled
to run, which by default is around 17:00 America/New York time everyday.
You should adjust the time according to your timezone.

To check the cron jobs that MaLT relies on, simply do `crontab -l`.

### Related information
- For details about MaLT's trading strategies,
see [Strategy Guide](strategies.md).
- For more information about MaLT as a software application,
see documentation under `docs/dev-docs`.


