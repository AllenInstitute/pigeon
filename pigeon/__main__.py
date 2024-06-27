from .client import Pigeon
import argparse
import yaml
from functools import partial


def callback(disp_headers, msg, topic, headers):
    print(f"Recieved message on topic '{topic}':")
    print(msg)
    if disp_headers:
        print("With headers:")
        for key, val in headers.items():
            print(f"{key}={val}")


def main():
    parser = argparse.ArgumentParser(prog="Pigeon CLI")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The message broker to connect to.",
    )
    parser.add_argument(
        "--port", type=int, default=61616, help="The port to use for the connection."
    )
    parser.add_argument(
        "--username",
        type=str,
        help="The username to use when connecting to the STOMP server.",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="The password to use when connecting to the STOMP server.",
    )
    parser.add_argument(
        "-p", "--publish", type=str, help="The topic to publish a message to."
    )
    parser.add_argument(
        "-d", "--data", type=str, help="The YAML/JSON formatted data to publish."
    )
    parser.add_argument(
        "-s",
        "--subscribe",
        type=str,
        action="append",
        default=[],
        help="The topic to subscribe to.",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List registered topics and exit."
    )
    parser.add_argument(
        "--headers", action="store_true", help="Display headers of received messages."
    )

    args = parser.parse_args()

    if args.list:
        connection = Pigeon("CLI")
        for topic in connection._topics:
            print(topic)
        return

    if args.publish is None and args.subscribe is None:
        print("No action specified.")
        return

    if args.publish and args.data is None:
        print("Must also specify data to publish.")
        return

    if args.data and args.publish is None:
        print("Most also specify topic to publish data to.")
        return

    connection = Pigeon("CLI", args.host, args.port)
    connection.connect(args.username, args.password)

    if args.publish:
        connection.send(args.publish, **yaml.safe_load(args.data))

    for topic in args.subscribe:
        connection.subscribe(topic, partial(callback, args.headers))

    if args.subscribe:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("exiting")


if __name__ == "__main__":
    main()
