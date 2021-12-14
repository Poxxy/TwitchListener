import os

print("Running backup...")

os.system("pg_dump yourdb > your/backup/location/yourdbbck")

print("Backup finished.")
