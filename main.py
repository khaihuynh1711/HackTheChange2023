# Inputs - > Address, Power per year, Roof size, Production ratio, Panel wattage
# Convert Address - > Co-ordinates
# Use Co-ordinates with API to get the
# Number of panels = system size/production ratio/panel wattage
# Outputs - > Number of panels, Solar panel cost
# Solar PV system
# PROGRAM START HERE!!!!!
import math
import pandas
import requests
from geopy.geocoders import Nominatim
'''
# user input
address from input
yearly_power_use from input
cost_of_power = float(input())
roof_size = float(input())
'''
# return pair of latitude and longitude


def get_coords_funct(address):
    geolocator = Nominatim(user_agent="Solar_Panel_Optimization")
    location = geolocator.geocode(address)
    return [location.latitude, location.longitude]
# get data from api server
# return pair of list
def get_radiation_from_API(latitude, longitude) -> list:
    response_winter = requests.get(
        f'https://api.solcast.com.au/data/historic/radiation_and_weather?latitude={latitude}&longitude={longitude}&azimuth=44&tilt=90&start=2022-12-06T14:45:00.000Z&duration=P31D&format=json&time_zone=utc&api_key=PSjUgTPzeIZb2kGk8fsQs7yA_wjgHK9X')
    response_summer = requests.get(
        f'https://api.solcast.com.au/data/historic/radiation_and_weather?latitude={latitude}&longitude={longitude}&azimuth=44&tilt=90&start=2022-06-06T14:45:00.000Z&duration=P31D&format=json&time_zone=utc&api_key=PSjUgTPzeIZb2kGk8fsQs7yA_wjgHK9X')
    # checking api identity: print(response.status_code)
    data_winter = response_winter.json()
    data_summer = response_summer.json()
    dni_data_winter = []
    dni_data_summer = []
    for i in range(len(data_winter['estimated_actuals'])):
        dni_data_winter.append(data_winter['estimated_actuals'][i]['dni'])
        dni_data_summer.append(data_summer['estimated_actuals'][i]['dni'])
    return [dni_data_winter, dni_data_summer]
# return power of the system
def api_funct(roof_size, input_pair, area_of_the_solar_panel):
    tally_one = 0
    total_dni_one = 0
    total_dni_two = 0
    tally_two = 0
    for x in input_pair[0]:
        tally_one += 1
        total_dni_one = total_dni_one + x
    for x in input_pair[1]:
        tally_two += 1
        total_dni_two = total_dni_two + x
    dni_per_year = ((total_dni_one / tally_one) + (total_dni_two / tally_two)) * 6
    power_of_the_panel = area_of_the_solar_panel * dni_per_year * 0.8 * 0.15
    num_of_panel = roof_size / area_of_the_solar_panel
    power_of_the_system = power_of_the_panel * num_of_panel
    return [num_of_panel, power_of_the_system]

def output(address, yearly_power_use, cost_of_power, roof_size):
    print("HI")
    area_of_the_solar_panel = 1.7  # default value for area of the solar panel
    coordinates = get_coords_funct(address)
    dni_data = get_radiation_from_API(coordinates[0], coordinates[1])
    solar_result = api_funct(
        roof_size, [dni_data[0], dni_data[1]], area_of_the_solar_panel)
    total_cost = 413 * roof_size
    time = total_cost/(cost_of_power*solar_result[1])
    excess_money_per_year = (solar_result[1] - yearly_power_use) * cost_of_power
    return [str(coordinates[0])+" "+str(coordinates[1]), str(math.ceil(solar_result[0])), str(solar_result[1]), f'{total_cost:.2f}', f'{time:.2f}', f'{excess_money_per_year:.2f}']







import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
final_info = []

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1400}x{580}")

        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SOLAR SENSE YYC", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="About us", command=self.about_us_button)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Application", command=self.application_button)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.exit_program, fg_color="#8B0000")
        self.exit_button.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))




        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")




    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def application_button(self):
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Reset",
                                                        command=self.application_button)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=(10,0))
        self.slider_progressbar_frame = customtkinter.CTkFrame(self)
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)

        self.address_label = customtkinter.CTkLabel(master=self.slider_progressbar_frame,
                                                    text="Enter your address below:", anchor="w")
        self.address_label.grid(row=0, column=0, columnspan=1, sticky="")

        self.address_entry = customtkinter.CTkEntry(self.slider_progressbar_frame,
                                                    placeholder_text="Street-number\tstreet-name\tcity")
        self.address_entry.grid(row=1, column=0, padx=(20, 10), sticky="ew")

        self.power_label = customtkinter.CTkLabel(master=self.slider_progressbar_frame,
                                                  text="Enter yearly power consumption in Kwh:", anchor="w")
        self.power_label.grid(row=2, column=0, columnspan=1, sticky="")

        self.power_entry = customtkinter.CTkEntry(self.slider_progressbar_frame, placeholder_text="Numeric value (Kwh)")
        self.power_entry.grid(row=3, column=0, padx=(20, 10), sticky="ew")

        self.cost_label = customtkinter.CTkLabel(master=self.slider_progressbar_frame,
                                                 text="Enter your area power cost:", anchor="w")
        self.cost_label.grid(row=4, column=0, columnspan=1, sticky="")

        self.cost_entry = customtkinter.CTkEntry(self.slider_progressbar_frame,
                                                 placeholder_text="Numeric value for price (CAD)")
        self.cost_entry.grid(row=5, column=0, padx=(20, 10), sticky="ew")

        self.roof_label = customtkinter.CTkLabel(master=self.slider_progressbar_frame,
                                                 text="Enter the roof area for the solar panel:", anchor="w")
        self.roof_label.grid(row=6, column=0, columnspan=1, sticky="")

        self.roof_entry = customtkinter.CTkEntry(self.slider_progressbar_frame, placeholder_text="Numeric value (m^2)")
        self.roof_entry.grid(row=7, column=0, padx=(20, 10), sticky="ew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Submit Data", fg_color="transparent",
                                                     border_width=4, text_color=("gray10", "#DCE4EE"),
                                                     command=self.generate_data, width=20)

        self.main_button_1.grid(row=3, column=1, padx=(10, 200), pady=(0), sticky="nsew", columnspan = 2)

        self.checkbox_slider_frame = customtkinter.CTkFrame(self, width=30)
        self.checkbox_slider_frame.grid(row=1, column=2, padx=(2, 200), pady=(10, 0), sticky="nsew", rowspan=1)

        self.option_label = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="Options")
        self.option_label.grid(row=1, column=0, pady=(10, 0), padx=20, sticky="w")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Number of Panel")
        self.checkbox_1.grid(row=2, column=0, pady=(10, 0), padx=20, sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Power Generated")
        self.checkbox_2.grid(row=3, column=0, pady=(10, 0), padx=20, sticky="w")

        self.checkbox_4 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Calculated Saving")
        self.checkbox_4.grid(row=5, column=0, pady=10, padx=20, sticky="w")



        # Add a label inside the custom frame next to the checkbox



    def about_us_button(self):
        # Create a scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="About us", width=300)
        self.scrollable_frame.grid(row=0, column=1, padx=10, pady=(5), sticky="nw")
        mess = "Five first year engineering folks:\n\n_Khai Huynh\n_Matthew Holden\n_Nhat Quang Nguyen\n_Claudiu Cociuba\n_Stephan Agwai\n\nWho are driven enough to pull up a\n \"painfull\" all nighter:(((\n\nABOUT PROJECT:\n\n  Solar Sense YYC aims to bring \nawareness to living a sustainable\n lifestyle by showcasing the ease\n and affordability of solar panels. \nThis is done by simply inputting \nyour address and some simple\n parameters like how much \nroof space you are willing to\nallocate and average yearly \npower consumption. From this \nwe are able to calculate your \naverage power created with solar \npanels based on solar data. \nWith the use of the Solcast \nAPI and the Geopy API, you are \nable to calculate the cost of \nsolar panels anywhere in \nthe world."
      
  
        # Text widget inside the scrollable frame
        self.switch = customtkinter.CTkLabel(master=self.scrollable_frame, text=mess, height= 100,justify= "left" )
        self.switch.grid(row = 1, column = 1)
    def exit_program(self):
        self.destroy()

    def generate_data(self):
        print("Generating...")

        checkbox_1_state = self.checkbox_1.get()
        checkbox_2_state = self.checkbox_2.get()
        checkbox_4_state = self.checkbox_4.get()

        address_entry_state = self.address_entry.get()
        power_entry_state = self.power_entry.get()
        roof_entry_state = self.roof_entry.get()
        cost_entry_state = self.cost_entry.get()

        
        final_info= output(address_entry_state,float(power_entry_state), float(cost_entry_state),float(roof_entry_state))
        print(final_info)


        print(checkbox_1_state,checkbox_2_state,checkbox_4_state)
        self.tabview = customtkinter.CTkTabview(self, width=590)
        self.tabview.grid(row=0, column=2, padx=5, pady=5, sticky="nsew", columnspan=2)
        if checkbox_1_state == 1:
            self.tabview.add("Number of Panel and Cost")
            self.panel_cost = customtkinter.CTkLabel(self.tabview.tab("Number of Panel and Cost"),
                                                     text="Number of Panel can apply: " + final_info[
                                                         1] + "\nPanel size: 1.7m x 1.0m\nCost and Labour per panel: $413 CAD\n\nTotal Cost: $" +
                                                          final_info[3] + " CAD",
                                                     justify="left",
                                                     font=("Helvetica", 20))
            self.panel_cost.grid(row=2, column=0, padx=20, pady=(10, 10))
        if checkbox_2_state == 1:
            self.tabview.add("Power Generated")
            self.power = customtkinter.CTkLabel(self.tabview.tab("Power Generated"),
                                                text="Average household power usage per year: "+power_entry_state+
                                                     " Kwh\nTotal power generated by solar panel per year: "+final_info[2]+" Kwh\n\nExcess power: "+str(float(final_info[2])-float(power_entry_state))+" Kwh",
                                                justify="left",
                                                font=("Helvetica", 20))
            self.power.grid(row=2, column=0, padx=20, pady=(10, 10))

        if checkbox_4_state == 1:
            self.tabview.add("Financial")
            if float(final_info[5])>= 0:
                self.finance = customtkinter.CTkLabel(self.tabview.tab("Financial"),
                                                    text="You earned $"+final_info[5]+" through the grid per year.",
                                                    justify="left",
                                                    font=("Helvetica", 20))
                self.finance.grid(row=2, column=0, padx=20, pady=(10, 10))
            else:
                self.finance = customtkinter.CTkLabel(self.tabview.tab("Financial"),
                                                      text="You have to pay $" + str(-int(final_info[
                                                          5])) + " for electricity bill per year.",
                                                      justify="left",
                                                      font=("Helvetica", 20))
                self.finance.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.custom_frame_next_to_checkbox = customtkinter.CTkFrame(self, width=100, height=100, bg_color="transparent", fg_color="#8B0000")
        self.custom_frame_next_to_checkbox.grid(row=1, column=2, padx=(345, 10), pady=(10, 0), sticky="nsew",columnspan = 2)
        self.custom_label = customtkinter.CTkLabel(self.custom_frame_next_to_checkbox,
                                                   text="In "+final_info[4]+" years, you'll be on the \n"
                                                                            "verge of recouping the entire \n"
                                                                            "expense of installing sustainable \n"
                                                                            "solar panels, ensuring the ongoing\n"
                                                                            "benefits of free and environmentally\n"
                                                                            
                                                                            "friendly electricity.", font=("Helvetica", 20), justify
                                                   ="left", pady = 30)
        self.custom_label.pack(padx=10, pady=10)









if __name__ == "__main__":
    app = App()
    app.mainloop()


