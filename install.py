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

if chroot not 0:
	print "Error in changing the root!"
else:
	print ""

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
	conf_hostname = "echo ", enter_hostname, " > /etc/hostname"
	hostname = call(conf_hostname, shell=True)

	# add new user & set password
	get_username = raw_input( "\033[31m Lets add new user & set password\033[0m")
	set_username = "useradd -m -G whell ",get_username
	user_pass = "passwd ", get_username
	user_passwd = call(user_pass, shell=True)

	# edit sudoers to allow new user to sudo
	file_sudoers = open("visudo", "w+")
	uncomment = file_sudoers.readline()
	if uncomment == "#%wheel ALL=(ALL) ALL":
		uncomment.replace("#", " ")

	file_sudoers.close()

	# check the name of your network interface
	interface = call("ip link", shell=True)

	# enable aquiring dynamic IP
	enable_dynamic_ip = call("systemctl enable dhcpcd.service", shell=True)
	start_dynamic_ip = call("systemctl start dhcpcd.service", shell=True)

	# generate new locales & set one system wide
	generate_locale = call("locale-gen", shell=True)
	set_locale = call("localectl set-local LANG=en_US.UTF-8", shell=True)

	# select timezone and set it permanent
	tzselect = call("tzselect", shell=True)
	set_timezone = call("timedatectl set-timezone 'Europe/Berlin'", shell=True)

	# set hardware clock and sync using ntp
	hwclock = call("hwclock --systohc --utc", shell=True)
	set_ntp = call("timedatectl set-ntp true" shell=True)

	################# BASIC SETTINGS OVER #################################

	time.delay(60)
	#######################################################################
	#                       DESKTOP ENVIRONMENT                           #
	#######################################################################

	print "\033[36m Installing Desktop Environment\033[0m"

	# install the default video driver
	default_driver = call("pacman -S xf86-video-vesa", shell=True)

	# install OpenGL support
	install_mesa = call("pacman -S mesa", shell=True)

	# install video driver specific for your hardware
	install_video_driver = call("pacman -S xf86-video-intel", shell=True)

	# install Xorg packages
	xorg_packages = call("pacman -S xorg-server xorg-utils xorg-xinit xterm",shell=True)

	# fancy loading ^-^
	time.sleep(1)
	print "loading",
	for x in range(1,5):
		print "\033[36m .\033[0m",


	print ""

	# installing Desktop Environment of your choice
	install_de = call("pacman -S xfce4 xfce4-goodies", shell=True)

	# install & enable login manager lightdm
	install_lightdm = call("pacman -S lightdm-gtk-greeter", shell=True)
	start_lightdm = call("systemctl enable lightdm.service", shell=True)

	############### DESKTOP ENVIROMENT INSTALLED #################


print "Volla! Arch is ready for customization. Just type reboot and start using Arch Linux"
