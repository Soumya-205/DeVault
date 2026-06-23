# DeVault

A distributed key-value store built from scratch in Python.

DeVault is a learning project aimed at understanding how distributed databases work under the hood — covering multi-node architecture, consistent hashing, replication, and fault tolerance.

---

## What it does

- Stores and retrieves key-value pairs over a network using raw sockets
- Routes keys across multiple nodes using consistent hashing
- Replicates data across nodes to prevent data loss on failure
- Detects node crashes and recovers automatically

> Currently in active development. New features added daily.

---

## Tech Stack

- Python
- Sockets (TCP)
- Threading

---

## Project Status

| Feature | Status |
|---|---|
| Single node KV store | ✅ Done |
| Multi-node routing | 🔨 In Progress |
| Consistent hashing | 🔨 In Progress |
| Replication | ⏳ Upcoming |
| Fault tolerance | ⏳ Upcoming |

---

## How to Run

```bash
# Start the server
python node/server.py

# In a separate terminal, run the client
python client/client.py
```

---

## Learning Reference

Built while studying distributed systems concepts from MIT 6.824 and Designing Data-Intensive Applications (DDIA).# DeVault
