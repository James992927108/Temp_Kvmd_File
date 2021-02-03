1. auto start dhcp

`$ systemctl start dhcpcd@eth0.service`  
`$ systemctl status dhcpcd@eth0.service`  
`$ systemctl enable dhcpcd@eth0.service`

2. step 2

`pacman-key --init`  
`pacman-key --populate`  
`pacman --noconfirm -Sy archlinux-keyring`  
`pacman --noconfirm -Syyu`  

### install vim & git

`pacman --noconfirm -S vim git`

### allow user:root ssh

`echo "PermitRootLogin yes" >> /etc/ssh/sshd_config`

1. edit  

`vim /etc/ssh/sshd_config`  

2. add 

`PermitRootLogin yes`

3. restart ssh server  

`systemctl restart sshd`

4. auto start

`systemctl enable ssh`


-----
### 遇到問題

1. curl: (6) Couldn't resolve host
在 WSL 的 DNS 設定如果預設為公司，部分網站會被擋下，因此需要修改 WSL 的 resolve Server。  
編輯 `sudo vim /etc/resolv.conf`
加入 目前使用的 DNS ，從 AP 的設定，例如目前前我的 ip 為 192.168.50.139，DNS 可能為 192.168.50.1 or 192.168.50.255


pacman-key --keyserver hkps://hkps.pool.sks-keyservers.net -r 912C773ABBD1B584 || pacman-key --keyserver keyserver.ubuntu.com -r 912C773ABBD1B584

pacman-key --lsign-key 912C773ABBD1B584

echo "Server = https://pikvm.org/repos/rpi4-arm" >> /etc/pacman.conf

echo "SigLevel = Required DatabaseOptional" >> /etc/pacman.conf
