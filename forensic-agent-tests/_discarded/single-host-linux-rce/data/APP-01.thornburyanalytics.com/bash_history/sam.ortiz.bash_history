#1786675066
whoami
#1786675409
ls -lh
#1786675457
date
#1786675805
ps aux --sort=-%mem | head
#1786676084
systemctl list-timers
#1786676093
resolvectl query login.microsoftonline.com
#1786677159
systemctl status gunicorn --no-pager
#1786677459
journalctl -u nginx --since '30 min ago' --no-pager | tail -20
#1786677510
ss -ltnp | grep gunicorn
#1786678269
systemctl show nginx -p ActiveState -p SubState -p MainPID
#1786678505
sysctl -a 2>/dev/null | grep net.ipv4.ip_forward
#1786678941
systemctl list-units --failed
#1786679125
cat /etc/passwd | head
#1786679185
users
#1786679488
date -u
#1786679535
cd -
#1786679608
journalctl -xe --no-pager | tail -20
#1786679700
iostat -x 1 3
#1786679709
ss -ltnp | grep nginx
#1786679780
du -sh /tmp/*
#1786679821
find /etc/systemd/user -maxdepth 2 -type f 2>/dev/null | head
#1786679875
journalctl --no-pager -n 5
#1786679912
loginctl session-status
#1786679972
loginctl list-sessions
