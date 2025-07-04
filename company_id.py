import xmlrpc.client

# Odoo credentials
url = "https://prashanti-sarees-stage-120625-21457163.dev.odoo.com"
db = "prashanti-sarees-stage-120625-21457163"
username = "ashikibrahimshah@wedtree.com"
password = "Ashik@123"

# Connect
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

if not uid:
    print("❌ Failed to authenticate.")
    exit()

# Search all payment methods
payment_method_ids = models.execute_kw(db, uid, password, 'pos.payment.method', 'search', [[]])
payment_methods = models.execute_kw(db, uid, password, 'pos.payment.method', 'read', [payment_method_ids], {
    'fields': ['id', 'name', 'company_id']
})

print("🧾 POS Payment Methods and Their Companies:\n")
for pm in payment_methods:
    company = pm['company_id'][1] if pm['company_id'] else "❌ Not Assigned"
    company_id = pm['company_id'][0] if pm['company_id'] else "N/A"
    print(f"🆔 ID: {pm['id']:<4} | Name: {pm['name']:<20} | Company: {company:<50} | Company ID: {company_id}")
