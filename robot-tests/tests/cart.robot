*** Settings ***
Test Setup        Start Test Session
Test Teardown     End Test Session
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource
Resource          ../resources/cart_keywords.resource


*** Keywords ***
Go To Inventory Cleaned
    [Documentation]    Log in and remove all items from cart.
    Login And Go To Inventory
    ${btns}=    Get WebElements    xpath=//div[@class='inventory_item']//button[contains(text(),'Remove')]
    FOR    ${btn}    IN    @{btns}
        JS Click Element    ${btn}
    END

Go To Cart With One Item
    [Documentation]    Login, clean cart, add Sauce Labs Backpack, navigate to cart.
    Go To Inventory Cleaned
    Add Item To Cart    Sauce Labs Backpack
    Go To Cart
    Cart Should Be Loaded

Go To Cart With Items
    [Documentation]    Login, clean cart, add Backpack + Onesie, navigate to cart.
    [Arguments]    ${item1}    ${item2}
    Go To Inventory Cleaned
    Add Item To Cart    ${item1}
    Add Item To Cart    ${item2}
    Go To Cart
    Cart Should Be Loaded


*** Test Cases ***
TC-CART-001: Items Added From Inventory Appear In Cart
    [Tags]    smoke    REQ-CART-001
    [Documentation]    Given the user added N items from the Inventory
    ...                When navigating to the Cart page
    ...                Then the cart displays N items with names matching those added
    Go To Cart With Items    Sauce Labs Backpack    Sauce Labs Onesie
    ${count}=    Get Cart Item Count
    Should Be Equal As Integers    ${count}    2
    ${names}=    Get Cart Item Names
    List Should Contain Value    ${names}    Sauce Labs Backpack
    List Should Contain Value    ${names}    Sauce Labs Onesie

TC-CART-002: Removing An Item Decrements Count And Removes From List
    [Tags]    functional    REQ-CART-002
    [Documentation]    Given the cart has 2 items
    ...                When clicking Remove on 1 of them
    ...                Then the item count drops to 1 and the removed item is no longer in the list
    Go To Cart With Items    Sauce Labs Backpack    Sauce Labs Onesie
    Remove Item From Cart    Sauce Labs Backpack
    ${count}=    Get Cart Item Count
    Should Be Equal As Integers    ${count}    1
    ${names}=    Get Cart Item Names
    List Should Not Contain Value    ${names}    Sauce Labs Backpack

TC-CART-003: Cart Badge Survives Navigation Away And Back
    [Tags]    functional    state    REQ-CART-003
    [Documentation]    Given the user added 1 item (badge shows 1)
    ...                When navigating to the cart and back to Inventory
    ...                Then the badge still shows 1 and the item remains in the cart
    Go To Inventory Cleaned
    Add Item To Cart    Sauce Labs Backpack
    ${badge}=    Get Cart Badge Count
    Should Be Equal As Integers    ${badge}    1
    Go To Cart
    Click Continue Shopping
    Wait Until Page Contains    Products    timeout=${TIMEOUT}
    ${badge}=    Get Cart Badge Count
    Should Be Equal As Integers    ${badge}    1

TC-CART-004: Empty Cart Shows Zero Items
    [Tags]    functional    REQ-CART-004
    [Documentation]    Given the user has just logged in without adding items
    ...                When navigating to the Cart page
    ...                Then the cart is empty (item count = 0)
    Go To Inventory Cleaned
    Go To Cart
    Cart Should Be Loaded
    ${count}=    Get Cart Item Count
    Should Be Equal As Integers    ${count}    0

TC-CART-005: Checkout Button Is Visible And Enabled
    [Tags]    functional    gui    REQ-CART-005
    [Documentation]    Given the cart has items
    ...                When viewing the checkout button
    ...                Then the button is visible and enabled
    Go To Cart With One Item
    Element Should Be Visible    css=[data-test="checkout"]
    Element Should Be Enabled    css=[data-test="checkout"]
