!/bin/sh

echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
echo "HOOKS=(base udev block filesystems)" >> /etc/mkinitcpio.conf
rm -f /etc/localtime && ln -s "/usr/share/zoneinfo/$TIMEZONE" /etc/localtime
echo "HOOKS=(base udev block filesystems)" >> /etc/mkinitcpio.conf
echo "Server = $REPO_URL/\$arch/\$repo" > /etc/pacman.d/mirrorlist
pacman-key --init && pacman-key --populate archlinuxarm

sed -i -e "s/^CheckSpace/#!!!CheckSpace/g" /etc/pacman.conf

pacman --noconfirm -Syy

pacman-db-upgrade && pacman --noconfirm -Syu

pacman --needed --noconfirm -S base base-devel colordiff vim tree wget unzip unrar htop nmap iftop iotop strace lsof git jshon rng-tools bc ccache

case "$ARCH" in \
        arm) \
            case "$BOARD" in \
                rpi|rpi2|rpi3|zero|zerow) pacman --needed --noconfirm -S linux-raspberrypi linux-raspberrypi-headers;; \
                rpi4) pacman --needed --noconfirm -S linux-raspberrypi4 linux-raspberrypi4-headers;; \
                *) pacman --needed --noconfirm -S linux-armv7-headers;; \
            esac;; \
        aarch64) pacman --needed --noconfirm -S linux-aarch64-headers;; \
        *) echo "Unknown architecture: $ARCH"; exit 1;; \
esac

pacman --noconfirm -Sc || true

echo 'RNGD_OPTS="-o /dev/random -r /dev/hwrng"' > /etc/conf.d/rngd \
	&& systemctl disable haveged \
	&& systemctl enable rngd

git clone --depth=1 $BUILDER_URL $_BUILDER_DIR

cp $_BUILDER_DIR/stages/os/semop-wrapper.c /tmp
gcc -fPIC -shared -o /usr/local/lib/libpreload-semop.so /tmp/semop-wrapper.c
export LD_PRELOAD=/usr/local/lib/libpreload-semop.so

sed -i -e "s/^#MAKEFLAGS=.*/MAKEFLAGS=-j5/g" /etc/makepkg.conf
sed -i -e "s/ !ccache / ccache /g" /etc/makepkg.conf
export PATH="/usr/lib/ccache/bin/:${PATH}"

echo "DNSSEC=no" >> /etc/systemd/resolved.conf \
	&& systemctl enable systemd-resolved

cp $_BUILDER_DIR/stages/os/gitconfig /etc/skel/.gitconfig
cp $_BUILDER_DIR/stages/os/gitconfig /root/.gitconfig
cp $_BUILDER_DIR/stages/os/gitconfig /home/alarm/.gitconfig

mkdir /tmp/linux-profile \
	&& git clone https://github.com/mdevaev/linux-profile.git /tmp/linux-profile --depth=1 \
	&& cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /etc/skel \
	&& cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /root \
	&& cp -a /tmp/linux-profile/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim} /home/alarm \
	&& chown -R alarm:alarm /home/alarm/{.bash_profile,.bashrc,.vimrc,.vimpagerrc,.vim,.gitconfig} \
	&& rm -rf /tmp/linux-profile

cp $_BUILDER_DIR/stages/os/pistat /usr/local/bin/
sudo chmod 777 /usr/local/bin/pistat 

cp $_BUILDER_DIR/stages/os/pkg-install /usr/local/bin/
sudo chmod 777 /usr/local/bin/pkg-install 

