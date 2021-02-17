import os, time, shutil, re
os.chdir("/opt/ctl_harvesting/bin")

def regex_filter_list(regex, list):
    rex = re.compile(regex)
    return [l for l in list if rex.match(l)]

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

found=False
for pid in pids:
    d = open(f"/proc/{pid}/cmdline", 'rb').read().decode().replace("\x00", " ")
    if d == "/bin/python3 /opt/ctl_harvesting/bin/gather_ctl_data.py dont_store_certs ":
        found=True
        break

if int(pid) > 10000 and found:
    print(f"Starting a new process...")
    resp = os.system("/bin/python3 /opt/ctl_harvesting/bin/gather_ctl_data.py dont_store_certs &")
    time.sleep(5)
    print(f"Killing process {pid} with command line: '{d}'")
    os.system(f"/bin/kill -9 {pid}")

    files = next(os.walk(f"/opt/ctl_harvesting/var/data"))[2]
    db_file = regex_filter_list("^ctl-[0-9]{10,20}.sqlite3$", files)
    journal_file = regex_filter_list("^ctl-[0-9]{10,20}.sqlite3\-journal$", files)
    db_file.sort()
    db_file.pop()


    for f in db_file:
        shutil.move(f"/opt/ctl_harvesting/var/data/{f}", f"/opt/ctl_harvesting/var/data/ready_to_process/{f}")
        print(f"Moved /opt/ctl_harvesting/var/data/{f} to the directory /opt/ctl_harvesting/var/data/ready_to_process/{f}")

    if len(journal_file) >1:
        journal_file.sort()
        journal_file.pop()
        for f in journal_file:
            os.remove(f"/opt/ctl_harvesting/var/data/{f}")
            print(f"Removed /opt/ctl_harvesting/var/data/{f}")




