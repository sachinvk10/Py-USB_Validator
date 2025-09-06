
 Py-USB_Validator
 =============== 
 A DSL-driven (Python Based)test suite to validate USB storage devices using predefined commands in `.tst` test files.
 
## Highlights:

•  USB detection limited to USB devices only
•  Partition creation and formatting
•  Mount/unmount with safe removal
•  File operations (copy, remove)
•  File checksum verification
•  Clean partition
•  Test runner with DSL support
•  Example test files

##  Features

- Detect USB devices (USB-only, filters out SATA/NVMe)
- Read detailed device metadata
- Create partitions with specified size
- Format partition as ext2, ext3, vfat, ntfs
- Mount & unmount USB partitions
- File operations:
  - Write file
  - Copy file
  - Remove file
  - Verify file checksum (integrity check)
- Safe removal
- Clean partition after test

## Project Structure:

usb_storage_test_suite/
├── README.md
├── src/
│   ├── usb_storage_api.py
│   └── usb_test_runner.py
└── tests/
    ├── usb_test_case.tst
    └── usb_fileops.tst
	
## DSL Command Reference

Command					Description
-------                 ------------
USBDetect				Detects USB devices
GetUSBMetadata			Prints metadata for USB device
CreatePartition size=	Creates a partition of given size (MB)
CreateFileSystem fs=	Formats partition as ext2/ext3/vfat/ntfs
USBMount				Mounts the partition to /mnt/usb_test
WriteTestFile			Writes a test file to USB
CopyFile				Copies file from src to dst
RemoveFile				Deletes file/folder
VerifyFileChecksum		Verifies checksum of file
SafeRemoval				Unmounts and marks USB safe to remove
CleanPartition			Wipes USB partition table


## Building a Standalone Executable (No Python Required for Tester)

	1. Install PyInstaller:
		#pip install pyinstaller
	 
	2. Build
		#cd usb_storage_test_suite
		#pyinstaller --onefile src/usb_test_runner.py

	3. Copy generated executable:
		#dist/usb_test_runner  ->  deploy folder

	4. Final structure for testers:

		usb_storage_test_deploy/
		├── usb_test_runner          # Executable
		└── tests/
			└── usb_fileops.tst      # Test case
		
	5. Tester can run:
		#sudo ./usb_test_runner tests/usb_fileops.tst

