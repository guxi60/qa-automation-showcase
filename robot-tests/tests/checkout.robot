*** Settings ***
Test Setup        Start Test Session
Test Teardown     End Test Session
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource
Resource          ../resources/cart_keywords.resource
Resource          ../resources/checkout_keywords.resource


*** Keywords ***
Go To Cart Ready For Checkout
    [Documentation]    Login, add Backpack, go to cart.
    Login And Go To Inventory
    Add Item To Cart    Sauce Labs Backpack
    Go To Cart
    Cart Should Be Loaded


*** Test Cases ***
TC-CHK-001: Complete Purchase From Cart To Confirmation
    [Tags]    smoke    e2e    happy-path    REQ-CHK-001
    [Documentation]    Given the user's cart has items
    ...                When they complete the shipping form, review the order, and click Finish
    ...                Then a "Thank you" confirmation is displayed
    ...                and clicking Back Home returns to Inventory
    Go To Cart Ready For Checkout
    Click Checkout
    Fill Checkout Info    Gu    Xiang    201318
    Click Continue
    Wait Until Element Is Visible    css=[data-test="finish"]    timeout=${TIMEOUT}
    Location Should Be    ${CHECKOUT_STEP_TWO_URL}
    ${item_count}=    Get Checkout Item Count
    Should Be Equal As Integers    ${item_count}    1
    ${total}=    Get Order Total Text
    Should Contain    ${total}    Total
    Click Finish
    Location Should Be    ${CHECKOUT_COMPLETE_URL}
    ${header}=    Get Confirmation Header
    Should Contain    ${header}    Thank you
    Click Back Home
    Location Should Be    ${INVENTORY_URL}

TC-CHK-002: Empty First Name Rejected On Checkout
    [Tags]    negative    validation    REQ-CHK-002
    [Documentation]    Given the user is on the checkout form
    ...                When First Name is empty and Continue is clicked
    ...                Then an error containing "First Name" is displayed
    Go To Cart Ready For Checkout
    Click Checkout
    Fill Checkout Info    ${EMPTY}    Xiang    201318
    Click Continue
    ${error}=    Get Checkout Error Text
    Should Contain    ${error}    First Name

TC-CHK-003: Empty Last Name Rejected On Checkout
    [Tags]    negative    validation    REQ-CHK-003
    [Documentation]    Given the user is on the checkout form
    ...                When Last Name is empty and Continue is clicked
    ...                Then an error containing "Last Name" is displayed
    Go To Cart Ready For Checkout
    Click Checkout
    Fill Checkout Info    Gu    ${EMPTY}    201318
    Click Continue
    ${error}=    Get Checkout Error Text
    Should Contain    ${error}    Last Name

TC-CHK-004: Empty Postal Code Rejected On Checkout
    [Tags]    negative    validation    REQ-CHK-004
    [Documentation]    Given the user is on the checkout form
    ...                When Postal Code is empty and Continue is clicked
    ...                Then an error containing "Postal Code" is displayed
    Go To Cart Ready For Checkout
    Click Checkout
    Fill Checkout Info    Gu    Xiang    ${EMPTY}
    Click Continue
    ${error}=    Get Checkout Error Text
    Should Contain    ${error}    Postal Code

TC-CHK-005: Cancel On Checkout Returns To Cart
    [Tags]    navigation    REQ-CHK-005
    [Documentation]    Given the user is on the checkout form
    ...                When they click Cancel (without filling any fields)
    ...                Then they are returned to the cart page with no side effects
    Go To Cart Ready For Checkout
    Click Checkout
    Cancel Checkout
    Location Should Be    ${CART_URL}
