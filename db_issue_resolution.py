import sqlite3

# ----------------------------
# Step 1: Create DB & Table
# ----------------------------
conn = sqlite3.connect("support_lab.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT
)
""")

# Insert records (some are broken: missing email, duplicate username)
users = [
    (1, "alice", "alice@example.com"),
    (2, "bob", None),  # Issue: missing email
    (3, "charlie", "charlie@example.com"),
    (4, "bob", "duplicate@example.com")  # Issue: duplicate username
]
cursor.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", users)
conn.commit()

print("\nInitial Records:")
for row in cursor.execute("SELECT * FROM users"):
    print(row)

# ----------------------------
# Step 2: Identify Issues
# ----------------------------
print("\nDetecting issues...")
missing_emails = cursor.execute("SELECT * FROM users WHERE email IS NULL").fetchall()
duplicates = cursor.execute("""
SELECT username, COUNT(*) as count FROM users
GROUP BY username HAVING count > 1
""").fetchall()

print("Users with missing emails:", missing_emails)
print("Duplicate usernames:", duplicates)

# ----------------------------
# Step 3: Fix Issues
# ----------------------------
print("\n⚙️ Applying fixes...")

# Fix missing email (assign default)
cursor.execute("UPDATE users SET email='noemail@fix.com' WHERE email IS NULL")

# Fix duplicate usernames by renaming the second occurrence of the nce

cursor.execute("UPDATE users SET username='bob_2' WHERE id=4")

conn.commit()

# ----------------------------
# Step 4: Validate Fixes
# ----------------------------
print("\nFinal Records After Fixes:")
for row in cursor.execute("SELECT * FROM users"):
    print(row)

# Log the fix in a simple text file
with open("fix_log.txt", "w") as log:
    log.write("Fixed missing email for user_id=2\n")
    log.write("Renamed duplicate username for user_id=4\n")

print("\nFixes documented in fix_log.txt")

conn.close()
