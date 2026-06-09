*** Settings ***
Suite Setup       Start Test Session
Suite Teardown    End Test Session
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource
Resource          ../resources/cart_keywords.resource


*** Keywords ***
Go To Inventory Cleaned
    [Documentation]    Log in and remove all items from cart.
    Login And Go To Inventory
    ${btns}=    Get WebElements    xpath=//div[@class='inventory_item']//button[contains(text(),'Remove')]
    FOR    ${btn}    IN    @{btns}
        Click Button    ${btn}
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
    [Tags]    smoke
    [Documentation]    Cart page should display all items added from inventory.
    Go To Cart With Items    Sauce Labs Backpack    Sauce Labs Onesie
    ${count}=    Get Cart Item Count
    Should Be Equal As Integers    ${count}    2
    ${names}=    Get Cart Item Names
    List Should Contain Value    ${names}    Sauce Labs Backpack
    List Should Contain Value    ${names}    Sauce Labs Onesie

TC-CART-002: Removing An Item Decrements Count And Removes From List
    [Tags]    functional
    [Documentation]    Removing one item from cart updates count and listing.
    Go To Cart With Items    Sauce Labs Backpack    Sauce Labs Onesie
    Remove Item From Cart    Sauce Labs Backpack
    ${count}=    Get Cart Item Count
    Should Be Equal As Integers    ${count}    1
    ${names}=    Get Cart Item Names
    List Should Not Contain Value    ${names}    Sauce Labs Backpack

TC-CART-003: Cart Badge Survives Navigation Away And Back
    [Tags]    functional    state
    [Documentation]    Cart badge persists across page navigation.
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
    [Tags]    functional
    [Documentation]    Navigating to cart without adding items shows empty cart.
    Go To Inventory Cleaned
    Go To Cart
    Cart Should Be Loaded
    ${count}=    Get Cart Item Count
    Should Be Equal As Integers    ${count}    0

TC-CART-005: Checkout Button Is Visible And Enabled
    [Tags]    functional    gui
    [Documentation]    Checkout button should be present when cart has items.
    Go To Cart With One Item
    Element Should Be Visible    css=[data-test="checkout"]
    Element Should Be Enabled    css=[data-test="checkout"]
