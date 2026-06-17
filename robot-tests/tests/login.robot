*** Settings ***
Test Setup        Start Browser
Test Teardown     Close Browser
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource

*** Variables ***
${STANDARD_USER}      standard_user
${SECRET_SAUCE}       secret_sauce
${LOCKED_USER}        locked_out_user


*** Keywords ***
Negative Login Template
    [Documentation]    DDT template for negative/boundary login tests.
    [Arguments]    ${username}    ${password}    ${expected_error}
    Navigate To Login
    Login With Credentials    ${username}    ${password}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    ${expected_error}

Negative Login With URL Check
    [Documentation]    DDT template for negative login that also checks URL.
    [Arguments]    ${username}    ${password}    ${expected_error}
    Navigate To Login
    Login With Credentials    ${username}    ${password}
    ${error}=    Get Login Error Text
    Should Contain    ${error}    ${expected_error}
    Location Should Be    ${BASE_URL}


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
    [Template]    Negative Login With URL Check
    ${STANDARD_USER}    wrong_password    do not match

TC-LOGIN-003: Empty Username Is Rejected
    [Tags]    negative    validation    boundary
    [Template]    Negative Login Template
    ${EMPTY}    ${SECRET_SAUCE}    Username is required

TC-LOGIN-004: Empty Password Is Rejected
    [Tags]    negative    validation    boundary
    [Template]    Negative Login Template
    ${STANDARD_USER}    ${EMPTY}    Password is required

TC-LOGIN-005: Locked-Out User Is Denied
    [Tags]    negative    access-control
    [Template]    Negative Login With URL Check
    ${LOCKED_USER}    ${SECRET_SAUCE}    locked out

TC-LOGIN-006: Login Page Renders Required Elements
    [Tags]    smoke    gui
    [Documentation]    All form controls must be visible on initial load.
    Navigate To Login
    Verify Login Form Elements Visible
