# Extended USB File Operations test

USBDetect
GetUSBMetadata
CreatePartition size=200
CreateFileSystem fs=ext3
USBMount

# Create a test file
WriteTestFile name=hello.txt content="This is a test file."

# Copy file within USB mount
CopyFile src=/mnt/usb_test/hello.txt dst=/mnt/usb_test/copy_hello.txt

# Verify checksum of original and copied file
VerifyFileChecksum path=/mnt/usb_test/hello.txt checksum=81f4cba6b0850ed55eaed8d4c9cc3a7c350c9dc420ed863792cc3c363f3b2f0e
VerifyFileChecksum path=/mnt/usb_test/copy_hello.txt checksum=81f4cba6b0850ed55eaed8d4c9cc3a7c350c9dc420ed863792cc3c363f3b2f0e

# Remove copied file
RemoveFile path=/mnt/usb_test/copy_hello.txt

# Safely unmount device
SafeRemoval

CleanPartition
