import subprocess

# Define the partitions
partitions = [
    {"name": "/dev/sda1", "size": "512M", "fs": "ef00", "mount": "/boot", "format": "mkfs.fat -F32"},
    {"name": "/dev/sda2", "size": "2G", "fs": "8200", "swap": True},
    {"name": "/dev/sda3", "size": "20G", "fs": "8300", "mount": "/", "format": "mkfs.ext4"},
    {"name": "/dev/sda4", "fs": "8300", "mount": "/home", "format": "mkfs.ext4"},
]

# Partition the disk
for partition in partitions:
    subprocess.run(["parted", "-s", "/dev/sda", "mklabel", "gpt"])
    subprocess.run(["parted", "-s", "/dev/sda", "mkpart", partition["fs"], "0%", partition["size"]])
    if partition.get("format"):
        subprocess.run(["bash", "-c", f"{partition['format']} {partition['name']}"])

# Mount the partitions
subprocess.run(["mount", partitions[2]["name"], "/mnt"])
subprocess.run(["mkdir", "-p", "/mnt/boot"])
subprocess.run(["mount", partitions[0]["name"], "/mnt/boot"])
subprocess.run(["mkdir", "-p", "/mnt/home"])
subprocess.run(["mount", partitions[3]["name"], "/mnt/home"])

# Install the base system
subprocess.run(["pacstrap", "/mnt", "base", "base-devel", "linux", "linux-firmware"])

# Generate fstab
subprocess.run(["genfstab", "-U", "/mnt", "/mnt/etc/fstab"])

# Chroot into the new system
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm grub efibootmgr"])
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=arch"])
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "grub-mkconfig -o /boot/grub/grub.cfg"])
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm networkmanager"])
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "systemctl enable NetworkManager"])

# Install and configure desktop environment (e.g., GNOME)
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm gnome"])
subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "systemctl enable gdm"])

# Install additional software
# subprocess.run(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm <additional-packages>"])

# Exit the chroot environment and reboot
subprocess.run(["umount", "-R", "/mnt"])
subprocess.run(["reboot"])
