#!/usr/bin/python

from subprocess import *
import time

print "\033[1;32m---------W3lC0M3 T0 INST4RCH---------------\033[0m"

# Create a single partition and mark it bootable
create_partition = call("cfdisk /dev/sda", shell=True)

# Build ext4 filesystem on it
build_filesystem = call("mkfs.ext4 /dev/sda1", shell=True)

# Mount the new partition
mount = call("mount /dev/sda1 /mnt", shell=True)

# install the base system
base_sys = call("pacstrap /mnt base base-devel", shell=True)

# generate fstab
gen_fstab = call("genfstab -U /mnt > /mnt/etc/fstab", shell=True)

# chroot in to the new system
chroot = call("arch-chroot /mnt", shell=True)

# install and configure GRAND UNIFIED BOOTLOADER
download_grub = call("pacman -S grub os-prober", shell=True)
grub_install  = call("grub-install --recheck /dev/sda", shell=True)
grub_config = call("grub-mkconfig -o /boot/grub/grub.cfg", shell=True)

# sleep for few seconds.
time.sleep(60)
#####################################################################
#                       BASE SETTING                                #
#####################################################################

print "\033[40;1;31m Lets Configure Base Setting\033[0m"

# set password for root
print "\033[31m Enter the root password\033[0m"
passwd = call("passwrd", shell=True)

# set hostname
enter_hostname = raw_input("\033[32mEnter the hostname for your ARCH\033[0m")
conf_hostname = "echo "+hostname+" > /etc/hostname"
hostname = call(conf_hostname, shell=True)
