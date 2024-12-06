#This is a for space type you want to rent or buy


def ActivityType():
    while True:
        choice = input("Please type: Rent or Buy: ").strip().lower()

        match choice:
            case "rent":
                return choice
            case "buy":
                return choice
            case _:
                print("Please try again, choose: Rent or Buy")

def BuildingType():
    while True:
        choice = input("Please choose: House, Apartment or Condo: ").strip().lower()

        match choice:
            case "house":
                return choice
            case "apartment":
                return choice
            case "Condo":
                return choice
            case _:
                print("Please try again, choose: House, Apartment or Condo: ")

def get_url():
    activity_type = ActivityType()
    building_type = BuildingType()

    url = f"https://www.realestate.com.kh/{activity_type}/{building_type}".__str__()


    return url

def open_browser_and_select_filters(url, driver):

    driver.get(url)
    print("Deschide browserul și selectează filtrele dorite.")
    print("După ce ai terminat, închide browserul.")

    input("Apasă Enter pentru a continua după ce ai selectat filtrele...")
    final_url = driver.current_url  # Obține URL-ul curent după selectarea filtrelor

    driver.quit()

    print(f"URL-ul selectat este: {final_url}")
    return final_url
