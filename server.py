import socket
import threading
from rules import ContainsRule, RuleManager
from logging_config import logger

HOST = '127.0.0.1'
PORT = 65432

double_a_rule = ContainsRule(substring='aa', ignore_case=True, message='Double "a" rule detected')

chain_rules = [
    double_a_rule
]
rule_manager = RuleManager(chain_rules)

def get_string_weighting(cadena: str) -> float:
    """Computes the weighting coefficient of a string.

    Formula:
        (1.5 * letters + 2 * digits) / number of spaces

    Args:
        cadena (str): The input string.

    Returns:
        float: The computed coefficient, or -1.0 if no spaces are present.
    """
    letters = sum(1 for c in cadena if c.isalpha())
    numbers = sum(1 for c in cadena if c.isdigit())
    spaces = cadena.count(' ')
    if spaces == 0:
        return -1
    return (letters * 1.5 + numbers * 2) / spaces

def handle_client(conn, addr):
    """Handles a single client connection.

    Processes each string sent by the client:
    - Applies rules via RuleManager
    - Sends back either the computed coefficient or an error message
    """
    with conn:
        logger.info(f"[+] connection established from {addr}")
        # Accumulate incoming data in buffer until newline is found
        # Then extract and process each complete line
        buffer = ''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)

                # Check if the line should be ignored based on rules
                not_valid_rule_message = rule_manager.test_rules(line)

                if not not_valid_rule_message: # If valid, compute the coefficient and send it back to the client
                    pound = get_string_weighting(line.strip())
                    conn.sendall(f"{pound:.4f}\n".encode('utf-8'))
                else:
                    logger.info(f'chain "{line}" did not pass a rule -> {not_valid_rule_message}')
                    conn.sendall(f'[error] {not_valid_rule_message} >> {line}\n'.encode('utf-8'))

def start_server():
    """Starts the TCP server and listens for client connections.

    For each new connection, a dedicated thread is spawned.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"[i] server listenning on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    # --- Server entry point ---
    # Binds to a TCP socket and handles multiple incoming connections.
    start_server()
