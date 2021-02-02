### Stage: os
1. setup LOCALE
> echo "en_US.UTF-8 UTF-8" > /etc/locale.gen  
> echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen  
> echo "HOOKS=(base udev block filesystems)" >> /etc/mkinitcpio.conf  

<!-- export LC_ALL "en_US.UTF-8" -->

> rm -f /etc/localtime && ln -s "/usr/share/zoneinfo/$TIMEZONE" /etc/localtime

> echo "HOOKS=(base udev block filesystems)" >> /etc/mkinitcpio.conf

2. setup mirrorlist
> echo "Server = http://de3.mirror.archlinuxarm.org/\$arch/\$repo" > /etc/pacman.d/mirrorlist  
> pacman-key --init  
> pacman-key --populate archlinuxarm

> sed -i -e "s/^CheckSpace/#!!!CheckSpace/g" /etc/pacman.conf

3. install basic pkg
pacman --noconfirm -Syy

<!-- there is nothing to do -->
<!-- pacman --needed --noconfirm -S glibc pacman -->

> pacman-db-upgrade && pacman --noconfirm -Syu

<!-- there is nothing to do -->
<!-- pacman --needed --noconfirm -S p11-kit archlinux-keyring ca-certificates ca-certificates-mozilla ca-certificates-utils -->

> pacman --needed --noconfirm -S base base-devel colordiff vim tree wget unzip unrar htop nmap iftop iotop strace lsof git jshon rng-tools bc ccache

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

---> 

### OA 

scp -r Stages/stages-pikvm-rpi4-armv7/ root@192.168.50.199:~/  

rsync -a --info=progress2 Stages/stages-pikvm-rpi4-armv7/ root@192.168.50.199:~/

<---

> cp stages-pikvm-rpi4-armv7/os/semop-wrapper.c /tmp  
> gcc -fPIC -shared -o /usr/local/lib/libpreload-semop.so /tmp/semop-wrapper.c  
> export LD_PRELOAD=/usr/local/lib/libpreload-semop.so  

> sed -i -e "s/^#MAKEFLAGS=.*/MAKEFLAGS=-j5/g" /etc/makepkg.conf  
> sed -i -e "s/ \!ccache / ccache /g" /etc/makepkg.conf  
> export PATH="/usr/lib/ccache/bin/:${PATH}"  

echo "DNSSEC=no" >> /etc/systemd/resolved.conf  
systemctl enable systemd-resolved  

> cp stages-pikvm-rpi4-armv7/os/gitconfig /etc/skel/.gitconfig  
> cp stages-pikvm-rpi4-armv7/os/gitconfig /root/.gitconfig  
> cp stages-pikvm-rpi4-armv7/os/gitconfig /home/alarm/.gitconfig  

> mkdir /tmp/linux-profile  
> git clone https://github.com/mdevaev/linux-profile.git /tmp/linux-profile --depth=1  
> cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /etc/skel  
> cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /root  
> cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /home/alarm   
> chown -R alarm:alarm /home/alarm/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim,.gitconfig}  
> rm -rf /tmp/linux-profile  

> cp stages-pikvm-rpi4-armv7/os/pistat /usr/local/bin/  

<!-- Not use pkg-install --> 
> cp stages-pikvm-rpi4-armv7/os/pkg-install /usr/local/bin/  

6. go to pikvm-repo.md page