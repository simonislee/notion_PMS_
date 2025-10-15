import pandas as pd
from notion_client import Client

from system_variables.system_variables import get_notion_api, get_database_lease


def get_lease():
    # Initialize Notion client with your API key
    notion = Client(auth=get_notion_api())  # Replace with your actual API key

    # Database ID
    database_id = get_database_lease()

    def get_page_title(page_id):
        """Helper function to fetch the title of a related page."""
        try:
            page = notion.pages.retrieve(page_id=page_id)
            # Assume the title is in the first title property
            for prop_name, prop_value in page["properties"].items():
                if prop_value["type"] == "title" and prop_value["title"]:
                    return prop_value["title"][0]["plain_text"]
            return page_id  # Fallback to page ID if no title is found
        except Exception as e:
            return page_id  # Fallback to page ID if error occurs

    try:
        # Query the database
        response = notion.databases.query(database_id=database_id)

        # Extract the results (rows of the database)
        results = response["results"]

        # Prepare a list to store the table data
        table_data = []

        # Iterate through each page (row) in the database
        for page in results:
            properties = page["properties"]
            row = {"Page ID": page["id"]}
            # Add page ID to the row
            # Extract each property value
            for prop_name, prop_value in properties.items():
                prop_type = prop_value["type"]
                if prop_type == "title":
                    row[prop_name] = prop_value["title"][0]["plain_text"] if prop_value["title"] else ""
                elif prop_type == "rich_text":
                    row[prop_name] = prop_value["rich_text"][0]["plain_text"] if prop_value["rich_text"] else ""
                elif prop_type == "number":
                    row[prop_name] = prop_value["number"] if prop_value["number"] is not None else ""
                elif prop_type == "select":
                    row[prop_name] = prop_value["select"]["name"] if prop_value["select"] else ""
                elif prop_type == "multi_select":
                    row[prop_name] = ", ".join([option["name"] for option in prop_value["multi_select"]]) if prop_value[
                        "multi_select"] else ""
                elif prop_type == "date":
                    row[prop_name] = prop_value["date"]["start"] if prop_value["date"] else ""
                elif prop_type == "checkbox":
                    row[prop_name] = prop_value["checkbox"]
                elif prop_type == "relation":
                    # Extract related page IDs and fetch their titles
                    related_pages = prop_value["relation"]
                    if related_pages:
                        titles = [get_page_title(page["id"]) for page in related_pages]
                        row[prop_name] = ", ".join(titles)
                    else:
                        row[prop_name] = ""
                elif prop_type == "formula":
                    # Extract formula result based on its type
                    formula_result = prop_value["formula"]
                    if formula_result["type"] == "string":
                        row[prop_name] = formula_result["string"] if formula_result["string"] is not None else ""
                    elif formula_result["type"] == "number":
                        row[prop_name] = formula_result["number"] if formula_result["number"] is not None else ""
                    elif formula_result["type"] == "boolean":
                        row[prop_name] = formula_result["boolean"]
                    elif formula_result["type"] == "date":
                        row[prop_name] = formula_result["date"]["start"] if formula_result["date"] else ""
                    else:
                        row[prop_name] = ""  # Fallback for unsupported formula types
                # Add more property types as needed
            table_data.append(row)

        # Convert to a pandas DataFrame for a table-like structure
        df = pd.DataFrame(table_data)
        active_lease = df.loc[df['Status'] == 'Active']
        print(active_lease)
        return active_lease

    except Exception as e:
        print(f"An error occurred: {e}")
    pass


def lease_change_next_payment_date(page_id: str, next_payment_date: str):
    # Initialize Notion client with your API key
    notion = Client(auth=get_notion_api())  # Replace with your
    try:
        # Prepare the property update
        properties = {
            "Next Payment Date": {
                "date": {"start": next_payment_date.strip()}
                if isinstance(next_payment_date,
                              str) and next_payment_date.strip() else None
            }
        }

        # Update the page
        response = notion.pages.update(
            page_id=page_id,
            properties=properties
        )
        print(f"Updated Payment Date for Page ID: {response['id']}")

    except Exception as e:
        print(f"An error occurred: {e}")
    pass


if __name__ == '__main__':
    # next_payment = datetime.today().strftime("%Y-%m-%d")
    # print(next_payment)
    # lease_change_next_payment_date(page_id='287151d118e78079be36fac0cc133ffc', next_payment_date=next_payment)
    get_lease()
    pass
