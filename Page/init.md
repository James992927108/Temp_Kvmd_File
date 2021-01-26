
### In Tinker
1. Enable root ssh 

    `echo "PermitRootLogin yes" >> /etc/ssh/sshd_config`

2. Initialize the pacman keyring and populate the Arch Linux ARM package signing keys  

    `pacman-key --init`  
    `pacman-key --populate`  
    `pacman --noconfirm -Sy archlinux-keyring`  
    `pacman --noconfirm -Syyu` 
    
3. (Not Ready) sudo ./init.sh

4. go to os.md