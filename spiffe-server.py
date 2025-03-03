# Create a TLS server with SPIFFE-based MTLS
from spiffetls import listen, ListenOptions
from spiffe import SpiffeId, X509Source
from spiffetls.mode import ServerTlsMode
from spiffetls.tlsconfig.authorize import authorize_id, authorize_one_of
import logging, sys

logger = logging.getLogger("spiffe-server")
logging.basicConfig(format="%(name)s[%(lineno)d] - %(message)s", stream=sys.stdout)
logger.setLevel(logging.INFO)

# This SPIFFE ID (SVID)will be the server's ID. Clients will need to authorize this SVID for use.
this_spiffe_id = "spiffe://paulc-trial.teleport.sh/svc/server"

# This is a list of authorized client IDs, ie. client IDs that are allowed to connect.
valid_spiffe_ids = [
    "spiffe://paulc-trial.teleport.sh/svc/client"
]

"""
This function returns the SVID for this server. The WorkloadAPI (and tbot) can return more than one
SVID. In order to ensure the server is using the correct one, this function just iterates the list until
the chosen SVID is found. Returns None if not found.
"""
def server_svid(svid_list):
    for svid in svid_list:
        if (svid.spiffe_id == this_spiffe_id):
            return svid
    logger.error("The WorkloadAPI did not return the SVID for this server.")
    return None

x509_source = X509Source(svid_picker=server_svid)
options = ListenOptions(
    tls_mode=ServerTlsMode.MTLS,
    authorize_fn=authorize_one_of(allowed_ids=valid_spiffe_ids),
)

try:
    listener = listen("localhost:8443", x509_source, options)
except Exception as e:
    logger.error(str(e))
    sys.exit(1)


logger.info("This server SPIFFE ID: " + str(x509_source.svid.spiffe_id))

while True:
    connection, client_address = listener.accept()
    print('\n')
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                break
            logger.info("Received: " + data.decode('utf-8'))
            connection.send('Thank you for connecting'.encode()) 
            connection.close()
        except Exception as e:
            if e.args[0] == 9:
                logger.info("Connection closed.")
            else:
                logger.error(str(e))
            break
