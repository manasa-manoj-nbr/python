import ftplib

def connect_ftp():
    server = input("Enter FTP Server Address: ")
    port = int(input("Enter Port: "))
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        ftp = ftplib.FTP()
        ftp.connect(server, port)
        ftp.login(user=username, passwd=password)
        print("Connected to FTP server!")
        return ftp
    except Exception as e:
        print("Connection failed:", e)
        return None


def list_files(ftp):
    try:
        print("\nFiles on server:")
        files = ftp.nlst()
        for f in files:
            print(f)
    except Exception as e:
        print("rror listing files:", e)


def upload_file(ftp):
    filepath = input("Enter local file path to upload: ").strip().replace("\\", "/")
    dest_name = input("Enter destination filename on server: ")

    try:
        with open(filepath, 'rb') as file:
            ftp.storbinary(f"STOR {dest_name}", file)
        print(f"Uploaded '{filepath}' as '{dest_name}'")
    except Exception as e:
        print(" Upload failed:", e)


def download_file(ftp):
    remote_name = input("Enter filename to download from server: ")
    save_path = input("Enter local path to save the file: ")

    try:
        with open(save_path, 'wb') as file:
            ftp.retrbinary(f"RETR {remote_name}", file.write)
        print(f"Downloaded '{remote_name}' to '{save_path}'")
    except Exception as e:
        print("Download failed:", e)


def main():
    ftp = connect_ftp()
    if not ftp:
        return

    while True:
        print("\n--- FTP Operations ---")
        print("1. List Files")
        print("2. Upload File")
        print("3. Download File")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            list_files(ftp)
        elif choice == "2":
            upload_file(ftp)
        elif choice == "3":
            download_file(ftp)
        elif choice == "4":
            ftp.quit()
            print("Disconnected from server.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()