from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

# main automation process at the bottom of the file.

# DOWNLOAD FIREFOX DRIVER AND SPECIFY IT'S LOCATION IN config.json at the 'driverLocation' field. 

# load the credentials and driver location from the config 
with open("config.json", "r") as f:
    config = json.load(f)
    credentials = config["credentials"]
    driver_executable = config["driverLocation"]

# for a different browser, you'd have to change the next 3 lines
profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webnotifications.enabled", False)   # disable notifications in the browser.
driver = webdriver.Firefox(firefox_profile=profile,executable_path=driver_executable)    # start driver
# this 30 seconds wait will occur when the driver can't find any elements of the specified selector(like when deleting is complete)
driver.maximize_window()    #maximize window
driver.implicitly_wait(30)  # wait for 30 seconds at most to find an object on the web page(should be adjusted for slower internet connections)
requests_wait = 5   # 5 seconds wait for requests that take some time(opening login iframe and logging in).

# navigate to reddit's home page and click login
def go_to_reddit_login():
    driver.get('https://reddit.com')                              # navigate to reddit's login page
    accept_cookies()
    click_object(driver.find_element_by_css_selector("[href*='https://www.reddit.com/login/']"))
    time.sleep(requests_wait)   # wait 5 seconds for the iframe.

# click accept on the toaster prompting about cookies
def accept_cookies():
    accept_cookies = driver.find_elements_by_css_selector("form button[type='submit']")[1]
    click_object(accept_cookies)

# navigate to the profile after logging in (choose whether )
def go_to_profile_page(posts, comments):
    if posts:
        sub_page = '/posts/'    # will display posts only
    elif comments:
        sub_page = '/comments/' # will display comments only
    else:
        sub_page = ''               # will default to 'overview'
    driver.get('https://reddit.com/user/'+credentials["username"] + sub_page)

# switch the driver's focus to the login iframe after clicking login.
def switch_to_login_iframe():
    login_iframe = driver.find_element_by_css_selector('[src*="https://www.reddit.com/login/"]')
    driver.switch_to.frame(login_iframe)

# switch the driver's focus back to the default window
def switch_to_window():
    driver.switch_to.default_content()

# fill in the login form and press enter to login.
def login(username, password):
    username_input = driver.find_element_by_id("loginUsername")
    password_input = driver.find_element_by_id("loginPassword")
    username_input.send_keys(username)
    password_input.send_keys(password + Keys.ENTER)  # optionally send an Enter key press after the password is entered
    time.sleep(requests_wait)   # couldn't be bothered to make a proper wait for the login request. Just increase this if the browser navigates before the login is complete.

# delete the first post on the profile page.
def delete_post():
    posts_menu_button = driver.find_element_by_css_selector("button[aria-label='more options']")
    click_object(posts_menu_button)
    actions_menu = driver.find_elements_by_css_selector("div[role='menu'] button")
    click_object(actions_menu[len(actions_menu)-1])
    delete_confirmation_button = driver.find_elements_by_css_selector("div[role='dialog'] footer button")[1]
    click_object(delete_confirmation_button)

# check if there's remaining posts
def are_there_posts_remaining(posts_only, comments_only):
    if posts_only:
        go_to_profile_page(True, False)
        posts_menu_button = driver.find_elements_by_css_selector("button[aria-label='more options']")
        return bool(len(posts_menu_button)>0)
    elif comments_only:
        go_to_profile_page(False, True)
        posts_menu_button = driver.find_elements_by_css_selector("button[aria-label='more options']")
        return bool(len(posts_menu_button)>0)
    else:
        go_to_profile_page(True,False)
        posts_menu_button = driver.find_elements_by_css_selector("button[aria-label='more options']")
        if(len(posts_menu_button) == 0): # finished deleting posts
            go_to_profile_page(False, True)
            posts_menu_button = driver.find_elements_by_css_selector("button[aria-label='more options']")
        return bool(len(posts_menu_button)>0)

def click_object(web_element):
    try:
        web_element.click()                                             # try click the element normally
    except:
        driver.execute_script("arguments[0].click()", web_element)     # click the element forcefully by javascript if normal clicks don't work

# main automation process
def main():
    go_to_reddit_login()
    switch_to_login_iframe()
    login(credentials["username"], credentials["password"])
    switch_to_window()
    ## Set the arguments in the while condition to:
    #   Posts, Comments : operation
    #   True, False : to delete posts only
    #   False, True : to delete comments only
    #   False, False: To delete everything.
    #   (True, True will operate like true false since posts are prioritized in that method)
    posts_only = False      # set true to delete posts only.
    comments_only = False   # set true(and other false) to delete comments only.
    while(are_there_posts_remaining(posts_only,comments_only)):
        delete_post()
        if('/comments/' in driver.current_url):
            comments_only = True    # set the remaining of the delete process to comments only if there are no more posts to delete.
    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()
