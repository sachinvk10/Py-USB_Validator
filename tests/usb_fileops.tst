# usb_fileops.tst - USB File operations & integrity test

USBDetect
GetUSBMetadata
CreatePartition size=200
CreateFileSystem fs=ext3
USBMount

WriteTestFile name=hello.txt content="This is a test file."

CopyFile src=/mnt/usb_test/hello.txt dst=/mnt/usb_test/copy_hello.txt

VerifyFileChecksum path=/mnt/usb_test/hello.txt checksum=81f4cba6b0850ed55eaed8d4c9cc3a
