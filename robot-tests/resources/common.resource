*** Settings ***
Library           SeleniumLibrary
Library           String
Library           Collections
Variables         test_data.py

*** Variables ***
${BASE_URL}               https://www.saucedemo.com/
${INVENTORY_URL}          https://www.saucedemo.com/inventory.html
${CART_URL}               https://www.saucedemo.com/cart.html
${TIMEOUT}                20s
${RETRY_INTERVAL}         500ms

*** Keywords ***
Start Browser
    [Documentation]    Open a fresh browser instance. Called as Test Setup.
    Open Browser    ${BASE_URL}    Chrome    options=${CHROME_OPTIONS}    executable_path=${CHROMEDRIVER_PATH}
    Set Window Size    1280    720
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Implicit Wait    10s
    Register Keyword To Run On Failure    Capture Screenshot On Failure

Close Browser
    [Documentation]    Close browser. Called as Test Teardown.
    Close All Browsers
    Sleep    1s

Capture Screenshot On Failure
    [Documentation]    Capture screenshot on failure (registered as run-on-failure).
    Capture Page Screenshot

Clear Session State
    [Documentation]    Delete all cookies to prevent cross-test session carry-over.
    Go To    ${BASE_URL}
    Delete All Cookies

Navigate To Login
    [Documentation]    Go to the SauceDemo login page.
    Go To    ${BASE_URL}
    Wait Until Element Is Visible    css=[data-test="login-button"]    timeout=${TIMEOUT}

JS Click Element
    [Documentation]    Click an element via JavaScript (reliable on headless Linux).
    [Arguments]    ${locator}
    ${el}=    Get WebElement    ${locator}
    Execute Javascript    arguments[0].click();    ARGUMENTS    ${el}

JS Input Text
    [Documentation]    Clear & fill an input via JavaScript (reliable on headless Linux).
    [Arguments]    ${locator}    ${text}
    ${el}=    Get WebElement    ${locator}
    Execute Javascript    arguments[0].value=''; arguments[0].value=arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));    ARGUMENTS    ${el}    ${text}
