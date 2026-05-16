import os
import glob

# Delete 0007 migration files
migrations_to_delete = glob.glob('apps/assessments/migrations/0007*.py')
for m in migrations_to_delete:
    try:
        os.remove(m)
        print(f"Deleted: {m}")
    except Exception as e:
        print(f"Failed to delete {m}: {e}")

# Clear pycache
import shutil
for root, dirs, files in os.walk('apps'):
    if '__pycache__' in dirs:
        try:
            shutil.rmtree(os.path.join(root, '__pycache__'))
        except:
            pass

print("Done")
