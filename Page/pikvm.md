### pikvm.md

---> 

# OA 

scp -r Apk/apk-pikvm-generic-armv7/ root@192.168.50.199:~/

<---

pacman --noconfirm -Syu && pacman --noconfirm --needed -S netctl parted e2fsprogs

pacman --noconfirm -Syu && pacman --noconfirm --needed -S kvmd-platform-v2-hdmiusb-generic

pacman --noconfirm -Syu && pacman --noconfirm --needed -S kvmd-webterm

pacman --noconfirm -Syu && pacman --noconfirm --needed -S kvmd-oled

pacman --noconfirm -Syu && pacman --noconfirm --needed -S pastebinit tmate 

systemctl enable kvmd

systemctl enable kvmd-nginx

systemctl enable kvmd-webterm

<!-- systemctl enable kvmd-tc358743 -->

cp stages-pikvm-rpi4-armv7/pikvm/motd /etc/

<!-- There is no v2-hdmiusb-generic.sed, so select v2-hdmiusb-rpi4.sed-->
sed -i -f /usr/share/kvmd/configs.default/os/cmdline/v2-hdmiusb-rpi4.sed /boot/cmdline.txt

cp /usr/share/kvmd/configs.default/os/boot-config/v2-hdmiusb-rpi4.txt /boot/config.txt

sed -i -e "s/-session   optional   pam_systemd.so/#-session   optional   pam_systemd.so/g" /etc/pam.d/system-login

<!-- use uuidgen get NEW_HTTPS_CERT-->
<!-- if get results is 7c1be81a-d68f-4342-846e-ff7795663ea6 -->
echo 7c1be81a-d68f-4342-846e-ff7795663ea6  && kvmd-gencert --do-the-thing