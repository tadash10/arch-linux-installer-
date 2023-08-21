import subprocess

def run_command(command, check=True):
    try:
        subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

# Define the partitions
partitions = [
    {"name": "/dev/sda1", "size": "512M", "fs": "ef00", "mount": "/boot", "format": "mkfs.fat -F32"},
    {"name": "/dev/sda2", "size": "2G", "fs": "8200", "swap": True},
    {"name": "/dev/sda3", "fs": "8300", "mount": "/", "format": "mkfs.ext4"},
    {"name": "/dev/sda4", "fs": "8300", "mount": "/home", "format": "mkfs.ext4"},
]

# Partition the disk
for partition in partitions:
    run_command(["parted", "-s", "/dev/sda", "mkpart", partition["fs"], "0%", partition["size"]])
    if partition.get("format"):
        run_command(["bash", "-c", f"{partition['format']} {partition['name']}"])

# Automatically detect root partition
root_partition = [p for p in partitions if p["mount"] == "/"][0]["name"]

# Mount the partitions
run_command(["mount", root_partition, "/mnt"])
for partition in partitions:
    if partition["mount"] != "/":
        run_command(["mkdir", "-p", f"/mnt{partition['mount']}"])
        run_command(["mount", partition["name"], f"/mnt{partition['mount']}"])

# Install the base system
run_command(["pacstrap", "/mnt", "base", "linux", "linux-firmware", "base-devel"])

# Generate fstab
run_command(["genfstab", "-U", "/mnt", "/mnt/etc/fstab"])

# Chroot into the new system
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm grub efibootmgr"])
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", f"grub-install --target=x86_64-efi --efi-directory={partitions[0]['mount']} --bootloader-id=arch"])
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "grub-mkconfig -o /boot/grub/grub.cfg"])
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm networkmanager"])
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "systemctl enable NetworkManager"])

# Install and configure desktop environment (e.g., GNOME)
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm gnome"])
run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "systemctl enable gdm"])

# Install additional software
# run_command(["arch-chroot", "/mnt", "/bin/bash", "-c", "pacman -S --noconfirm <additional-packages>"])

# Exit the chroot environment and reboot
run_command(["umount", "-R", "/mnt"])
run_command(["reboot"])
