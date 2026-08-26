#1786673091
uptime
#1786673239
ss -s
#1786673479
systemctl --failed --no-pager
#1786673870
ls
#1786673919
systemd-analyze blame | head
#1786674786
ssh -A sam.ortiz@APP-01
#1786676922
systemctl is-active sshd
#1786676956
journalctl -u sshd -n 200 --no-pager
#1786677020
ssh -l sam.ortiz APP-01.thornburyanalytics.com
