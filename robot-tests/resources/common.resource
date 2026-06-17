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
Start Test Session
    [Documentation]    Open browser and set window size. Called as Suite Setup.
    Open Browser    ${BASE_URL}    Chrome    options=${CHROME_OPTIONS}    executable_path=${CHROMEDRIVER_PATH}
    Set Window Size    1280    720
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Implicit Wait    10s
    Register Keyword To Run On Failure    Capture Screenshot On Failure

End Test Session
    [Documentation]    Close browser and allow driver process to terminate.
    Close All Browsers
    Sleep    2s

Capture Screenshot On Failure
    [Documentation]    Capture screenshot on failure (registered as run-on-failure).
    Capture Page Screenshot

Clear Session State
    [Documentation]    Delete all cookies + storage to prevent cross-test carry-over.
    Go To    ${BASE_URL}
    Delete All Cookies
    Execute Javascript    window.localStorage.clear(); window.sessionStorage.clear();

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
    [Documentation]    Clear & fill an input via native setter (triggers React).
    [Arguments]    ${locator}    ${text}
    ${el}=    Get WebElement    ${locator}
    Execute Javascript    var n=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; n.call(arguments[0],arguments[1]); arguments[0].dispatchEvent(new InputEvent('input',{bubbles:true}));    ARGUMENTS    ${el}    ${text}
