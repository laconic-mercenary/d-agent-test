#1718110840
journalctl -u systemd-resolved --since today --no-pager | tail -20
#1718111294
tail -20 /var/log/syslog
#1718111298
systemctl status sshd --no-pager
#1718111310
journalctl -u nginx --since '30 min ago' --no-pager | tail -50
#1718111458
ss -ltnp | grep nginx
#1718111520
systemctl show sshd -p ActiveState -p SubState -p MainPID
#1718111562
who
#1718111573
grep -i warning /var/log/syslog | tail
#1718111682
cat /proc/meminfo | head -5
#1718111722
journalctl -xe --no-pager | tail -20
#1718111729
who -a
#1718111736
tail -200 /var/log/auth.log
#1718112115
grep -i 'failed password' /var/log/auth.log | tail -20
#1718112510
nmcli device show | grep -E 'GENERAL.DEVICE|IP4.ADDRESS|IP4.GATEWAY'
#1718112564
journalctl --since '10 min ago' --no-pager -n 20
#1718112652
resolvectl status 2>/dev/null | head -30
#1718112694
cqt
#1718112706
ulimit -n
#1718113738
cd /tmp
#1718114268
udevadm info --query=property --name=/dev/null | head
#1718114307
tail -100 /var/log/auth.log
#1718114399
cat /etc/fstab
#1718116818
du -sh /var/log/*
#1718116944
last -20
#1718117036
df -h /var
#1718117247
systemctl status nginx
#1718117257
systemctl list-timers --all --no-pager | head
#1718117558
cat /etc/crontab
#1718117626
ls -ltr /var/log | tail
#1718117660
ls -ltr /var/log/ | tail -10
#1718117701
nmcli device status 2>/dev/null
#1718117855
grep -i failed /var/log/auth.log | tail
#1718124738
hostnamectl
#1718124756
command -v python3
#1718124826
crontab -l
#1718125112
journalctl -u sshd --since '30 min ago' --no-pager | tail -20
#1718125148
systemd-analyze blame | head
#1718125176
tail -20 ~/.bash_history
