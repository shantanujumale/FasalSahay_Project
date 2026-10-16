import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from app.database import SessionLocal
from app.models import User, Claim
from app.schemas import UserOut, ClaimOut

db = SessionLocal()
print("=== USERS IN DATABASE ===")
for u in db.query(User).all():
    print(f"ID={u.id} | Email={u.email} | Role={u.role} | Phone={u.phone!r} | Aadhaar={u.aadhaar_last4!r} | BankAcc={u.bank_account_last4!r} | BankIFSC={u.bank_ifsc!r}")
    try:
        uo = UserOut.model_validate(u)
        print("  -> UserOut valid:", uo.email, uo.role)
    except Exception as e:
        print("  -> UserOut VALIDATION ERROR:", type(e), e)

print("\n=== CLAIMS IN DATABASE ===")
for c in db.query(Claim).all():
    print(f"ID={c.id} | Ref={c.reference} | ExtRef={c.external_reference!r} | Insurer={c.insurer_name!r}")
    try:
        co = ClaimOut.model_validate(c)
        print("  -> ClaimOut valid:", co.reference)
    except Exception as e:
        print("  -> ClaimOut VALIDATION ERROR:", type(e), e)

db.close()
