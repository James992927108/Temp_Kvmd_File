### pikvm

---> 

# OA 

scp -r Apk root@192.168.50.199:~/

<---
pacman --noconfirm -Syu && pacman --noconfirm --needed -S netctl parted e2fsprogs

pacman --noconfirm -Sc

<!-- From here for kvmd depance-->
pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/python-spidev-3.5-2-any.pkg.tar.xz 

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/python-pyghmi-1.5.19-1-any.pkg.tar.xz

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/libgpiod-1.6.2-1-armv7h.pkg.tar.xz

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/platformio-5.0.3-1-any.pkg.tar.xz

<!-- 提示已安裝過 -->
<!-- pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/avrdude-svn-20201019.1450-1-armv7h.pkg.tar.xz -->

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/ustreamer-2.2-1-armv7h.pkg.tar.xz

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-dependency/raspberrypi-io-access-0.5-1-any.pkg.tar.xz
<!-- End -->

<!-- Install kvmd  -->
pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-2.10-1-any.pkg.tar.xz

<!-- Install kvmd-platform  -->

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-platform-v2-hdmiusb-generic-2.10-1-any.pkg.tar.xz

<!-- From here for kvmd-webterm depance-->
pacman --noconfirm -Syu && pacman --noconfirm --needed -U  apk/armv7/kvmd-webterm-dependency/ttyd-1.6.1.100-1-armv7h.pkg.tar.xz
<!-- End -->

<!-- Install kvmd-webterm -->
pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/kvmd-webterm-0.35-1-any.pkg.tar.xz


<!-- From here for kvmd-oled depance-->


pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/new_test/python-luma-core-2.2.0-1-any.pkg.tar.xz

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/new_test/python-luma-oled-3.8.1-1-any.pkg.tar.xz

pacman --noconfirm -Syu && pacman --noconfirm --needed -U apk/armv7/new_test/kvmd-oled-0.3-1-any.pkg.tar.xz

systemctl restart kvmd

systemctl restart kvmd-webterm

systemctl restart kvmd-nginx

<!-- systemctl restart kvmd-tc358743 -->

systemctl enable kvmd-nginx

systemctl enable kvmd-webterm

systemctl enable kvmd

<!-- systemctl enable kvmd-tc358743 -->

cp stages/pikvm/motd /etc/