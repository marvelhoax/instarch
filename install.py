#!/usr/bin/python2
# This script is made by Marvel Hoax <marvelhoax@gmail.com>
# All contribution and suggestions are welcome

from subprocess import *
import time

print """\033[1;32m
	/$$$$$$                       /$$      /$$$$$$                      /$$      
	|_  $$_/                      | $$     /$$__  $$                    | $$      
	  | $$   /$$$$$$$   /$$$$$$$ /$$$$$$  | $$  \ $$  /$$$$$$   /$$$$$$$| $$$$$$$ 
	  | $$  | $$__  $$ /$$_____/|_  $$_/  | $$$$$$$$ /$$__  $$ /$$_____/| $$__  $$
	  | $$  | $$  \ $$|  $$$$$$   | $$    | $$__  $$| $$  \__/| $$      | $$  \ $$
	  | $$  | $$  | $$ \____  $$  | $$ /$$| $$  | $$| $$      | $$      | $$  | $$
	 /$$$$$$| $$  | $$ /$$$$$$$/  |  $$$$/| $$  | $$| $$      |  $$$$$$$| $$  | $$
	|______/|__/  |__/|_______/    \___/  |__/  |__/|__/       \_______/|__/  |__/
                                                                              
                                                                              
                                                                              \033[0m"""

time.sleep(5)

# Create a single partition and mark it bootable
create_partition = call("cfdisk /dev/sda", shell=True)

# Build ext4 filesystem on it
build_filesystem = call("mkfs.ext4 /dev/sda1", shell=True)

# Mount the new partition
mount = call("mount /dev/sda1 /mnt", shell=True)

# update pacman and install keyring
call("pacman -Syu",shell=True)
call("pacman -S archlinux-keyring")

# install the base system
base_sys = call("pacstrap /mnt base base-devel", shell=True)

def gen_fstab():
	# generate fstab
	gen_fstab = call("genfstab -U /mnt > /mnt/etc/fstab", shell=True)
	print "Genfstab command executed successfully"
	print "Its time to configure grub, This shit is not working and Allah is not helping me to figure out this problem"
	answer = raw_input("\033[1;34mDo you want to configure grub?")
	if answer == 'y' or answer == 'Y':
		configure_grub()
	else:
		print "You are looser!Fck this bitch..."

# chroot in to the new system
def configure_grub():
	call("arch-chroot /mnt pacman -S grub", shell=True)
	call("arch-chroot /mnt grub-install --target=i386-pc --debug /dev/sda", shell=True)
	call("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg", shell=True)
	print "\033[1;32m#####Grub Installed Successfully#############\033[0m"
	
print " "

gen_fstab()

# sleep for few seconds.
time.sleep(2)
#####################################################################
#                             BASE SETTING                          #
#####################################################################

print "\033[40;1;31m Lets Configure Base Setting\033[0m"

# set password for root
print "\033[31m Enter the root password\033[0m"
passwd = call("passwd", shell=True)

# set hostname
enter_hostname = raw_input("\033[32mEnter the hostname for your ARCH\033[0m")
conf_hostname = "arch-chroot /mnt echo ", enter_hostname, " > /etc/hostname"
hostname = call(conf_hostname, shell=True)

# add new user & set password
get_username = raw_input( "\033[31m Lets add new user & set password\033[0m")
set_username = "arch-chroot /mnt useradd "+ get_username
username = call(set_username, shell=True)
user_pass = "arch-chroot /mnt passwd "+ get_username
user_passwd = call(user_pass, shell=True)


# Adding user to sudoers file
addUser = "arch-chroot /mnt echo "+get_username+" ALL=(ALL:ALL) ALL >> /etc/sudoers"
Sudo = call(addUser, shell=True)

# Add user to wheel group
#add_wheel_group = "arch-chroot /mnt gpasswd -a "+get_username+" wheel"
#wheeel_grp = call(add_wheel_group, shell=True)
# edit sudoers to allow new user to sudo
#sudoers = call("arch-chroot /mnt cd /etc/");
#open_sudoers = open("sudoers", "a")
#write = get_username, " ALL=(ALL) ALL"
#open_sudoers.append(write)
#open_sudoers.close()
#file_sudoers = open("visudo", "w+")
#uncomment = file_sudoers.readline()
#if uncomment == "#%wheel ALL=(ALL) ALL":
	#uncomment.replace("#%wheel", " %whell")
#file_sudoers.close()

# check the name of your network interface
interface = call("ip link", shell=True)

# enable aquiring dynamic IP
enable_dynamic_ip = call("systemctl enable dhcpcd.service", shell=True)
start_dynamic_ip = call("systemctl start dhcpcd.service", shell=True)

# generate new locales & set one system wide
generate_locale = call("arch-chroot /mnt locale-gen", shell=True)
set_locale = call("arch-chroot /mnt localectl set-local LANG=en_US.UTF-8", shell=True)

# select timezone and set it permanent
tzselect = call("arch-chroot /mnt tzselect", shell=True)
set_timezone = call("arch-chroot /mnt timedatectl set-timezone 'Europe/Berlin'", shell=True)
	
# set hardware clock and sync using ntp
hwclock = call("arch-chroot /mnt hwclock --systohc --utc", shell=True)
set_ntp = call("arch-chroot /mnt timedatectl set-ntp true", shell=True)

# set hardware clock and sync using ntp
hwclock = call("arch-chroot /mnt hwclock --systohc --utc", shell=True)
set_ntp = call("arch-chroot /mnt timedatectl set-ntp true", shell=True)

################# BASIC SETTINGS OVER #################################

time.sleep(5)

#######################################################################
#                       DESKTOP ENVIRONMENT                           #
#######################################################################

print "\033[36m Installing Desktop Environment\033[0m"

print "1. AMD\n2. INTEL\n3. Nvdia"
video_hardware = raw_input("select the Brand for video driver")

if video_hardware == "1":
	# install the default video driver
	default_driver = call("arch-chroot /mnt pacman -S xf86-video-amdgpu", shell=True)
	if default_driver == "0":
		print "Video Driver installed successfully"
	else :
		print "Error in installing Video Driver. Try Again"
elif video_hardware == "2":
	default_driver = call("arch-chroot /mnt pacman -S xf86-video-intel", shell=True)
	if default_driver == "0":
		print "Video Driver installed successfully"
	else :
		print "Error in installing Video Driver. Try Again"
elif video_hardware == "3":
	default_hardware = call("arch-chroot /mnt pacman -S xf86-video-nouveau", shell=True)
	if default_driver == "0":
		print "Video Driver installed successfully"
	else :
		print "Error in installing Video Driver. Try Again"
else:
	print "Error in installing video driver"

# install OpenGL support
install_mesa = call("arch-chroot /mnt pacman -S mesa", shell=True)

# install video driver specific for your hardware
install_video_driver = call("arch-chroot /mnt pacman -S xf86-video-intel", shell=True)

# install Xorg packages
xorg_packages = call("arch-chroot /mnt pacman -S xorg-server xorg-utils xorg-xinit xterm",shell=True)
	
# fancy loading ^-^
time.sleep(1)
print "loading",
for x in range(1,5):
	print "\033[36m .\033[0m",
	
print ""

# installing Desktop Environment of your choice
print "Choose the Desktop Environment to Install for Your Arch"
print "1. Gnome\n2. KDE\n3. Xfce4\n4. Lxde\n5. Cinnamon\n6. MATE\n7. LXQt"
desktop = raw_input("Enter the number of desktop environment? ")
if desktop == "1":
	install_de = call("arch-chroot /mnt pacman -S gnome gnome-extra", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
elif desktop == "2":
	install_de = call("arch-chroot /mnt pacman -S kde kde-applications", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
elif desktop == "3":
	install_de = call("arch-chroot /mnt pacman -S xfce4 xfce4-goodies", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
elif desktop == "4":
	install_de = call("arch-chroot /mnt pacman -S lxde", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
elif desktop == "5":
	install_de = call("arch-chroot /mnt pacman -S cinnamon", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
elif desktop == "6":
	install_de = call("arch-chroot /mnt pacman -S mate", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
elif desktop == "7":
	install_de = call("arch-chroot /mnt pacman -S lxqt", shell=True)
	if install_de == "0":
		print "Desktop installed Successfully"
	else:
		print "Failed to install Desktop Environment"
else :
		print "Error in installing Desktop Environment"

# install & enable login manager lightdm
install_lightdm = call("arch-chroot /mnt pacman -S lightdm-gtk-greeter", shell=True)
enable_lightdm = call("arch-chroot /mnt systemctl enable lightdm.service", shell=True)
start_lightdm = call("arch-chroot /mnt systemctl start lightdm.service",shell=True)

############### DESKTOP ENVIROMENT INSTALLED #################

print "\n\n\n\n"
print "Volla! Arch is ready for customization. Just type reboot and start using Arch Linux"
