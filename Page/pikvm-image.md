### pikvm-image

rm -f /etc/ssh/ssh_host_* /etc/kvmd/nginx/ssl/*

cp stages-pikvm-rpi4-armv7/pikvm-image/_pikvm-firstboot.sh /usr/local/bin/_pikvm-firstboot.sh

cp stages-pikvm-rpi4-armv7/pikvm-image/pikvm-firstboot.service /etc/systemd/system/pikvm-firstboot.service

systemctl enable pikvm-firstboot
