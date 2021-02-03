### os

pacman --noconfirm -Syy

pacman --needed --noconfirm -S glibc pacman

pacman-db-upgrade

pacman --noconfirm -Syu

pacman --needed --noconfirm -S p11-kit archlinux-keyring ca-certificates ca-certificates-mozilla ca-certificates-utils

pacman --needed --noconfirm -S base base-devel colordiff vim tree wget unzip unrar htop nmap iftop iotop strace lsof git jshon rng-tools bc ccache

pacman --needed --noconfirm -S linux-armv7-headers

pacman --noconfirm -Sc || true

echo 'RNGD_OPTS="-o /dev/random -r /dev/hwrng"' > /etc/conf.d/rngd

systemctl disable haveged

systemctl enable rngd

---> 

# OA 

scp -r stages root@192.168.50.199:~/

<---

cp stages/os/semop-wrapper.c /tmp

gcc -fPIC -shared -o /usr/local/lib/libpreload-semop.so /tmp/semop-wrapper.c

export LD_PRELOAD=/usr/local/lib/libpreload-semop.so

sed -i -e "s/^#MAKEFLAGS=.*/MAKEFLAGS=-j5/g" /etc/makepkg.conf

sed -i -e "s/ \!ccache / ccache /g" /etc/makepkg.conf

export PATH="/usr/lib/ccache/bin/:${PATH}"

echo "DNSSEC=no" >> /etc/systemd/resolved.conf 

systemctl enable systemd-resolved

cp stages/os/gitconfig /etc/skel/.gitconfig

cp stages/os/gitconfig /root/.gitconfig

cp stages/os/gitconfig /home/alarm/.gitconfig

mkdir /tmp/linux-profile

git clone https://github.com/mdevaev/linux-profile.git /tmp/linux-profile --depth=1

cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /etc/skel

cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /root

cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /home/alarm 

chown -R alarm:alarm /home/alarm/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim,.gitconfig} 

rm -rf /tmp/linux-profile

cp stages/os/pistat /usr/local/bin/

<!-- Not use pkg-install -->
<!-- cp stages/os/pkg-install /usr/local/bin/ -->