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

# === Step 1: Ask user to enter pos_reference of the refund order ===
pos_ref = "Order 03000-001-0002"

# === Step 2: Find the refunded order by pos_reference ===
refunded_ids = models.execute_kw(db, uid, password, 'pos.order', 'search', [[['pos_reference', '=', pos_ref]]])
if not refunded_ids:
    print("❌ No refund order found with this pos_reference.")
    exit()

refunded_orders = models.execute_kw(db, uid, password, 'pos.order', 'read', [refunded_ids], {'fields': ['id', 'name', 'pos_reference']})
refunded_order = refunded_orders[0]
refunded_name = refunded_order['name']

print(f"\n🧾 Refunded Order: {refunded_name}")

# === Step 3: Derive original order name ===
if not refunded_name.endswith("REFUND"):
    print("⚠️ This doesn't appear to be a refund order (missing 'REFUND' in name). Exiting.")
    exit()

original_name = refunded_name.replace(" REFUND", "").strip()

# === Step 4: Find the original order by name ===
original_ids = models.execute_kw(db, uid, password, 'pos.order', 'search', [[['name', '=', original_name]]])
if not original_ids:
    print(f"❌ Could not find original order with name '{original_name}'")
    exit()

# === Step 5: Read the note of the original order ===
original_orders = models.execute_kw(db, uid, password, 'pos.order', 'read', [original_ids], {'fields': ['id', 'name', 'note']})

for order in original_orders:
    old_note = order.get('note') or ''
    print(f"\n🧾 Original Order: {order['name']}")
    print(f"📝 Old Note:\n{old_note}")

    # Remove 'REFUNDED' lines
    cleaned_lines = [line for line in old_note.split('\n') if 'REFUNDED' not in line.upper()]
    cleaned_note = '\n'.join(cleaned_lines).strip()

    if cleaned_note != old_note:
        models.execute_kw(db, uid, password, 'pos.order', 'write', [[order['id']], {'note': cleaned_note}])
        print("✅ Note cleaned.")
    else:
        print("ℹ️ No 'REFUNDED' text found. Nothing to clean.")

print("\n🎯 Done. The original order's note is now clean and reusable.")