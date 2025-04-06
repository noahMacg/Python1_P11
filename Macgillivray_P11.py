# MacGillivray_P11
# # Programmer: Noah MacGillivray
# EMail: nmacgillivray@cnm.edu
# Purpose: Extends from P10 and practices GUI
# This program creates a list of geo points from file read in, asks the user
# for a location and finds the closest location from the data read in.

from GeoPoint import GeoPoint
import wx
import textwrap

user_continue = True  # Condition to continue program loop


# Imported list header
def list_header(results_area):

    header_text = "The following are the locations for comparison and their associated coordinates:\n\n"
    results_area.AppendText(header_text)
    results_area.AppendText(f"{'Latitude':<14} {'Longitude':<14} {'Location':<14}\n")
    results_area.AppendText(f"{'-'*54}\n")


# Calculates the closest distance from user input and imported list
def calc_closest_distance(user_input, other_points):

    closest_distance = float("inf")
    closest_point = None

    for i in other_points:
        distance = GeoPoint.calc_distance(user_input.point, i.point)

        if distance < closest_distance:
            closest_distance = distance
            closest_point = i.description

    return (closest_distance, closest_point)


def on_submit(event, file_input, lat_input, long_input, desc_input, results_area):
    try:
        # Get data drom the text box
        file_path = file_input.GetValue()
        # Get GPS coords and locations name variables from text boxes
        user_lat = float(lat_input.GetValue())
        user_long = float(long_input.GetValue())
        user_location_name = desc_input.GetValue()

        # List to hold the imported geo points
        geo_points = []

        # Import data
        with open(file_path, "r") as f:
            for line in f:
                data = line.strip().split(",")
                lat = float(data[0])
                long = float(data[1])
                description = data[2]
                obj = GeoPoint(lat, long, description)
                geo_points.append(obj)
            f.close()

        # Create user point
        user_input = GeoPoint(user_lat, user_long, user_location_name)

        # Calculate closest
        closest_point = calc_closest_distance(user_input, geo_points)

        # Print header to GUI
        list_header(results_area)

        # Print imported to GUI
        for point in geo_points:
            results_area.AppendText(str(point) + "\n\n")

        # Print closest_point to GUI
        closest_dist = closest_point[0]
        closest_desc = closest_point[1]

        results_text = f"You are closest to {closest_desc} with a distance of {closest_dist: .2f} km\n\n"
        results_area.AppendText(results_text)

        results_area.AppendText("If you would like to calculate another press 'Reset'")

    except Exception as e:
        print("Something went wrong: ", e)


def on_reset(event, file_input, lat_input, lon_input, desc_input, results_area):

    # Clear all input fields
    file_input.Clear()
    lat_input.Clear()
    lon_input.Clear()
    desc_input.Clear()

    # Clear results area
    results_area.Clear()

    # Optional: Display a welcome message
    results_area.AppendText("Program reset. Please enter new data and submit.\n\n")

    # Set focus to the first input field
    file_input.SetFocus()


def main():

    app = wx.App()

    # Create the main window
    frame = wx.Frame(None, title="P11_Find Closest Poin", size=(600, 800))
    panel = wx.Panel(frame)

    # Create StaticText labels
    file_label = wx.StaticText(panel, label="File Path:", pos=(10, 20))
    lat_label = wx.StaticText(panel, label="Latitude:", pos=(10, 60))
    long_label = wx.StaticText(panel, label="Longitude:", pos=(10, 100))
    desc_label = wx.StaticText(panel, label="Description:", pos=(10, 140))
    results_label = wx.StaticText(panel, label="Log:", pos=(10, 220))

    # Create TextCtrl fields for user input
    file_input = wx.TextCtrl(panel, pos=(120, 20), size=(250, 25))
    lat_input = wx.TextCtrl(panel, pos=(120, 60), size=(250, 25))
    long_input = wx.TextCtrl(panel, pos=(120, 100), size=(250, 25))
    desc_input = wx.TextCtrl(panel, pos=(120, 140), size=(250, 25))

    # Create results field
    results_area = wx.TextCtrl(
        panel,
        pos=(10, 250),
        size=(560, 500),
        style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
    )

    # Create a submit button
    submit_button = wx.Button(panel, label="Submit", pos=(150, 180))

    # Creat a clear button
    reset_button = wx.Button(panel, label="Reset", pos=(240, 180), size=(100, 30))

    # Bind the button click event to the on_submit function
    submit_button.Bind(
        wx.EVT_BUTTON,
        lambda event: on_submit(
            event, file_input, lat_input, long_input, desc_input, results_area
        ),
    )
    # Bind the button click event to the rest function
    reset_button.Bind(
        wx.EVT_BUTTON,
        lambda event: on_reset(
            event, file_input, lat_input, long_input, desc_input, results_area
        ),
    )

    prog_desc = (
        "This program finds the distance between a list of predetermined locations"
        " read in from a file and the location you provide. It then calculates which location"
        " you are closer to. Please provide the information specified above and press submit.\n\n"
    )
    results_area.AppendText(prog_desc)

    frame.Centre()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
