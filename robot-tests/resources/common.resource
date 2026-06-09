*** Settings ***
Library           SeleniumLibrary
Library           String
Library           Collections
Variables         test_data.py

*** Variables ***
${BASE_URL}               https://www.saucedemo.com/
${INVENTORY_URL}          https://www.saucedemo.com/inventory.html
${CART_URL}               https://www.saucedemo.com/cart.html
${TIMEOUT}                10s
${RETRY_INTERVAL}         500ms

*** Keywords ***
Start Test Session
    [Documentation]    Open browser and set window size. Called as Suite Setup.
    Open Browser    ${BASE_URL}    Chrome    options=${CHROME_OPTIONS}    executable_path=${CHROMEDRIVER_PATH}
    Set Window Size    1280    720
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Implicit Wait    5s
    Register Keyword To Run On Failure    Capture Screenshot On Failure

End Test Session
    [Documentation]    Close browser and allow driver process to terminate.
    Close All Browsers
    Sleep    2s

Capture Screenshot On Failure
    [Documentation]    Capture screenshot on failure (registered as run-on-failure).
    Capture Page Screenshot

Navigate To Login
    [Documentation]    Go to the SauceDemo login page.
    Go To    ${BASE_URL}
    Wait Until Element Is Visible    css=[data-test="login-button"]    timeout=${TIMEOUT}
