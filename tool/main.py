import sys
import tarfile


def main():
    with tarfile.open(
        fileobj=sys.stdin.buffer,
        mode="r|",
    ) as tar:
        with tarfile.open(
            fileobj=sys.stdout.buffer,
            mode="w|",
        ) as out_tar:
            for member in tar:
                pax_headers = list(member.pax_headers.items())
                print(
                    f"Received entry: {member.name}, Type: {member.type}, Size: {member.size}",
                    file=sys.stderr,
                )
                print(f"PAX headers: {pax_headers}", file=sys.stderr)
                fileobj = tar.extractfile(member)
                out_tar.addfile(member, fileobj)


if __name__ == "__main__":
    main()
