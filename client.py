import socket
from pathlib import Path
from string_generator import StringGenerator, StringGeneratorConfig
import time
from logging_config import logger
import argparse

def parse_range(s: str):
    if ':' in s:
        ini, fin = map(int, s.split(':'))
        return (ini, fin)
    val = int(s)
    return (val, val)

def parse_args():
    parser = argparse.ArgumentParser(description="String generator client.")
    parser.add_argument('--count', type=int, default=10, help="Number of strings to generate.")
    parser.add_argument('--length', type=parse_range, default="50:100", help="Fixed length or range (e.g. 10 or 10:20).")
    parser.add_argument('--spaces', type=parse_range, default="3:5", help="Number of spaces (e.g.: 3 or 2:4).")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Server IP address")
    parser.add_argument('--output', type=str, default="results.txt", help="File to save the results")
    parser.add_argument('--port', type=int, default=65432, help="Server port.")
    return parser.parse_args()

def main():
    args = parse_args()
    config = StringGeneratorConfig(length=args.length, count=args.count, blank_spaces=args.spaces)

    HOST = args.host
    PORT = args.port
    OUTPUT_FILE = args.output
    INPUT_FILE = 'chains.txt'

    generator = StringGenerator(config)

    logger.info("starting process...")
    logger.info("creating chains.txt")
    generator.write_to_file(INPUT_FILE)
    logger.info("done creating chains.txt")

    start_time = time.perf_counter()
    with socket.create_connection((HOST, PORT)) as sock, \
        open(OUTPUT_FILE, "w", encoding="utf-8") as fout, \
        open(INPUT_FILE, 'r', encoding='utf-8') as fin:

        for cadena in fin:
            sock.sendall((cadena).encode('utf-8'))

            data = b""
            while not data.endswith(b'\n'):
                data += sock.recv(1024)
            data = data.decode('utf-8').strip()
            if data.startswith('['):
                result = data
                logger.info(f"'{result}")
            else:
                result = float(data)
                fout.write(f"{cadena.strip()} -> {result}\n")
                logger.info(f"'{cadena.strip()}' -> {result}")
            pass

    total_time = time.perf_counter() - start_time
    logger.info(f"Tiempo total del proceso: {total_time} segundos")

if __name__ == "__main__":
    main()
