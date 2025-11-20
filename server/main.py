import tarfile

from http.server import HTTPServer, BaseHTTPRequestHandler


# echo server
class EchoServer(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"Content-Type: {self.headers['Content-Type']}")
        self.send_response(200)
        self.send_header("Content-Type", "application/x-tar")
        self.end_headers()

        # decode tar stream and respond with the same tar stream
        with tarfile.open(
            fileobj=self.rfile,
            mode="r|",
            format=tarfile.PAX_FORMAT,
            ignore_zeros=True,
            debug=3,
        ) as tar:
            with tarfile.open(
                fileobj=self.wfile, mode="w|", format=tarfile.PAX_FORMAT
            ) as out_tar:
                for member in tar:
                    pax_headers = list(member.pax_headers.items())
                    print(
                        f"Received entry: {member.name}, Type: {member.type}, Size: {member.size}"
                    )
                    print(f"PAX headers: {pax_headers}")
                    print()
                    fileobj = tar.extractfile(member)
                    out_tar.addfile(member, fileobj)


def main():
    # simplest http server

    server_address = ("", 8080)
    httpd = HTTPServer(server_address, EchoServer)
    print("Starting server on port 8080...")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
