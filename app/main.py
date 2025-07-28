import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json
import os
from app.invoice_generator import generate_invoice
from app.email_sender import send_email


def main():
    def select_file():
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if path:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, path)

    def generate():
        try:
            with open("config.json") as f:
                config = json.load(f)

            df = pd.read_excel(entry_file.get())

            # Normalize column names (strip spaces)
            df.columns = df.columns.str.strip()

            os.makedirs("invoices", exist_ok=True)

            # Group by Invoice Number
            for invoice_number, group in df.groupby("Invoice Number"):
                first_row = group.iloc[0]

                items = []
                for _, row in group.iterrows():
                    items.append({
                        "product_name": row["Product Name"],
                        "sku": row["SKU"],
                        "description": row["Description"],
                        "quantity": row["Quantity"],
                        "unit_price": row["Unit Price"],
                        "discount": row["Discount (%)"],
                        "tax_rate": row["Tax Rate (%)"],
                        "total_line_amount": row["Total Line Amount"]
                    })

                data = {
                    "invoice_number": invoice_number,
                    "invoice_date": str(first_row["Invoice Date"]),
                    "due_date": str(first_row["Due Date"]),
                    "order_id": first_row["Order ID"],
                    "client_name": first_row["Customer Name"],
                    "client_email": first_row["Customer Email"],
                    "billing_address": first_row["Billing Address"],
                    "shipping_address": first_row["Shipping Address"],
                    "phone": first_row["Phone Number"],
                    "payment_method": first_row["Payment Method"],
                    "salesperson": first_row["Salesperson"],
                    "job": first_row["Job"],
                    "currency": first_row["Currency"],
                    "items": items,
                    "subtotal": group["Line Subtotal"].sum(),
                    "total_tax": group["Tax Amount"].sum(),
                    "total_shipping": group["Shipping Cost"].sum(),
                    "total_amount": group["Total Line Amount"].sum()
                }


                pdf_path = generate_invoice(data, config)

                if config.get("email_sending"):
                    send_email(
                        to_email=data["client_email"],
                        subject=f"Invoice {data['invoice_number']}",
                        body="Please find your invoice attached.",
                        attachment_path=pdf_path,
                        smtp_settings=config["smtp_settings"]
                    )

            messagebox.showinfo("Success", "Invoices generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    # GUI Setup
    root = tk.Tk()
    root.title("Invoice Generator")

    tk.Label(root, text="Select Excel File").pack(pady=5)
    entry_file = tk.Entry(root, width=50)
    entry_file.pack(pady=5)
    tk.Button(root, text="Browse", command=select_file).pack(pady=5)
    tk.Button(root, text="Generate Invoices", command=generate).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
