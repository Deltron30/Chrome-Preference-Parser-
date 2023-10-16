import tkinter as tk
from tkinter import filedialog
import json

# Function to extract and print "gaia_cookie" and "clear_data" sections
def extract_and_print_sections(parsed_data):
    clear_data = parsed_data.get("browser", {}).get("clear_data", {})
    gaia_cookie = parsed_data.get("gaia_cookie", {})

    print("Clear Data Section:")
    print(" - Cookies Basic:", clear_data.get("cookies_basic"))
    print(" - Download History:", clear_data.get("download_history"))
    print(" - Hosted Apps Data:", clear_data.get("hosted_apps_data"))
    print(" - Time Period:", clear_data.get("time_period"))

    print("\nGaia Cookie Section:")
    print(" - Changed Time:", gaia_cookie.get("changed_time"))
    print(" - Hash:", gaia_cookie.get("hash"))
    print(" - Last List Accounts Data:", gaia_cookie.get("last_list_accounts_data"))

# Create a simple GUI window
root = tk.Tk()
root.withdraw()  # Hide the main window

while True:
    # Prompt the user to select a file
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])

    if not file_path:
        print("No file selected. Exiting...")
        break

    try:
        # Try to determine the file format based on content
        with open(file_path, 'rb') as file:
            file_content = file.read()
            if file_content.strip().startswith(b'{'):
                # The file content starts with '{', suggesting it's JSON data
                data = json.loads(file_content)
                print("JSON data successfully parsed:")
                extract_and_print_sections(data)
            else:
                print("The file doesn't appear to be in JSON format.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {str(e)}")
        print("Failed to parse JSON data from the selected file.")

    # Ask if the user wants to upload a new file
    user_choice = input("Do you want to upload another file? (y/n): ").strip().lower()
    if user_choice != 'y':
        break

# Close the GUI window
root.destroy()

