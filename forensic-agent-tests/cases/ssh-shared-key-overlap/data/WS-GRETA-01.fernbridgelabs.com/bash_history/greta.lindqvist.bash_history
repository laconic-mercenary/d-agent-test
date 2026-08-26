#1715609885
ssh -l greta.lindqvist APP-SHARED-01.fernbridgelabs.com
#1715610728
timedatectl
#1715610965
ss -s
#1715611196
systemctl --failed --no-pager
#1715611318
docker images
#1715615673
ssh -o ServerAliveInterval=30 greta.lindqvist@APP-SHARED-01
#1715615906
nano /opt/company/webapp/main.py
#1715615959
make -j4 -C /home/greta.lindqvist/projects/data-pipeline
