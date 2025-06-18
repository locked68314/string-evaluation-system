# String Evaluation System (Client-Server Architecture)

This project implements a scalable client-server system for evaluating strings based on configurable rules. The client generates strings, sends them to a server over a socket connection, and receives a numeric coefficient as a response. The server filters or evaluates strings according to modular, customizable rules.

---

## Features

### Server
- Receives strings from one or more clients.
- Filters strings based on rules (e.g., ignore strings starting with `"aa"` case-insensitive).
- Calculates a **coefficient** for accepted strings:

  \[
  \text{coefficient} = \frac{1.5 \cdot \text{letter_count} + 2 \cdot \text{digit_count}}{\text{space_count}}
  \]

- Returns the coefficient to the client as a string (e.g. `"5.3333\n"`).
- Logs ignored strings with a custom reason per rule.

### Client
- Reads strings from a file or generates them on demand.
- Sends each string to the server and stores the response.
- Supports command-line configuration for:
  - Server IP and port
  - Number of strings to generate
  - Range or fixed string length
  - Range or fixed number of spaces
  - Input/output files
- Measures total processing time.

### Rules
- Each filter is defined as a class implementing a common interface.
- Rules can return custom ignore messages.
- New rules can be easily added without modifying the main logic.
- Rules can be composed and evaluated independently.

---

## Usage

### Start the Server

```bash
python server.py
```

The server listens on `127.0.0.1:65432` by default. You can customize this in the code.

---

### Run the Client

#### 1. Generate and process strings:

```bash
python client.py --count 10 --length 50:100 --spaces 3:5 --host 127.0.0.1 --port 65432 --output results.txt
```

---

## Configuration Parameters

| Argument       | Description                                     | Example        |
|----------------|-------------------------------------------------|----------------|
| `--count`      | Number of strings to generate                   | `--count 100`  |
| `--length`     | Fixed or range length per string                | `--length 10:20` |
| `--spaces`     | Fixed or range number of spaces per string      | `--spaces 3:5` |
| `--output`     | Output file for results                         | `--output out.txt` |
| `--host`       | Server IP address                               | `--host 192.168.0.10` |
| `--port`       | Server port                                     | `--port 9000` |


---

## Project Structure (Suggested)

```
project/
├── client.py              # Client script
├── server.py              # Server script
├── string_generator.py    # Modular string generator
├── rules.py               # Rule classes and manager
├── chains.txt             # (optional) input data
├── results.txt            # (generated) output data
└── Readme
```

---

## Notes

- All communication is over plain TCP sockets.
- Strings are UTF-8 encoded and newline-delimited.
- The server responds with either a float (coefficient) or a message if a rule blocks the string.
- The client logs all results.