import sqlite3
import os

for db_path in ['backend/pmfby_dev.db', 'pmfby_dev.db']:
    if not os.path.exists(db_path):
        continue
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            UPDATE users SET 
                phone = COALESCE(phone, ''),
                aadhaar_last4 = COALESCE(aadhaar_last4, ''),
                bank_account_last4 = COALESCE(bank_account_last4, ''),
                bank_ifsc = COALESCE(bank_ifsc, '')
        """)
        cur.execute("""
            UPDATE claims SET 
                external_reference = COALESCE(external_reference, ''),
                insurer_name = COALESCE(insurer_name, '')
        """)
        conn.commit()
        print(f"Successfully normalized database: {db_path}")
        cur.execute("SELECT id, email, role, phone, aadhaar_last4, bank_account_last4, bank_ifsc FROM users")
        for row in cur.fetchall():
            print("  User:", row)
        conn.close()
    except Exception as e:
        print(f"Error on {db_path}: {e}")
