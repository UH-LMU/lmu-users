Prerequisites
- install Vagrant

# create VM
vagrant up

# log in with ssh, allow X windows
vagrant ssh -- -X

# start sqlitebrowser
sqlitebrowser &

# run script that reads CellProfiler database
cd /vagrant/scripts
python endocytosis.py


