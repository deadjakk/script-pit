#!/bin/bash

#Changes made:
sudo apt remove cups exim4 -y
#edited the sshd binary to present a different version string upon connection -AWAITING REBOOT 
#enabled tcp syn cookies: 
#vim /etc/sysctl.d/99-sysctl.conf
#disabled ICMP: 
echo "1" > /proc/sys/net/ipv4/icmp_echo_ignore_all
#disabled IPv6: 
echo "net.ipv6.conf.all.disable_ipv6=1; echo "net.ipv6.conf.default.disable_ipv6=1
#disabled mDNS/avahi-daemon: 
service avahi-daemon stop; systemctl disable avahi-daemon #NEEDS TO BE VERIFIED

#MODULE CONFIGURATION:
#disabled freevxfs kernel module: 
echo "install freevxfs /bin/true" > /etc/modprobe.d/freevxfs.conf
#disabled hfs kernel module: 
echo "install hfs /bin/true" > /etc/modprobe.d/hfs.conf
#disabled hfsplus kernel module: 
echo "install hfsplus /bin/true" > /etc/modprobe.d/hfsplus.conf
#disabled udf kernel module: 
echo "install udf /bin/true" > /etc/modprobe.d/udf.conf
#disabled dccp kernel module: 
echo "install dccp /bin/true" > /etc/modprobe.d/dccp.conf
#disabled sctp kernel module: 
echo "install sctp /bin/true" > /etc/modprobe.d/sctp.conf
#disabled rds kernel module: 
echo "install rds /bin/true" > /etc/modprobe.d/rds.conf
#disabled tipc kernel module: 
echo "install tipc /bin/true" > /etc/modprobe.d/tipc.conf

#set log permissions
chmod -R g-wx,o-rwx /var/log/*

#set permissions on crontab
chmod og-rwx /etc/crontab
chown root:root /etc/crontab

#Ensure permissions on /etc/cron.hourly are configured
chown root:root /etc/cron.hourly
chmod og-rwx /etc/cron.hourly

#Ensure permissions on /etc/cron.monthly are configured
chown root:root /etc/cron.monthly
chmod og-rwx /etc/cron.monthly

#Ensure permissions on /etc/cron.d are configured
chown root:root /etc/cron.d 
chmod og-rwx /etc/cron.d

#Ensure at/cron is restricted to authorized users - at.allow
rm /etc/cron.deny 
rm /etc/at.deny 
touch /etc/cron.allow 
touch /etc/at.allow 
chmod og-rwx /etc/cron.allow 
chmod og-rwx /etc/at.allow 
chown root:root /etc/cron.allow 
chown root:root /etc/at.allow

#set permissions on sshd config
chown root:root /etc/ssh/sshd_config 
chmod og-rwx /etc/ssh/sshd_config

#Ensure SSH Protocol is set to 2
sudo echo "Protocol 2" >> /etc/ssh/sshd_config

#Ensure SSH LogLevel is appropriate
cat "LogLevel VERBOSE" >> /etc/ssh/sshd_config

#Ensure SSH MaxAuthTries is set to 4 or less
cat "echo MaxAuthTries 1" >> /etc/ssh/sshd_config

#Ensure SSH IgnoreRHosts #needs evaluation
#echo "IgnoreRhosts yes" >> /etc/ssh/sshd_config

#Ensure SSH HostbasedAuthentication is disabled #needs evaluation #will DEVIATE
#echo "HostbasedAuthentication no" >> /etc/ssh/sshd_config

#Ensure SSH PermitUserEnvironment is disabled #needs evaluation
#echo "PermitUserEnvironment no" >> /etc/ssh/sshd_config

#Ensure SSH Idle Timeout Interval is configured - ClientAliveInterval #needs evaluation
#echo "ClientAliveInterval 300" >> /etc/ssh/sshd_config
#echo "ClientAliveInterval 0" >> /etc/ssh/sshd_config
#echo "ClientAliveCountMax 3" >> /etc/ssh/sshd_config

#Ensure SSH LoginGraceTime is set to one minute or less #needs evaluation
#echo "LoginGraceTime 120" >> /etc/ssh/sshd_config

#Ensure SSH access is limited #needs evaluation
#AllowUsers <userlist>
#AllowGroups <grouplist>
#DenyUsers <userlist>
#DenyGroups <grouplist>

#Ensure SSH warning banner is configured
echo "Banner none" >> /etc/ssh/sshd_config

#Ensure password creation requirements are configured
echo "minlen = 14" >> /etc/security/pwquality.conf
echo "dcredit = -1" >> /etc/security/pwquality.conf
echo "ucredit = -1" >> /etc/security/pwquality.conf
echo "ocredit = -1" >> /etc/security/pwquality.conf
echo "lcredit = -1" >> /etc/security/pwquality.conf


#Ensure permissions on /etc/cron.weekly are configured
chown root:root /etc/cron.weekly
chmod og-rwx /etc/cron.weekly

#set grub permissions:  
chown root:root /boot/grub/grub.cfg
chmod og-rwx /boot/grub/grub.cfg

#set permissions on cron.daily
chown root:root /etc/cron.daily
chmod og-rwx /etc/cron.daily

#changed core dump settings: added "* hard core 0" to /etc/security/limits.conf 
echo "fs.suid_dumpable=0

#enable ASLR
echo "kernel.randomize_va_space=2

#wipe out motd
echo "null" > /etc/motd
echo "null" > /etc/issue
echo "null" > /etc/issue.net

#place this in these in file manually
#"[org/gnome/login-screen] banner-message-enable=true banner-message-text='Authorized uses only. All activity may be monitored and reported.'" >>  /etc/gdm3/greeter.dconf-defaults
sudo apt install ntp chrony tcpdump curl screen vim locate -y

#All of the following sysctl commands have been added to
#/etc/sysctl.d/99-sysctl.conf
#disable forwarding
echo "net.ipv4.route.flush=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.default.send_redirects=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.all.send_redirects=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.all.accept_source_route=0 " >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.default.accept_source_route=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.conf.all.accept_source_route=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.conf.default.accept_source_route=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.route.flush=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.route.flush=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.all.accept_redirects=0 " >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.default.accept_redirects=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.conf.all.accept_redirects=0 " >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.conf.default.accept_redirects=0 " >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.all.secure_redirects=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.default.secure_redirects=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.route.flush=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.default.log_martians=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.all.log_martians=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.icmp_echo_ignore_broadcasts=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.icmp_ignore_bogus_error_responses=1 " >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.all.rp_filter=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.conf.default.rp_filter=1" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv4.tcp_syncookies=1"  >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.conf.all.accept_ra=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.conf.default.accept_ra=0" >> /etc/sysctl.d/99-sysctl.conf
echo "net.ipv6.route.flush=1" >> /etc/sysctl.d/99-sysctl.conf

#Set logging in SSH to VERBOSE
sed s/#LogLevel\ INFO/LogLevel\ VERBOSE/g /etc/ssh/sshd_config -i

#Set SSH configuration
sed s/#MaxAuthTries\ 6/MaxAuthTries\ 1/g /etc/ssh/sshd_config -i

#Ensure system accounts are non-login
for user in `awk -F: '($3 < 1000) {print $1 }' /etc/passwd`; do if [ $user != "root" ]; then usermod -L $user if [ $user != "sync" ] && [ $user != "shutdown" ] && [ $user != "halt" ]; then usermod -s /usr/sbin/nologin $user fi fi done


#set shadow file permissions
chown root:shadow /etc/gshadow-
chown root:root /etc/gshadow- 
chmod o-rwx,g-rw /etc/gshadow-
chown root:shadow /etc/shadow-
chown root:root /etc/shadow- 
chmod o-rwx,g-rw /etc/shadow-

#Ensure access to the su command is restricted - /etc/pam.d/su #do this manually with userlist
#echo "auth required pam_wheel.so" >> /etc/pam.d/su
#create something like this in /etc/groups:
#sudo:x:10:root,debuser

#set root umask to 027
echo "umask 027" >> /root/.bashrc

#Software installed:
apt install -y nmap python-pip
