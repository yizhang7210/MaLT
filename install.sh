# Install software dependencies (primarily sklearn and pylint)
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-numpy
sudo apt-get install python3-scipy
sudo apt-get install python3-matplotlib
sudo apt-get install python3-dev
sudo apt-get install python3-tk

sudo pip3 install -U scikit-learn
sudo pip3 install -U pylint


# Add useful folders and files
# logs
cd $MALT
mkdir logs

# data store directories
mkdir malt/data/store
mkdir malt/strategies/euler/store

# daily strategy serialization directory
mkdir malt/exec/daily_strategy

# setup templates
cp docs/cron_setup.template cron_setup
cp docs/account.info.template account.info


