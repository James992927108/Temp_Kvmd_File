#!/bin/sh
pacman-key --init
pacman-key --populate
pacman --noconfirm -Sy archlinux-keyring
pacman --noconfirm -Syyu

pacman --noconfirm -Syy
pacman-db-upgrade
pacman --noconfirm -Syu
pacman --needed --noconfirm -S base base-devel colordiff vim tree wget unzip unrar htop nmap iftop iotop strace lsof git jshon rng-tools bc ccache