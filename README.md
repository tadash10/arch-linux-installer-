# arch-linux-installer-

Arch Linux Automated Installation Script

This script automates the installation process of Arch Linux on a target system. It sets up the partitions, installs the base system, configures the bootloader, and installs the GNOME desktop environment. The script is designed to simplify the installation process and make it more user-friendly.
Prerequisites

    A bootable USB drive with the Arch Linux ISO burned onto it.
    Basic understanding of Arch Linux installation process and partitioning.

Usage

    Boot the target system from the USB drive containing the Arch Linux ISO.

    Once the system boots into the Arch Linux environment, make sure you have an internet connection.

    Open a terminal and navigate to the directory containing the script.

    Execute the script by running the following command:

    bash

    python script.py

    Replace script.py with the actual name of the script file.

    The script will guide you through the installation process and will perform the following steps:
        Partition the disk according to your specified partitions.
        Automatically detect the root partition.
        Mount partitions.
        Install the base system, including necessary packages.
        Generate the /etc/fstab file.
        Set up the bootloader (GRUB) with UEFI support.
        Install and enable NetworkManager for network connectivity.
        Install the GNOME desktop environment and enable GDM.

    After the script completes, the system will prompt you to reboot. Remove the USB drive and reboot the system.

Customization

You can customize the script by modifying the partitions list at the beginning of the script. Each partition entry includes information about the partition name, size, filesystem type, mount point, and whether it should be formatted. You can also modify the install_desktop_environment function to install a different desktop environment if desired.
Disclaimer

This script is provided as-is and without any warranty. Use it at your own risk. Make sure to backup any important data before running the script.
License

This script is released under the MIT License. You are free to use, modify, and distribute it according to the terms of the license.
