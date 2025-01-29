import frappe

@frappe.whitelist()
def ping():
    return 'pong'

# def get_customer(allow_guest=True):
#     customers=frappe.get_all('customer',fields=["name","customer_name"])
#     return customers

@frappe.whitelist()
def get_customer_details():
    return frappe.db.sql(f"""SELECT name,customer_name FROM `tabCustomer`WHERE  name="Palmer Productions Ltd.";""",as_dict=True)




@frappe.whitelist()
def get_sales_invoices_for_customer(customer_name):
         query = """
            SELECT 
                si.name AS invoice_name, 
                si.customer, 
                si.posting_date,
                si.grand_total
            FROM 
                `tabSales Invoice` si
            WHERE 
                si.customer = (SELECT name FROM `tabCustomer` WHERE customer_name = %s)
                AND si.docstatus = 1  -- Only submitted invoices
            ORDER BY 
                si.posting_date DESC
        """
         sales_invoices = frappe.db.sql(query, (customer_name,), as_dict=True)
        
         return {
            "status": "success",
            "customer_name": customer_name,
            "data": sales_invoices
        }

# For fix Customer
@frappe.whitelist()
def sales_and_customer(customer_name="Grant Plastics Ltd."):
    customer_query="""
                    SELECT name as customer_id,
                    customer_name,
                    customer_type
                    FROM `tabCustomer`
                    WHERE customer_name=%s
                    LIMIT 1"""
    customer_data=frappe.db.sql(customer_query,(customer_name),as_dict=True)
    if not customer_data:
            return {"status": "error", "message": f"Customer '{customer_name}' not found."}
    customer_data=customer_data[0]
        
    # Fetching Sales Invoices for above  Customer
    
    slaes_invoice_query="""
                        SELECT 
                        name as invoice_name,
                        customer,
                        posting_date,
                        grand_total
                        FROM `tabSales Invoice`
                        WHERE customer=%s
    
    """
    sales_invoices=frappe.db.sql(slaes_invoice_query,(customer_data["customer_id"],),as_dict=True)
    
    return customer_data,sales_invoices
    
# For dynamic Customer
@frappe.whitelist()
def sales_and_customer(customer_name):
    customer_query="""
                    SELECT name as customer_id,
                    customer_name,
                    customer_type
                    FROM `tabCustomer`
                    WHERE customer_name=%s
                    LIMIT 1"""
    customer_data=frappe.db.sql(customer_query,(customer_name),as_dict=True)
    if not customer_data:
            return {"status": "error", "message": f"Customer '{customer_name}' not found."}
    customer_data=customer_data[0]
        
    # Fetching Sales Invoices for above  Customer
    
    slaes_invoice_query="""
                        SELECT 
                        name as invoice_name,
                        customer,
                        posting_date,
                        grand_total,
                        due_date
                        FROM `tabSales Invoice`
                        WHERE customer=%s
    
    """
    sales_invoices=frappe.db.sql(slaes_invoice_query,(customer_data["customer_id"],),as_dict=True)
    
    return customer_data,sales_invoices