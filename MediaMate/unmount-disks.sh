#!/bin/bash
# Unmount all disks
echo "Unmounting disks..."
diskutil unmount /Volumes/Disk1
diskutil unmount /Volumes/Disk2
diskutil unmount /Volumes/Disk3
diskutil unmount /Volumes/Disk4
echo "Done !"