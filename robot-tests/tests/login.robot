*** Settings ***
Test Setup        Start Test Session
Test Teardown     End Test Session
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource

*** Variables ***
${STANDARD_USER}      standard_user
${SECRET_SAUCE}       secret_sauce
${LOCKED_USER}        locked_out_user


*** Test Cases ***
TC-LOGIN-001: Valid Credentials Grant Access
    [Tags]    smoke    happy-path    REQ-AUTH-001
    [Documentation]    Given the user is on the login page
    ...                When they enter a correct username and password and click Login
    ...                Then the page redirects to /inventory.html, displaying the "Products" title
    Navigate To Login
    Login With Credentials    ${STANDARD_USER}    ${SECRET_SAUCE}
    Verify Redirected To Inventory
    ${count}=    Get Product Count
    Should Be Equal As Integers    ${count}    6

TC-LOGIN-002: Wrong Password Is Rejected
    [Tags]    negative    validation    REQ-AUTH-002
    [Documentation]    Given the user is on the login page
    ...                When they enter a correct username but a wrong password and click Login
    ...                Then the page stays on the login page and displays an error containing "do not match"
    Navigate To Login
    Login With Credentials    ${STANDARD_USER}    wrong_password
    ${error}=    Get Login Error Text
    Should Contain    ${error}    do not match
    Location Should Be    ${BASE_URL}

TC-LOGIN-003: Empty Username Is Rejected
    [Tags]    negative    validation    boundary    REQ-AUTH-003
    [Documentation]    Given the user is on the login page
    ...                When the username is empty and password is non-empty, then click Login
    ...                Then the error "Username is required" is displayed
    Navigate To Login
    Login With Credentials    ${EMPTY}    ${SECRET_SAUCE}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    Username is required

TC-LOGIN-004: Empty Password Is Rejected
    [Tags]    negative    validation    boundary    REQ-AUTH-004
    [Documentation]    Given the user is on the login page
    ...                When the username is non-empty and password is empty, then click Login
    ...                Then the error "Password is required" is displayed
    Navigate To Login
    Login With Credentials    ${STANDARD_USER}    ${EMPTY}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    Password is required

TC-LOGIN-005: Locked-Out User Is Denied
    [Tags]    negative    access-control    REQ-AUTH-005
    [Documentation]    Given the user is on the login page
    ...                When they attempt to log in with a locked-out account
    ...                Then an error containing "locked out" is displayed and the user remains on the login page
    Navigate To Login
    Login With Credentials    ${LOCKED_USER}    ${SECRET_SAUCE}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    locked out
    Location Should Be    ${BASE_URL}

TC-LOGIN-006: Login Page Renders Required Elements
    [Tags]    smoke    gui    REQ-AUTH-006
    [Documentation]    Given the user visits the login page
    ...                When the page finishes loading
    ...                Then the username input, password input, and Login button are all visible,
    ...                and the button reads "Login"
    Navigate To Login
    Verify Login Form Elements Visible
