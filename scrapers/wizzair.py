from seleniumbase import SB

FROM_LOC = "London Gatwick"
TO_LOC = "Prague"
ONE_WAY = True
DEPARTURE_DATE = "Friday 15 August 2025"

with SB(uc=True, test=True,locale="en", ad_block=True) as sb:
    url= "https://www.wizzair.com/en-gb"
    sb.activate_cdp_mode(url)
    sb.sleep(5)
    sb.cdp.click_if_visible('button#onetrust-reject-all-handler')
    if ONE_WAY:
        sb.cdp.click('input#radio-button-id-5')
    sb.cdp.type('input#wa-autocomplete-input-7',FROM_LOC)
    sb.cdp.click(f'div[role="option"]')
    sb.cdp.type('input#wa-autocomplete-input-9',TO_LOC)
    sb.cdp.click(f'div[role="option"]')
    sb.cdp.type('fieldset[data-test="date-inputs"]',DEPARTURE_DATE)
    #sb.cdp.click(f'span[role="button" name="{DEPARTURE_DATE}"]')
    #sb.cdp.click(f'span[role="button"]')
    sb.cdp.click(f'span[aria-label="{DEPARTURE_DATE}"]')
    sb.cdp.click(f'button[data-test="flight-search-submit"]')
    for window in sb.driver.window_handles:
        sb.switch_to_window(window)
        if "/booking/select-flight" in sb.get_current_url():
            break
    
    sb.cdp.click_if_visible('button#onetrust-reject-all-handler')
    sb.sleep(25)
     