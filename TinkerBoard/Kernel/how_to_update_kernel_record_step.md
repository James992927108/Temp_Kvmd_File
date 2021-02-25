### 安裝 archlinuxarm 到 tinkerboards 的 emmc 中

1. 使用燒入軟體 balenaEtcher-1.5.116-x64 將 image
檔案 （Tinker_Board-Debian-Stretch-V2.1.16-20200813.img）
燒入到 tinkerboards 中。

2. 完成後，重新連接 tinkerboards 與 pc 的 usb，會有兩個分區,
第一個分區taye 為 fat，存放 boot 資料:第二個為 ext4，存放 rootfs（一般就是linux發行版本）。在 window 上應該只能看到第一個分區（boot）,linux 則可看到兩個分區。

<!-- 3. 移除連接中的 tinkerboards 裝置, 一般是掛載在 /dev/sdX，X-> 取決於有幾個外接usb除存裝置，如果 tinkerboard 為第二個，則為 sdb, 第一個分區為 sdb1，以此類推數字與分區關係。

    `sudo umount /dev/sdb*` -->

4. 在桌面建立 armv7 資料夾並下載 archlinuxarm image 檔案[Download](https://archlinuxarm.org/about/downloads), 因為tinkerboards 使用 rk3288 Soc 為 armv7 架構，所以選擇 ArchLinuxARM-armv7-latest.tar.gz。在arch資料夾底下建立 boot 和 rootfs 兩個資料夾。

    ```
    armv7|-boot
        |-rootfs
        |-ArchLinuxARM-armv7-latest.tar.gz
    ```

5. 查看 tinkerboards 掛載的路徑
    > df -a 或者 sudo fdisk -l

<!-- 5. 假設因為目前 /dev/sdb2 上面是官方 debain 中的檔案，刪除資料夾中所有檔案。

    `yes | sudo mkfs.ext4 /dev/sdb4` -->

6. 假設掛載路徑為 /dev/sdb，分區 1 為 sdb1，分區 2 為 sdb2，並掛載到對應 boot 和 rootfs 資料夾。
    > sudo mount /dev/sdb1 ~/Desktop/armv7/boot  
    sudo mount /dev/sdb2 ~/Desktop/armv7/rootfs

7. 因為要安裝 archlinuxarm，所以先刪除 rootfs 資料夾中所有檔案，不需要重新格式化，保留分區原本的 UUID
    > cd ~/Desktop/armv7/rootfs  
    sudo rm -rf *  
 
8. 解壓縮 ArchLinuxARM-armv7-latest.tar.gz 到 rootfs
    > sudo tar -zxf ArchLinuxARM-armv7-latest.tar.gz -C ~/Desktop/armv7/rootfs

9. 解壓縮完，一定要先 sync 完成後在卸載 boot 和 rootfs  
    > sudo sync
    需要一段時間，可以透過以下指令看目前進度，當 writeback 為 0 即為完成。
    > watch -d grep -e Dirty: -e Writeback: /proc/meminfo

10. (直接參考 Update kernel) 移除連結 pc 的 usb, 並改使用 vcc usb 以及 hdmi 連接 tinkerboards，等待 5～20 秒, 應該是可以正常啟動。

    update: tinkeros 中的 linux kernel 為 4.4.x，但 archlinuxarm 以使用上 5.11.x ,可能會出現錯誤，參考更新 kernel 章節。
    
### Update kernel

reference: [Update TinkerBoard Kernel](https://gist.github.com/TinkerTeam/6286550ce70d34f6b3d483cd803da786#gistcomment-3563189)

1. Clone from kernel.org to Desktop
    > git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git

2. change directory
    > cd ~/Desktop/linux  
    git branch --list --remotes  
    git branch --show-current  
    git checkout linux-5.11.y

3. Copy kernel config  
    - Tinkerboard:    
        > sudo cp Kernel/miniarm-rk3288_tinkerboard_defconfig ~/Desktop/linux/armv7/arm/configs/miniarm-rk3288_tinkerboard_defconfig

    - armbain(default use this):   
        > sudo cp Kernel/miniarm-rk3288_armbain_defconfig ~/Desktop/linux/armv7/arm/configs/miniarm-rk3288_armbain_defconfig

4. Configure the kernel
    > sudo make ARCH=miniarm-rk3288_armbain_defconfig -j16

5. Compile kernel and its modules
    - kernel:
        > sudo make zImage ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j16
    - module:
        > sudo make modules ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j16

6. Compile tinkerboards device tree binary file(.dtb)   
Tinker's dts is in mainline kernel, under the name rk3288-tinker-s.dts.(see: arm/boot/dts/rk3288-tinker-s.dts)
    > sudo make ARCH=arm rk3288-tinker-s.dtb CROSS_COMPILE=arm-linux-gnueabihf- -j16

7. Copy new kernel, rk3288-tinker-s.dtb to boot(partion 1)
    - kernel:
        > cd ~/Desktop/linux/armv7/arm/boot/  
        cp zImage ~/Desktop/armv7/boot
    - device tree binary:
        >cd ~/Desktop/linux/armv7/arm/boot/dts/   
        cp rk3288-tinker-s.dtb ~/Desktop/armv7/boot

8. (option) remove the original device tree binary file
    > cd ~Desktop/armv7/boot  
    sudo rm rk3288-miniarm.dtb

9. Install modules to rootfs(partion 2)
(if kernel is 5.11.0, file will install in /lib/modules/5.11.0)
    > sudo make ARCH=arm INSTALL_MOD_PATH=~/Desktop/armv7/rootfs modules_install

10. Copy initramfs-linux.img to boot(partion 1)
    > cd ~/Desktop/armv7/rootfs/boot  
   sudo cp initramfs-linux.img ~/Desktop/armv7/boot

11. Get rootfs UUID
    > 1. go to *Show Application*
    > 2. search *Disks*
    > 3. select *TinkerBoard UMS* and *Filesystem Partition 2*
    > 4. look UUID
    > <img src="img/disks.png" alt="drawing"/>

9. Modity extlinux.conf
    ```
    label kernel-5.11.0
        kernel /zImage
        fdt /rk3288-tinker-s.dtb
        initrd /initramfs-linux.img
        append console=ttyS3,115200n8 earlyprintk quiet splash plymouth.ignore-serial-consoles root=UUID=68781559-87cf-43d3-8a94-fd4294d6ef72 console=tty1 rw init=/sbin/init
    ```
10. connect power and check
    > <img src="img/uname_pacman_version.png" alt="drawing"/>

### How to check if the modules have loaded in linux kernel ?
> lsmod  
- if there is nothing, try to use 
    > depmod -a
### How to use uart to debug?
if use uart3, need to modifty extlinux
- append *console=ttyS3,115200n8*  
    from  
    'append earlyprintk quiet splash plymouth.ignore-serial-consoles root=UUID=68781559-87cf-43d3-8a94-fd4294d6ef72 console=tty1 rw init=/sbin/init'  
    to  
    'append console=ttyS3,115200n8 earlyprintk quiet splash plymouth.ignore-serial-consoles root=UUID=68781559-87cf-43d3-8a94-fd4294d6ef72 console=tty1 rw init=/sbin/init'
- use *USB convert UART TTL* to connect tinkerboard and pc by follow: 
    > <img src="img/gpio-pinout.png" alt="drawing"/>

- pc(host) open terminal use:
> sudo minicom -D /dev/ttyUSB0 -b 115200 

### 如何使用 onboard emmc？
參考官網 setup 頁面：
https://tinkerboarding.co.uk/wiki/index.php/Setup
如果 tinkerboard 接到 pc 無反應，直接參考這個小節：
https://tinkerboarding.co.uk/wiki/index.php/Setup#UMS_from_SD_card1

### tinkerboard /S 兩著差異在於 S 版本有內建 emmc，一般版本沒有內建 emmc。

解說 sd card ＆ emmc 關係
沿用原生 uboot 
