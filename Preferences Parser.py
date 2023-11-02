import json
import tkinter as tk
from tkinter import filedialog, messagebox
import csv


ascii_art = '''
Q29weXJpZ2h0IChjKSBTdG9maWs=
╔═╗┬─┐┌─┐┌─┐┌─┐┬─┐┌─┐┌┐┌┌─┐┌─┐┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┬─┐
╠═╝├┬┘├┤ ├┤ ├┤ ├┬┘├┤ ││││  ├┤ └─┐  ╠═╝├─┤├┬┘└─┐├┤ ├┬┘
╩  ┴└─└─┘└  └─┘┴└─└─┘┘└┘└─┘└─┘└─┘  ╩  ┴ ┴┴└─└─┘└─┘┴└─
Preferences Parser V0.0.3
https://github.com/MDCDF

'''


def open_json_file():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        display_data()

    except FileNotFoundError:
        result_label.config(text="File not found")
    except json.JSONDecodeError:
        result_label.config(text="Invalid JSON file")

def display_data():
    account_info = data.get("account_info", [{}])[0]
    clear_data = data.get("browser", {}).get("clear_data", {})
    store_file_paths = data.get("optimization_guide", {}).get("store_file_paths_to_delete", {})
    download_data = data.get("download", {})
    profile_data = data.get("profile", {})

    # Clear previous data in the text widget
    text.delete(1.0, tk.END)

    # Create a bigger, bold, and blue font
    text.tag_configure("topic", font=("Arial", 14, "bold"), foreground="blue")
    
    # Display 'Account Info:'
    text.insert(tk.END, "Account Info:\n", "topic")
    for key, value in account_info.items():
        if key not in ["account_id", "gaia", "accountcapabilities"]:
            text.insert(tk.END, f"{key}: {value}\n")

    # Create a space between categories
    text.insert(tk.END, "\n")

    # Display 'Clear Data:'
    text.insert(tk.END, "Clear Data:\n", "topic")
    for key, value in clear_data.items():
        if key in ["cache", "cache_basic", "cookies", "cookies_basic", "form_data", "hosted_apps_data", "passwords", "site_settings", "time_period"]:
            text.insert(tk.END, f"{key}: {value}\n")
        else:
            text.insert(tk.END, f"{key}: {value}\n")

    # Create a space between categories
    text.insert(tk.END, "\n")

    # Display 'Store File Paths to Delete:'
    text.insert(tk.END, "Store File Paths to Delete:\n", "topic")
    for key, value in store_file_paths.items():
        text.insert(tk.END, f"{key}: {value}\n")

    # Create a space between categories
    text.insert(tk.END, "\n")

    # Display 'Download Data:'
    text.insert(tk.END, "Download Data:\n", "topic")
    text.insert(tk.END, f"Default Directory: {download_data.get('default_directory', 'N/A')}\n")

    # Create a space between categories
    text.insert(tk.END, "\n")

    # Display 'Profile Data:'
    text.insert(tk.END, "Profile Data:\n", "topic")
    for website, website_data in profile_data.get("content_settings", {}).get("exceptions", {}).items():
        if not website_data:
            continue
        text.insert(tk.END, f"Website: {website}\n")
        for site_key, _ in website_data.items():
            text.insert(tk.END, f"  Site Key: {site_key}\n")

def export_to_csv():
    if 'data' not in globals():
        result_label.config(text="No data to export.")
        return

    csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not csv_file_path:
        return

    account_info = data.get("account_info", [{}])[0]
    clear_data = data.get("browser", {}).get("clear_data", {})
    store_file_paths = data.get("optimization_guide", {}).get("store_file_paths_to_delete", {})
    download_data = data.get("download", {})
    profile_data = data.get("profile", {})

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Section", "Key", "Value"])

        for key, value in account_info.items():
            if key not in ["account_id", "gaia", "accountcapabilities"]:
                csv_writer.writerow(["Account Info", key, value])

        for key, value in clear_data.items():
            if key in ["Cache", "cache_basic", "cookies", "cookies_basic", "form_data", "hosted_apps_data", "passwords", "site_settings", "time_period"]:
                csv_writer.writerow(["Clear Data", key, value])
            else:
                csv_writer.writerow(["Clear Data", key, value])

        for key, value in store_file_paths.items():
            csv_writer.writerow(["Store File Paths to Delete", key, value])

        # Export Download Data
        csv_writer.writerow(["Download Data", "Default Directory", download_data.get('default_directory', 'N/A')])

        # Export Profile Data
        csv_writer.writerow(["Profile Data", "Website", "Site Key"])
        for website, website_data in profile_data.get("content_settings", {}).get("exceptions", {}).items():
            if not website_data:
                continue
            for site_key, _ in website_data.items():
                csv_writer.writerow(["Profile Data", website, site_key])

    result_label.config(text="Data exported to CSV.")

def show_help():
    messagebox.showinfo("Help", "test")

# Create a GUI window with a default size
window = tk.Tk()
window.title("JSON Parser")
window.geometry("800x600")  # Set the default size

# Create and pack a frame for the parsed data
data_frame = tk.Frame(window)
data_frame.pack(fill="both", expand=True)

# Create a Text widget for displaying parsed data with a vertical scrollbar
text = tk.Text(data_frame, wrap=tk.WORD)
text.pack(side="left", fill="both", expand=True)

# Create a scrollbar and link it to the Text widget
scrollbar = tk.Scrollbar(data_frame, command=text.yview)
scrollbar.pack(side="right", fill="y")
text.config(yscrollcommand=scrollbar.set)

# Create and pack a "Browse JSON File" button
browse_button = tk.Button(window, text="Browse JSON File", command=open_json_file)
browse_button.pack()

# Create and pack an "Export to CSV" button
export_button = tk.Button(window, text="Export to CSV", command=export_to_csv)
export_button.pack()

# Create and pack a "Help" button
help_button = tk.Button(window, text="Help", command=show_help)
help_button.pack()

# Create and pack a label to display results or errors
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()


