import asyncio
from sys import argv
from pyppeteer import launch

# Example usage
username = argv[1]
password = argv[2]

print (f"Username: {username}")
print (f"Password: {password}")
async def login_to_prusa_connect(username, password):
    browser = await launch(headless=True)  # Set to True to run headless
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})

    # Navigate to the login page
    await page.goto('https://connect.prusa3d.com/login')

    # Wait for the username input to appear and type the username
    await page.waitForSelector('input[name="email"]')
    await page.type('input[name="email"]', username)

    # # Wait for the password input to appear and type the password
    await page.waitForSelector('input[name="password"]')
    await page.type('input[name="password"]', password)

    # # Click the login button
    await page.click('button[type="submit"]')

    # Wait for navigation to complete
    await page.waitForNavigation()
    print("Logged in!")

    button_xpath = '//button[contains(text(), "I am OK with that")]'

    while True:
        try:
            # Wait for the button to appear
            await page.waitForXPath(button_xpath, timeout=5000)

            # Get the list of buttons matching the XPath
            buttons = await page.xpath(button_xpath)

            if buttons:
                button = buttons[0]  # Use the first matching button

                # Check if the button is enabled
                disabled = await page.evaluate('(btn) => btn.disabled', button)
                if not disabled:
                    # Click the button
                    await button.click()

                    match button_xpath:
                        case '//button[contains(text(), "I am OK with that")]':
                            print("Clicked 'I am OK with that'")
                            button_xpath = '//button[.//div[contains(text(), "Set ready")]]'

                        case '//button[.//div[contains(text(), "Set ready")]]':
                            print("Clicked 'Set ready'")
                            button_xpath = '//button[.//div[contains(text(), "Confirm")]]'

                        case '//button[.//div[contains(text(), "Confirm")]]':
                            print("Clicked 'Confirm'")
                            await asyncio.sleep(5)
                            button_xpath = '//button[.//div[contains(text(), "Set ready")]]'
                        
                        case _:
                            continue
                else:
                    print("Button is disabled. Retrying...")
            else:
                print("Button not found. Retrying...")

        except asyncio.TimeoutError:
            print("Button not found within timeout. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait before retrying
        await asyncio.sleep(1)  # Adjust the sleep duration as needed
asyncio.get_event_loop().run_until_complete(login_to_prusa_connect(username, password))