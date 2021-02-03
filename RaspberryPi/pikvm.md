### pikvm

---> 

# OA 

scp -r apk root@192.168.50.199:~/

<---

pacman --noconfirm --needed -S netctl parted e2fsprogs

<!-- From here for kvmd depance-->
pacman --noconfirm --needed -U apk/kvmd-dependency/python-spidev-3.5-2-any.pkg.tar.xz 

pacman --noconfirm --needed -U apk/kvmd-dependency/python-pyghmi-1.5.19-1-any.pkg.tar.xz

pacman --noconfirm --needed -U apk/kvmd-dependency/libgpiod-1.6.2-1-armv7h.pkg.tar.xz

pacman --noconfirm --needed -U apk/kvmd-dependency/platformio-5.0.3-1-any.pkg.tar.xz

pacman --noconfirm --needed -U apk/kvmd-dependency/avrdude-svn-20201019.1450-1-armv7h.pkg.tar.xz

pacman --noconfirm --needed -U apk/kvmd-dependency/ustreamer-2.2-1-armv7h.pkg.tar.xz

pacman --noconfirm --needed -U apk/kvmd-dependency/raspberrypi-io-access-0.5-1-any.pkg.tar.xz
<!-- End -->

<!-- Install kvmd  -->
pacman --noconfirm --needed -U apk/kvmd-2.10-1-any.pkg.tar.xz

<!-- Install kvmd-platform  -->

pacman --noconfirm --needed -U apk/kvmd-platform-v2-hdmiusb-generic-2.10-1-any.pkg.tar.xz

<!-- From here for kvmd-webterm depance-->
pacman --noconfirm --needed -U  apk/kvmd-webterm-dependency/ttyd-1.6.1.100-1-armv7h.pkg.tar.xz
<!-- End -->

<!-- Install kvmd-webterm -->
pacman --noconfirm --needed -U apk/kvmd-webterm-0.35-1-any.pkg.tar.xz

systemctl restart kvmd

systemctl restart kvmd-webterm

systemctl restart kvmd-nginx

<!-- systemctl restart kvmd-tc358743 -->

systemctl enable kvmd-nginx

systemctl enable kvmd-webterm

systemctl enable kvmd

<!-- systemctl enable kvmd-tc358743 -->

cp stages/pikvm/motd /etc/