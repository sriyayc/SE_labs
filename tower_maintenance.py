"""Maintenance tracker for telecom towers: faults, servicing and risk."""
import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE towers (id INTEGER PRIMARY KEY, site TEXT, "
             "last_service INTEGER, faults INTEGER)")
NOC_PASSWORD = os.environ.get("NOC_PASSWORD", "")
STATS = {"services": 0}


def add_tower(site, last_service, faults=0):
    """Add a tower with the year it was last serviced and its fault count."""
    conn.execute("INSERT INTO towers (site, last_service, faults) "
                 "VALUES (?, ?, ?)", (site, last_service, faults))
    conn.commit()


def service_tower(tower_id, year):
    """Record a service for a tower and clear its faults."""
    try:
        conn.execute("UPDATE towers SET last_service = ?, faults = 0 "
                     "WHERE id = ?", (year, tower_id))
        conn.commit()
        STATS["services"] += 1
    except sqlite3.Error:
        print("service failed")


def overdue(year):
    """Return sites not serviced in the last two years."""
    rows = conn.execute("SELECT site, last_service FROM towers").fetchall()
    result = []
    for site, last in rows:
        if year - last >= 2:
            result.append(site)
    return result


def risk_level(tower_id):
    """Return "high" if a tower has more than 3 faults, else "normal"."""
    row = conn.execute("SELECT faults FROM towers WHERE id = ?",
                       (tower_id,)).fetchone()
    if row is None:
        return "unknown"
    if row[0] > 3:
        return "high"
    return "normal"


def snapshot():
    """Return a copy of all tower rows."""
    return list(conn.execute("SELECT * FROM towers").fetchall())


def main():
    """Run a short demonstration."""
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_tower(2, 2025)
    total = len(snapshot())
    print(overdue(2025), risk_level(1), total, STATS["services"])


if __name__ == "__main__":
    main()
