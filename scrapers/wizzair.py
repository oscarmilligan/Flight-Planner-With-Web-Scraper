from seleniumbase import SB
import pandas

FROM_LOC = "London Gatwick"
TO_LOC = "Prague"
ONE_WAY = True
DEPARTURE_DATE = "Friday 15 August 2025"
def wizzair_scraper(Departure_airport = FROM_LOC, Destination_airport = TO_LOC, formatted_date = DEPARTURE_DATE, one_way=True):
    if Departure_airport[:7] == "Budapest": Departure_airport = "Budapest"
    if Destination_airport[:7] == "Budapest": Destination_airport = "Budapest"
    for x in (Departure_airport, Destination_airport):
        x = x.strip("Airport")
    with SB(uc=True, test=True,locale="en", ad_block=True) as sb:
        url= "https://www.wizzair.com/en-gb"
        sb.activate_cdp_mode(url)
        sb.sleep(5)
        sb.cdp.click_if_visible('button#onetrust-reject-all-handler')
        if one_way:
            sb.cdp.click('input#radio-button-id-5')
        sb.cdp.type('input#wa-autocomplete-input-7',Departure_airport)
        sb.cdp.click(f'div[role="option"]')
        sb.cdp.type('input#wa-autocomplete-input-9',Destination_airport)
        sb.cdp.click(f'div[role="option"]')
        sb.cdp.type('fieldset[data-test="date-inputs"]',formatted_date)
        #sb.cdp.click(f'span[role="button" name="{DEPARTURE_DATE}"]')
        #sb.cdp.click(f'span[role="button"]')
        sb.cdp.click(f'span[aria-label="{formatted_date}"]')
        sb.cdp.click(f'button[data-test="flight-search-submit"]')
        sb.sleep(5)
        
        sb.cdp.close_active_tab()
        sb.cdp.switch_to_newest_tab()
        print("111111")
        sb.sleep(3)
        sb.cdp.click_if_visible('button#onetrust-reject-all-handler')
        #self.cdp.select_all(selector)
        days = sb.find_elements('div[class*="flight-select__flight"][data-test*="flight-select-flight"]')
        print("Found elements")
        flight_info = pandas.DataFrame(columns=["duration","land_time","depart_time","price"])
        for day in days: #doesnt actually loop yet
            if not day.text.strip():
                continue
            print("**** " + " ".join(day.text.split("\n")[0:2]) + " ****")
            info = day.text.split()
            duration = info[-11] + info[-10]
            print("".join(duration))
            land_time = info[-9]
            depart_time = info[-15]
            price = float(info[-4][1:])
            new_info=pandas.DataFrame({"duration":[duration],"land_time":[land_time],"depart_time":[depart_time],"price":[price]})
            flight_info = pandas.concat([flight_info,new_info],ignore_index=True)
           
        return flight_info.drop_duplicates()

if __name__ == "__main__": print(wizzair_scraper())
     