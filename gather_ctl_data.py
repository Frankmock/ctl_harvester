import logging, sys, certstream, sqlite3, os, json, datetime

int(datetime.datetime.now().timestamp())

db=f"/opt/ctl_harvesting/var/data/ctl-{str(int(datetime.datetime.now().timestamp()))}.sqlite3"

if sys.argv[1] == "store_certs":
    store_certs = True
else:
    store_certs = False

if os.path.isfile(db):
    conn = sqlite3.connect(db)
    cdb = conn.cursor()
else:
    conn = sqlite3.connect(db)
    cdb = conn.cursor()
    cdb.execute('CREATE TABLE "records" ("dns" TEXT,"source" TEXT,"source_info" TEXT,"time" INTEGER,PRIMARY KEY("dns"));')
    cdb.execute('CREATE TABLE "certificates" ("fingerprint" TEXT,"json" TEXT,PRIMARY KEY("fingerprint"));')

def print_callback(message, context):
    # logging.debug("Message -> {}".format(mess age))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        if store_certs:
            try:
                messageforstorage = json.dumps(message['data']).replace("'", "")
                cdb.execute(f"INSERT INTO certificates VALUES ('{message['data']['leaf_cert']['fingerprint']}','{messageforstorage}')")
            except sqlite3.IntegrityError:
                pass

        for d in message['data']['leaf_cert']['all_domains']:
            try:
                sqlcommand=f"INSERT INTO records VALUES ('{d}','ctl','{message['data']['leaf_cert']['fingerprint']}',{datetime.datetime.now().timestamp()})"
                cdb.execute(sqlcommand)
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        # sys.stdout.write(f"Certificate issued for: {str(message['data']['leaf_cert']['all_domains'])} by {message['data']['leaf_cert']['issuer']['O']}\n")
        # sys.stdout.flush()

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')
