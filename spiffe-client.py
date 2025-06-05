# Establish a secure connection to a TLS server
from spiffetls import dial
from spiffe import SpiffeId, X509Source
from spiffetls.tlsconfig.authorize import authorize_id
import logging, sys
from OpenSSL import SSL

logger = logging.getLogger("spiffe-client")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format="%(name)s[%(lineno)d] - %(message)s", stream=sys.stdout)

server_svid = "spiffe://paulc-demo.teleport.sh/svc/server"

if len(sys.argv) == 3:
    this_spiffe_id = sys.argv[2]
else:
    this_spiffe_id = "spiffe://paulc-demo.teleport.sh/svc/client"

"""
This function returns the SVID for this client. The WorkloadAPI (and tbot) can return more than one
SVID. In order to ensure the client is using the correct one, this function just iterates the list until
the chosen SVID is found. Returns None if not found.
"""
def client_svid(svid_list):
    for svid in svid_list:
        if (svid.spiffe_id == this_spiffe_id):
            return svid
    logger.error("The WorkloadAPI did not return the SVID for this application.")
    return None


x509_source = X509Source(svid_picker=client_svid)

try:
    conn = dial(
        sys.argv[1],
        x509_source,
        authorize_fn=authorize_id(server_svid),
    )
except Exception as e:
    logger.error(e)
    sys.exit(1)

logger.info(f"Connecting with {x509_source.svid.spiffe_id}")

try:
    conn.write(b"GET / HTTP/1.0\n\n")
    while True:
        try:
            data = conn.recv(4096)
            print(data.decode('utf-8'))
        except SSL.SysCallError:
            break
        if not data:
           break
    conn.close()
except Exception as e:
    logger.info(str(e))

