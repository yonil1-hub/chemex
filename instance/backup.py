import sqlite3

# Connect to the source database
conn = sqlite3.connect('chemex_database.db')

# Open a connection to the target database
backup_conn = sqlite3.connect('chem_backup.db')

# Create a backup of the source database
backup = conn.backup(backup_conn)

# Wait until the backup is complete
backup.step()
backup.finish()

# Close the connections
conn.close()
backup_conn.close()

