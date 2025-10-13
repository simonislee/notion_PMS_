from notion_client import Client

from system_variables.system_variables import get_notion_api, get_database_payment


# Example data for new rows (customize based on your database schema)


def add_payment_row(payment: list[dict]):
    # Initialize Notion client with your API key
    notion = Client(auth=get_notion_api())  # Replace with your actual API key

    # New database ID (replace with the actual database ID)
    database_id = get_database_payment()  # Replace with the new database ID
    try:
        for row in payment:
            # Prepare properties for the new page
            properties = {}

            # Map each field to the appropriate Notion property type
            for key, value in row.items():
                if key == "Payment Name":
                    properties[key] = {
                        "title": [{"text": {"content": value}}] if value else []
                    }
                elif key == "lease":
                    properties[key] = {
                        "relation": [{"id": page_id} for page_id in value] if value else []
                    }
                elif key == "Due Date" or key == "Payment Date":
                    # Handle date values (string, empty dict, or empty string)
                    if isinstance(value, str) and value.strip():
                        properties[key] = {"date": {"start": value.strip()}}
                    else:
                        properties[key] = {"date": null}  # Use null for empty dates ({} or "")
                elif key == "Rent Amount" or key == "Utility Fees":
                    properties[key] = {
                        "number": value if value is not None else None
                    }
                elif key == "Status":
                    properties[key] = {
                        "status": {"name": value} if value else None
                    }
                elif key == "Payment Method":
                    properties[key] = {
                        "select": {"name": value} if value else None
                    }
                elif key == "Notes":
                    properties[key] = {
                        "rich_text": [{"text": {"content": value}}] if value else []
                    }

            # Create a new page in the database
            response = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            print(f"Added row with Page ID: {response['id']}")

    except Exception as e:
        print(f"An error occurred: {e}")

    pass


if __name__ == '__main__':
    new_rows = [
        {
            "Payment Name": 'test',  # property-room-month-rent
            "lease": ['287151d118e78079be36fac0cc133ffc'],  # get the lease page id
            'Due Date': '2025-10-11',  # get the next due day from lease database
            'Rent Amount': 0,  # get the rent Amount
            'Status': 'Unpaid',
            'Payment Method': 'Cash',
        }
    ]
    add_payment_row(new_rows)
