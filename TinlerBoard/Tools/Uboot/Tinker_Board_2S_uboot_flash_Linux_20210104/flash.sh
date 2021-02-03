# !/bin/bash
sudo ./upgrade_tool ef MiniLoaderAll.bin
sudo ./upgrade_tool ul MiniLoaderAll.bin
sudo ./upgrade_tool di -p parameter.txt
sudo ./upgrade_tool di -u uboot.img
sudo ./upgrade_tool di -t trust.img
sudo ./upgrade_tool rd
