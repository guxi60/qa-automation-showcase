*** Settings ***
Suite Setup       Start Test Session
Suite Teardown    End Test Session
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource

*** Variables ***
${STANDARD_USER}      standard_user
${SECRET_SAUCE}       secret_sauce
${LOCKED_USER}        locked_out_user


*** Test Cases ***
TC-LOGIN-001: Valid Credentials Grant Access
    [Tags]    smoke    happy-path
    [Documentation]    Login with valid credentials should redirect to inventory.
    Navigate To Login
    Login With Credentials    ${STANDARD_USER}    ${SECRET_SAUCE}
    Verify Redirected To Inventory
    ${count}=    Get Product Count
    Should Be Equal As Integers    ${count}    6

TC-LOGIN-002: Wrong Password Is Rejected
    [Tags]    negative    validation
    [Documentation]    Wrong password should show error and stay on login page.
    Navigate To Login
    Login With Credentials    ${STANDARD_USER}    wrong_password
    ${error}=    Get Login Error Text
    Should Contain    ${error}    do not match
    Location Should Be    ${BASE_URL}

TC-LOGIN-003: Empty Username Is Rejected
    [Tags]    negative    validation    boundary
    [Documentation]    Empty username with valid password shows required error.
    Navigate To Login
    Login With Credentials    ${EMPTY}    ${SECRET_SAUCE}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    Username is required

TC-LOGIN-004: Empty Password Is Rejected
    [Tags]    negative    validation    boundary
    [Documentation]    Valid username with empty password shows required error.
    Navigate To Login
    Login With Credentials    ${STANDARD_USER}    ${EMPTY}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    Password is required

TC-LOGIN-005: Locked-Out User Is Denied
    [Tags]    negative    access-control
    [Documentation]    Locked-out account should show locked out error.
    Navigate To Login
    Login With Credentials    ${LOCKED_USER}    ${SECRET_SAUCE}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    locked out
    Location Should Be    ${BASE_URL}

TC-LOGIN-006: Login Page Renders Required Elements
    [Tags]    smoke    gui
    [Documentation]    All form controls must be visible on initial load.
    Navigate To Login
    Verify Login Form Elements Visible
