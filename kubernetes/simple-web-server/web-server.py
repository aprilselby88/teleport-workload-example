
import http.server, logging, sys, os
from http.server import SimpleHTTPRequestHandler

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)
http_logger = logging.getLogger()

class RequestHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        msg = ("%s - - [%s] %s\n" % (self.headers.get('X-Real-Ip'),self.log_date_time_string(),format%args)).strip()
        http_logger.info(msg)

server_listen_port = int(os.getenv("WEB_SERVER_LISTEN_PORT", "8000"))
server_bind_address = os.getenv("WEB_SERVER_BIND_ADDRESS", "0.0.0.0")

server = http.server.HTTPServer((server_bind_address, server_listen_port), RequestHandler)
server.serve_forever()
