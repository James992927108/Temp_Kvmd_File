pacman-key --keyserver hkps://hkps.pool.sks-keyservers.net -r $PIKVM_REPO_KEY \
		|| pacman-key --keyserver keyserver.ubuntu.com -r $PIKVM_REPO_KEY 

pacman-key --lsign-key $PIKVM_REPO_KEY && echo -e "\n[pikvm]" >> /etc/pacman.conf 


case "$ARCH" in \
        arm) \
            case "$BOARD" in \
                zero|zerow) echo "Server = https://pikvm.org/repos/zerow" >> /etc/pacman.conf;; \
                rpi|rpi2|rpi3|rpi4) echo "Server = https://pikvm.org/repos/$BOARD-$ARCH" >> /etc/pacman.conf;; \
            esac;; \
        aarch64) \
            case "$BOARD" in \
                    generic|rpi4) echo "Server = https://raw.githubusercontent.com/Yura80/pikvm-repo/main/$BOARD-$ARCH" >> /etc/pacman.conf;; \
                    *) echo "Not support"; exit ;; \
            esac;; \
        *) echo "Unknown architecture: $ARCH"; exit 1;; \
esac

echo "SigLevel = Required DatabaseOptional" >> /etc/pacman.conf