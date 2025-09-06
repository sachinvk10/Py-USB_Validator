from usb_storage_api import USBStorageAPI
import shutil
import os


context = {
    "device": None,
    "partition": None,
    "mount_point": "/mnt/usb_test"
}


def run_command(command_line):
    tokens = command_line.strip().split()
    if not tokens or tokens[0].startswith("#"):
        return

    cmd = tokens[0]
    args = dict(token.split("=", 1) for token in tokens[1:]) if len(tokens) > 1 else {}

    if cmd == "USBDetect":
        devices = USBStorageAPI.USBDetect()
        context["device"] = devices[0]

    elif cmd == "GetUSBMetadata":
        USBStorageAPI.GetUSBMetadata(context["device"])

    elif cmd == "CreatePartition":
        size = int(args.get("size", 100))
        context["partition"] = USBStorageAPI.CreatePartition(context["device"], size_mb=size)

    elif cmd == "CreateFileSystem":
        fs = args.get("fs", "ext3")
        USBStorageAPI.CreateFileSystem(context["partition"], fs_type=fs)

    elif cmd == "USBMount":
        context["mount_point"] = USBStorageAPI.USBMount(context["partition"])

    elif cmd == "WriteTestFile":
        fname = args.get("name", "test.txt")
        content = args.get("content", "Test file content")
        path = os.path.join(context["mount_point"], fname)
        with open(path, "w") as f:
            f.write(content)
        print(f"[WriteTestFile] Wrote file to {path}")

    elif cmd == "USBUnmount":
        USBStorageAPI.USBUnmount(context["mount_point"])

    elif cmd == "CleanPartition":
        USBStorageAPI.CleanPartition(context["device"])

    elif cmd == "CopyFile":
        src = args.get("src")
        dst = args.get("dst")
        if not src or not dst:
            print("[ERROR] CopyFile requires src and dst arguments.")
            return
        USBStorageAPI.CopyFile(src, dst)

    elif cmd == "RemoveFile":
        path = args.get("path")
        if not path:
            print("[ERROR] RemoveFile requires path argument.")
            return
        USBStorageAPI.RemoveFile(path)

    elif cmd == "VerifyFileChecksum":
        path = args.get("path")
        checksum = args.get("checksum")
        algo = args.get("algo", "sha256")
        if not path or not checksum:
            print("[ERROR] VerifyFileChecksum requires path and checksum arguments.")
            return
        USBStorageAPI.VerifyFileChecksum(path, checksum, algo)

    elif cmd == "SafeRemoval":
        USBStorageAPI.SafeRemoval(context["mount_point"])

    else:
        print(f"[ERROR] Unknown command: {cmd}")


def run_test_file(filename):
    with open(filename, "r") as f:
        for line in f:
            run_command(line)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: sudo python3 usb_test_runner.py testfile.tst")
        exit(1)

    test_file = sys.argv[1]
    try:
        run_test_file(test_file)
    except Exception as e:
        print(f"[FAIL] Error occurred: {e}")
    finally:
        shutil.rmtree(context["mount_point"], ignore_errors=True)
