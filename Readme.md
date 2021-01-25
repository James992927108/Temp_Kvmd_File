1. 開啟 root -> ssh 

`vi /etc/ssh/sshd_config`

> PermitRootLogin yes

2. 系統更新

> pacman-key --init  
> pacman-key --populate  
> pacman --noconfirm -Sy archlinux-keyring    
> pacman --noconfirm -Syyu

3. 安裝 vim & git

> pacman --noconfirm -S vim git

4. os stage

> pacman --noconfirm -Syy  
> pacman-db-upgrade  
> pacman --noconfirm -Syu  
> pacman --needed --noconfirm -S base base-devel colordiff vim tree wget unzip unrar htop nmap iftop iotop strace lsof git jshon rng-tools bc ccache

5. install headers

Board   | Arch    | type 
--------|:-------:|-----:
rpi4    | arm     | linux-raspberrypi4 linux-raspberrypi4-headers   
generic | arm     | linux-armv7-headers
generic | aarch64 | linux-aarch64-headers

> pacman --needed --noconfirm -S ${type} 

> pacman --noconfirm -Sc || true  
> echo 'RNGD_OPTS="-o /dev/random -r /dev/hwrng"' > /etc/conf.d/rngd  
> systemctl disable haveged  
> systemctl enable rngd 

5. 從 OA 複製 Stages 資料夾到 TinkerBoard

scp -r stages-rock64-generic-arm root@192.168.50.199:~/  

cp stages-rock64-generic-arm/os/semop-wrapper.c /tmp

gcc -fPIC -shared -o /usr/local/lib/libpreload-semop.so /tmp/semop-wrapper.c

export LD_PRELOAD=/usr/local/lib/libpreload-semop.so

sed -i -e "s/^#MAKEFLAGS=.*/MAKEFLAGS=-j5/g" /etc/makepkg.conf

sed -i -e "s/ \!ccache / ccache /g" /etc/makepkg.conf

export PATH="/usr/lib/ccache/bin/:${PATH}"

echo "DNSSEC=no" >> /etc/systemd/resolved.conf 

systemctl enable systemd-resolved

cp stages-rock64-generic-arm/os/gitconfig /etc/skel/.gitconfig

cp stages-rock64-generic-arm/os/gitconfig /root/.gitconfig

cp stages-rock64-generic-arm/os/gitconfig /home/alarm/.gitconfig

mkdir /tmp/linux-profile

git clone https://github.com/mdevaev/linux-profile.git /tmp/linux-profile --depth=1

cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /etc/skel

cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /root

cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /home/alarm 

chown -R alarm:alarm /home/alarm/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim,.gitconfig} 

rm -rf /tmp/linux-profile

cp stages-rock64-generic-arm/os/pistat /usr/local/bin/

<!-- Not use pkg-install -->
cp stages-rock64-generic-arm/os/pkg-install /usr/local/bin/  

6.  從 OA 複製 Apk 資料夾到 TinkerBoard

scp -r apk-pikvm-generic-armv7 root@192.168.50.199:~/  

7. 安裝全部的pkg

pacman --noconfirm -Syu && pacman --noconfirm --needed -S netctl parted e2fsprogs

pacman --noconfirm -Syu && pacman --noconfirm --needed -U *.tar.xz

pacman --noconfirm -Sc

cp stages-rock64-generic-armv7/pikvm/vcgencmd /tmp/

mkdir -p /opt/vc/bin && cp -a /tmp/vcgencmd /opt/vc/bin/vcgencmd 

systemctl enable kvmd

systemctl enable kvmd-nginx

systemctl enable kvmd-webterm

cp stages-rock64-generic-armv7/pikvm/motd /etc/

echo 7c1be81a-d68f-4342-846e-ff7795663ea6  && kvmd-gencert --do-the-thing


