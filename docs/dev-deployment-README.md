# AWS setup

## Credentials

Make sure you have sufficient AWS permissions for the actions required. If you have trouble, contact Jay.

## AWS RDS

1. Create AWS RDS database (if it is not already created). If it is created, make sure it is running.
1. When creating it, choose the following options:
   - `PostgreSQL - 12.5-R 1` for the Engine Type
   - Template - `Free Tier` - for the dev stuff
   - Master username - `postgres`
   - Auto generate a password - it will show the generated password once the database is created. MAKE SURE TO SAVE IT!
   - Leave the rest of the options as default
1. The RDS should now be in creating mode. The credentials (Password) will be displayed. MAKE SURE TO SAVE IT in a safe place!
1. Also note down the endpoint once available.
1. Update the security group to allow inbound traffic from the SG that the EC2 instance belongs to (next section).

## AWS EC2

1. Create an AWS EC2 instance (ask Jay for more details). Make sure the public IP is selected, or else it won't be accessible from outside. When choosing the instance type, choose "Ubuntu 20.04".
1. Change the security group rules to allow Inbound traffic (Custom TCP) to Port 8888 from `Anywhere`
1. Copy the latest version of the code to the EC2 instance using `scp`
1. Download the latest required dependencies:
   - `sudo apt-get update`
   - `sudo apt-get install python3.9 python3.9-venv libpq-dev python3.9-dev`
1. Update the configuration file to point to the AWS RDS endpoint and also add a password field under `postgres`. So, you will need to update "postgres.hostname" and "postgres.password". Also, update the asset prefix URL by "asset.prefix_url".
1. Download the python reqs:
   - `. ./env/bin/activate`
   - `make install`
1. Run the server using `tmux`:
   - `tmux`
   - `. ./env/bin/activate`
   - `PYTHONPATH=. CONFIG_PATH=./configs/dev-ec2-config.yaml python3.9 app/__main__.py`
