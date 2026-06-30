# DeVault

A distributed key-value store built from scratch in Python.

DeVault is a systems project aimed at understanding how distributed databases work under the hood — covering multi-node architecture, consistent hashing, replication, and fault tolerance.

---

## Demo

```
Client                    Server
  |                          |
  |----  SET name Alex  ---→ |
  |                          | store["name"] = "Alex"
  | ←-------------- Ok ----- |
  |                          |
  |----  GET name ----------→|
  |                          | store["name"] → "Alex"
  | ←----------- Alex ------ |
  |                          |
  |----  DELETE name ------→ |
  |                          | del store["name"]
  | ←--------- DELETED ----- |
  |                          |
  |----  EXISTS name ------→ |
  |                          | "name" not in store
  | ←-------------- No ----- |
```

---

## What it does

- Stores and retrieves key-value pairs over a network using raw sockets
- Interactive CLI — type commands directly in the terminal
- Handles multiple clients simultaneously using threads
- Routes keys across multiple nodes using consistent hashing
- Replicates data across nodes to prevent data loss on failure
- Detects node crashes and recovers automatically

> Currently in active development. New features pushed daily.

---

## Tech Stack

- Python
- Sockets (TCP)
- Threading

---

## How to Run

```bash
# Start the server
python node/server.py

# In a separate terminal, start the client
python client/client.py
```

## Supported Commands

| Command | Description | Example |
|---|---|---|
| SET key value | Store a value | SET name Alex |
| GET key | Retrieve a value | GET name |
| DELETE key | Remove a key | DELETE name |
| EXISTS key | Check if key exists | EXISTS name |
| EXIT | Close the client | EXIT |

---

## Project Status

| Feature | Status |
|---|---|
| Single node KV store | ✅ Done |
| Interactive CLI client | ✅ Done |
| Persistent connection | ✅ Done |
| Data persistence | ✅ Done |
| KEYS command + validation | ✅ Done |
| Multi-node routing | ✅ Done |
| Consistent hashing | ✅ Done |
| Three-node cluster | ✅ Done |
| Replication | ⏳ Upcoming |
| Fault tolerance | ⏳ Upcoming |
