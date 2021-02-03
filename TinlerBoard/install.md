1. look status  
`systemctl status udisks2`
2. 
`systemctl restart udisks2`

### show mount status

`df -a`  
`fdisk  -l`
`lsblk`

### dismount usb

example: usb mount on /dev/sdb  
/dev/sdb1  
/dev/sdb2  

`sudo umount /dev/sdb*`

### format flash or SD card

### disable auto mount

2. stop service  
`systemctl stop udisks2`

bzip2 -d *.bz2

sudo dd if=TinkerOS_DEBIAN.img of=/dev/mmcblkX bs=8192 conv=fsync status=progress

sudo mkdir root
sudo mount /dev/sdb2 root
sudo bsdtar -xpf ArchLinuxARM-armv7-latest.tar.gz -C root
sudo umount root