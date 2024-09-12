import sys
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'usage {sys.argv[0]} <nslookup output file>')
        exit(1)
    input_file = sys.argv[1]
    with open(input_file, 'r') as infile:
        content = infile.readlines()
        hostname, address = "", ""
        for line in content:
            if line.startswith("Name:"):
                hostname = ""
                address = ""
                hostname = line.split("\t")[-1].strip()
            else:
                if "Address:" in line and "#" not in line:
                    address = line.split(" ")[-1].strip()
                else:
                    if not hostname or not address:
                        continue
                    print(f"{hostname}\t{address}")

