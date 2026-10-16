import urllib.request
import json

def test_login(base_url, email, password):
    url = f"{base_url}/api/auth/login"
    payload = json.dumps({"email": email, "password": password}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            token = data.get("access_token")
            user = data.get("user")
            print(f"[{resp.status}] {email} -> Logged in as: {user['full_name']} (Role: {user['role']})")
            
            # Now test claims endpoint with this token
            claims_req = urllib.request.Request(
                f"{base_url}/api/claims",
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(claims_req) as c_resp:
                claims_data = json.loads(c_resp.read().decode("utf-8"))
                print(f"       Claims retrieved: {len(claims_data)} claims")
                
            # If officer or admin, test analytics
            if user['role'] in ['officer', 'admin']:
                analytics_req = urllib.request.Request(
                    f"{base_url}/api/analytics/summary",
                    headers={"Authorization": f"Bearer {token}"}
                )
                with urllib.request.urlopen(analytics_req) as a_resp:
                    analytics_data = json.loads(a_resp.read().decode("utf-8"))
                    print(f"       Analytics retrieved: {analytics_data['total_cases']} cases")
                    
            # If admin, test admin system status
            if user['role'] == 'admin':
                admin_req = urllib.request.Request(
                    f"{base_url}/api/admin/system-status",
                    headers={"Authorization": f"Bearer {token}"}
                )
                with urllib.request.urlopen(admin_req) as adm_resp:
                    adm_data = json.loads(adm_resp.read().decode("utf-8"))
                    print(f"       Admin status: env={adm_data.get('environment', 'ok')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[FAILED {e.code}] {email} -> {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"[ERROR] {email} -> {e}")
        return False

print("=== TESTING DIRECT BACKEND (http://127.0.0.1:8000) ===")
test_login("http://127.0.0.1:8000", "farmer@demo.local", "FarmerDemo!234")
test_login("http://127.0.0.1:8000", "officer@demo.local", "OfficerDemo!234")
test_login("http://127.0.0.1:8000", "admin@demo.local", "AdminDemo!234")

print("\n=== TESTING FRONTEND PROXY (http://localhost:5173) ===")
test_login("http://localhost:5173", "farmer@demo.local", "FarmerDemo!234")
test_login("http://localhost:5173", "officer@demo.local", "OfficerDemo!234")
test_login("http://localhost:5173", "admin@demo.local", "AdminDemo!234")
