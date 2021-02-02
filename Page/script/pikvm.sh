pkg-install	kvmd-webterm netctl parted e2fsprogs kvmd-platform-$PLATFORM-$BOARD

systemctl enable kvmd \
&& systemctl enable kvmd-nginx \
&& systemctl enable kvmd-webterm 

# in pi-builder there is no pikvm folder, in other project "os"
# cp $_BUILDER_DIR/stages/pikvm/motd /etc/

[ ! -f /boot/cmdline.txt ] || sed -i -f /usr/share/kvmd/configs.default/os/cmdline/$PLATFORM-$BOARD.sed /boot/cmdline.txt \
	&& [ ! -f /usr/share/kvmd/configs.default/os/boot-config/$PLATFORM-$BOARD.txt ] \
		|| cp /usr/share/kvmd/configs.default/os/boot-config/$PLATFORM-$BOARD.txt /boot/config.txt

RUN sed -i -e "s/-session   optional   pam_systemd.so/#-session   optional   pam_systemd.so/g" /etc/pam.d/system-login
echo $NEW_HTTPS_CERT && kvmd-gencert --do-the-thing