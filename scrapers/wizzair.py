from seleniumbase import SB

FROM_LOC = "London Gatwick"
TO_LOC = "Prague"
ONE_WAY = True
DEPARTURE_DATE = "Friday 15 August 2025"
def wizzair_scraper(Departure_airport = FROM_LOC, Destination_airport = TO_LOC, formatted_date = DEPARTURE_DATE, one_way=True):
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
        sb.sleep(5)
        sb.cdp.click_if_visible('button#onetrust-reject-all-handler')
        #self.cdp.select_all(selector)
        days = sb.find_elements('div[class*="flight-select__flight"][data-test*="flight-select-flight"]')
        print("Found elements")
        for day in days: #doesnt actually loop yet
            if not day.text.strip():
                continue
            print("**** " + " ".join(day.text.split("\n")[0:2]) + " ****")
            info = day.text.split()
            length = info[-11] + info[-10]
            print("".join(length))
            land = info[-9]
            depart = info[-15]
            price = info[-4]
            
            return price

if __name__ == "__main__": wizzair_scraper()
     