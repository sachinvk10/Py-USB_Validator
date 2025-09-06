# usb_test_case.tst - basic USB test script

USBDetect
GetUSBMetadata
CreatePartition size=100
CreateFileSystem fs=ext3
USBMount
WriteTestFile name=hello.txt content="USB is working!"
USBUnmount
CleanPartition
