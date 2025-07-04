import xmlrpc.client

# === Odoo credentials ===
url = "https://prashanti-sarees.odoo.com/"
db = "ganeshvana-prasanthilive-main-15204134"
username = "admin@test.com"
password = "admin@123"

# === Connect ===
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

if not uid:
    print("❌ Authentication failed")
    exit()
print("✅ Connected to Odoo")

# === Step 1: Find all orders with 'REFUNDED' in note ===
refunded_order_ids = models.execute_kw(db, uid, password, 'pos.order', 'search', [[['note', 'ilike', 'REFUNDED']]])
if not refunded_order_ids:
    print("🎉 No refunded orders found.")
    exit()

print(f"🔍 Found {len(refunded_order_ids)} order(s) marked as REFUNDED.")

# === Step 2: Read notes and clean them ===
orders = models.execute_kw(db, uid, password, 'pos.order', 'read', [refunded_order_ids], {'fields': ['id', 'name', 'note']})

for order in orders:
    old_note = order.get('note') or ''
    print(f"\n🧾 Order: {order['name']}")
    print(f"📝 Old Note:\n{old_note}")
    
    # Remove all lines that mention 'REFUNDED'
    cleaned_lines = [line for line in old_note.split('\n') if 'REFUNDED' not in line.upper()]
    cleaned_note = '\n'.join(cleaned_lines).strip()

    if cleaned_note != old_note:
        models.execute_kw(db, uid, password, 'pos.order', 'write', [[order['id']], {'note': cleaned_note}])
        print("✅ Note cleaned.")
    else:
        print("ℹ️ Nothing to clean.")

print("\n🎯 All eligible orders restored. You can now rerun the refund script.")
