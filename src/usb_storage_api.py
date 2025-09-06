import subprocess
import os
import json
import shutil
import hashlib


class USBStorageAPI:

    @staticmethod
    def USBDetect():
        print("[USBDetect] Scanning for USB storage devices...")
        try:
            output = subprocess.check_output(['lsblk', '-o', 'NAME,TRAN,TYPE', '-J']).decode()
            devices = json.loads(output).get("blockdevices", [])

            usb_devices = []
            for dev in devices:
                name = dev.get("name")
                tran = dev.get("tran")
                dtype = dev.get("type")

                if tran == "usb" and dtype == "disk":
                    usb_devices.append(f"/dev/{name}")

            if not usb_devices:
                raise RuntimeError("No USB storage devices found.")

            print(f"[USBDetect] USB devices detected: {usb_devices}")
            return usb_devices

        except subprocess.CalledProcessError as e:
            raise RuntimeError("Failed to detect USB devices.") from e

    @staticmethod
    def GetUSBMetadata(device):
        print(f"[GetUSBMetadata] Gathering metadata for {device}...\n")

        try:
            lsblk_output = subprocess.check_output(
                ['lsblk', '-o', 'NAME,SIZE,MOUNTPOINT,FSTYPE,LABEL,UUID,MODEL,VENDOR', '-J']
            ).decode()
            devices = json.loads(lsblk_output).get("blockdevices", [])

            metadata = None
            devname = device.replace("/dev/", "")

            for dev in devices:
                if dev["name"] == devname:
                    metadata = dev
                    break

            if not metadata:
                raise RuntimeError(f"Device metadata for {device} not found.")

            print("📦 USB Device Metadata:")
            print(f"  Device:     /dev/{metadata.get('name')}")
            print(f"  Size:       {metadata.get('size')}")
            print(f"  Filesystem: {metadata.get('fstype')}")
            print(f"  Label:      {metadata.get('label')}")
            print(f"  UUID:       {metadata.get('uuid')}")
            print(f"  Model:      {metadata.get('model')}")
            print(f"  Vendor:     {metadata.get('vendor')}")
            print(f"  Mountpoint: {metadata.get('mountpoint') or 'Not mounted'}")

            return metadata

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to fetch metadata for {device}") from e

    @staticmethod
    def CreatePartition(device, size_mb):
        print(f"[CreatePartition] Creating {size_mb}MB partition on {device}...")

        subprocess.run(["sudo", "parted", "-s", device, "mklabel", "msdos"], check=True)
        subprocess.run(["sudo", "parted", "-s", device, "mkpart", "primary", "1MiB", f"{size_mb}MiB"], check=True)

        partition = device + "1"
        print(f"[CreatePartition] Partition created: {partition}")
        return partition

    @staticmethod
    def CreateFileSystem(partition, fs_type):
        print(f"[CreateFileSystem] Formatting {partition} as {fs_type}...")

        fs_map = {
            "ext2": "mkfs.ext2",
            "ext3": "mkfs.ext3",
            "vfat": "mkfs.vfat",
            "ntfs": "mkfs.ntfs"
        }

        if fs_type not in fs_map:
            raise ValueError(f"Unsupported filesystem: {fs_type}")

        subprocess.run(["sudo", fs_map[fs_type], partition], check=True)
        print(f"[CreateFileSystem] {fs_type.upper()} filesystem created.")
        return True

    @staticmethod
    def USBMount(partition, mount_point="/mnt/usb_test"):
        print(f"[USBMount] Mounting {partition} at {mount_point}...")

        os.makedirs(mount_point, exist_ok=True)
        subprocess.run(["sudo", "mount", partition, mount_point], check=True)

        print(f"[USBMount] Mounted at {mount_point}")
        return mount_point

    @staticmethod
    def USBUnmount(mount_point="/mnt/usb_test"):
        print(f"[USBUnmount] Unmounting {mount_point}...")
        subprocess.run(["sudo", "umount", mount_point], check=True)
        print(f"[USBUnmount] Unmounted.")
        return True

    @staticmethod
    def CleanPartition(device):
        print(f"[CleanPartition] Wiping partition table on {device}...")
        subprocess.run(["sudo", "wipefs", "--all", device], check=True)
        print(f"[CleanPartition] Wipe complete.")
        return True

    @staticmethod
    def CopyFile(src, dst):
        print(f"[CopyFile] Copying {src} to {dst}...")
        shutil.copy2(src, dst)
        print("[CopyFile] Copy successful.")

    @staticmethod
    def RemoveFile(path):
        print(f"[RemoveFile] Removing {path}...")
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        print("[RemoveFile] Remove successful.")

    @staticmethod
    def VerifyFileChecksum(path, expected_checksum, algorithm="sha256"):
        print(f"[VerifyFileChecksum] Calculating {algorithm} checksum for {path}...")
        h = hashlib.new(algorithm)
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        calc_checksum = h.hexdigest()
        print(f"  Expected:   {expected_checksum}")
        print(f"  Calculated: {calc_checksum}")
        if calc_checksum == expected_checksum:
            print("[VerifyFileChecksum] Checksum matches!")
            return True
        else:
            print("[VerifyFileChecksum] Checksum mismatch!")
            return False

    @staticmethod
    def SafeRemoval(mount_point="/mnt/usb_test"):
        print(f"[SafeRemoval] Unmounting {mount_point} safely...")
        USBStorageAPI.USBUnmount(mount_point)
        print("[SafeRemoval] Device is safe to remove.")
        return True
