### pikvm-repo.md

pacman-key --keyserver hkps://hkps.pool.sks-keyservers.net -r 912C773ABBD1B584 || pacman-key --keyserver keyserver.ubuntu.com -r 912C773ABBD1B584

pacman-key --lsign-key 912C773ABBD1B584

echo -e "\n[pikvm]" >> /etc/pacman.conf

<!-- PIKVM_REPO_URL ?= https://pikvm.org/repos -->
<!-- $BOARD-$ARCH -->
echo "Server = https://pikvm.org/repos/rpi4-arm" >> /etc/pacman.conf

echo "SigLevel = Required DatabaseOptional" >> /etc/pacman.conf

# go to pikvm.md