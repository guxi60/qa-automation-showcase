*** Settings ***
Resource    common.resource

*** Keywords ***
Login With Credentials
    [Documentation]    Fill username, password and click Login.
    [Arguments]    ${username}    ${password}
    Input Text    css=[data-test="username"]    ${username}
    Input Text    css=[data-test="password"]    ${password}
    JS Click Element    css=[data-test="login-button"]

Get Login Error Text
    [Documentation]    Return the error message text.
    Wait Until Element Is Visible    css=[data-test="error"]    timeout=${TIMEOUT}
    ${error}=    Get Text    css=[data-test="error"]
    RETURN    ${error}

Verify Login Form Elements Visible
    [Documentation]    Assert all login form elements are visible.
    Wait Until Element Is Visible    css=[data-test="username"]    timeout=${TIMEOUT}
    Wait Until Element Is Visible    css=[data-test="password"]    timeout=${TIMEOUT}
    Wait Until Element Is Visible    css=[data-test="login-button"]    timeout=${TIMEOUT}
    Element Attribute Value Should Be
    ...    css=[data-test="login-button"]    value    Login

Verify Redirected To Inventory
    [Documentation]    Assert URL is the inventory page and Products title is visible.
    Location Should Be    ${INVENTORY_URL}
    Wait Until Page Contains    Products    timeout=${TIMEOUT}

Login And Go To Inventory
    [Documentation]    Full login flow: navigate → login → verify. Returns to Inventory-ready state.
    Navigate To Login
    Login With Credentials    standard_user    secret_sauce
    Wait Until Location Is    ${INVENTORY_URL}    timeout=${TIMEOUT}
    Wait Until Page Contains    Products    timeout=${TIMEOUT}
