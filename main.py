"""CLI Todo Manager - A simple command-line task tracker."""
import sqlite3
import argparse


DB_FILE = "todos.db"


def init_db(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS todos "
        "(id INTEGER PRIMARY KEY, task TEXT, done INTEGER DEFAULT 0)"
    )
    conn.commit()


def add_task(conn, task: str):
    conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    print(f"Added: {task}")


def list_tasks(conn):
    rows = conn.execute("SELECT id, task, done FROM todos").fetchall()
    for row in rows:
        status = "✓" if row[2] else "○"
        print(f"[{status}] {row[0]}. {row[1]}")


def main():
    parser = argparse.ArgumentParser(description="CLI Todo Manager")
    sub = parser.add_subparsers(dest="cmd")
    add_p = sub.add_parser("add")
    add_p.add_argument("task")
    sub.add_parser("list")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_FILE)
    init_db(conn)
    if args.cmd == "add":
        add_task(conn, args.task)
    elif args.cmd == "list":
        list_tasks(conn)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
