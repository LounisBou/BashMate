#!/bin/bash
# Mount all disks
echo "Create disks directories if they don't exist..."
sudo mkdir -p /Volumes/Disk1
sudo mkdir -p /Volumes/Disk2
sudo mkdir -p /Volumes/Disk4
sudo mkdir -p /Volumes/Disk3
echo "Mounting disks..."
sudo /opt/homebrew/sbin/mount_ntfs -o rw,auto,nobrowse /dev/disk4s2 /Volumes/Disk1
sudo /opt/homebrew/sbin/mount_ntfs -o rw,auto,nobrowse /dev/disk5s1 /Volumes/Disk2
sudo /opt/homebrew/sbin/mount_ntfs -o rw,auto,nobrowse /dev/disk6s2 /Volumes/Disk3
sudo /opt/homebrew/sbin/mount_ntfs -o rw,auto,nobrowse /dev/disk7s1 /Volumes/Disk4
echo "Done !"