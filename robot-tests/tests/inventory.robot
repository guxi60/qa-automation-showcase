*** Settings ***
Test Setup        Start Test Session
Test Teardown     End Test Session
Resource          ../resources/login_keywords.resource
Resource          ../resources/inventory_keywords.resource


*** Keywords ***
Go To Inventory With Clean Cart
    [Documentation]    Log in and remove all items from cart.
    Login And Go To Inventory
    ${btns}=    Get WebElements    xpath=//div[@class='inventory_item']//button[contains(text(),'Remove')]
    FOR    ${btn}    IN    @{btns}
        JS Click Element    ${btn}
    END


*** Test Cases ***
TC-INV-001: Inventory Displays Exactly 6 Products After Login
    [Tags]    smoke    REQ-INV-001
    [Documentation]    Given the user is logged in
    ...                When they land on the Inventory page
    ...                Then 6 products are displayed with the title "Products"
    Go To Inventory With Clean Cart
    Inventory Should Be Loaded
    ${count}=    Get Product Count
    Should Be Equal As Integers    ${count}    6
    ${names}=    Get Product Names
    Length Should Be    ${names}    6

TC-INV-002: Every Product Has Non-Empty Name And Positive Price
    [Tags]    functional    data-integrity    REQ-INV-002
    [Documentation]    Given the user is on the Inventory page
    ...                When iterating over all products
    ...                Then every product has a non-empty name and a price > $0
    Go To Inventory With Clean Cart
    ${names}=    Get Product Names
    ${prices}=    Get Product Prices
    FOR    ${name}    IN    @{names}
        Should Not Be Empty    ${name}
    END
    FOR    ${price}    IN    @{prices}
        Should Be True    ${price} > 0    Product price ${price} must be > 0
    END

TC-INV-003: Every Product Image Has Valid Source
    [Tags]    gui    data-integrity    REQ-INV-003
    [Documentation]    Given the user is on the Inventory page
    ...                When viewing each product
    ...                Then every product image is visible and has a valid src attribute
    Go To Inventory With Clean Cart
    ${images}=    Get WebElements    css=.inventory_item img.inventory_item_img
    FOR    ${img}    IN    @{images}
        Scroll Element Into View    ${img}
        Wait Until Element Is Visible    ${img}    timeout=20s
        ${src}=    Get Element Attribute    ${img}    src
        Should Match Regexp    ${src}    ^(/static/media/|http).*
    END

TC-INV-004: Products Sort Correctly By Each Criterion
    [Tags]    functional    REQ-INV-004
    [Documentation]    Given the user is on the Inventory page
    ...                When selecting each sort option
    ...                Then the first product matches the expected sort order
    Go To Inventory With Clean Cart
    Sort Inventory By    Name (A to Z)
    ${names}=    Get Product Names
    Should Be Equal    ${names}[0]    Sauce Labs Backpack
    Sort Inventory By    Name (Z to A)
    ${names}=    Get Product Names
    Should Be Equal    ${names}[0]    Test.allTheThings() T-Shirt (Red)
    Sort Inventory By    Price (low to high)
    ${names}=    Get Product Names
    Should Be Equal    ${names}[0]    Sauce Labs Onesie
    Sort Inventory By    Price (high to low)
    ${names}=    Get Product Names
    Should Be Equal    ${names}[0]    Sauce Labs Fleece Jacket

TC-INV-005: Price Low-To-High Sort Is Numerically Correct
    [Tags]    functional    REQ-INV-005
    [Documentation]    Given the user selects "Price (low to high)"
    ...                When iterating over the price list
    ...                Then prices are in non-decreasing order
    Go To Inventory With Clean Cart
    Sort Inventory By    Price (low to high)
    ${prices}=    Get Product Prices
    ${sorted}=    Copy List    ${prices}
    Sort List    ${sorted}
    Lists Should Be Equal    ${prices}    ${sorted}

TC-INV-006: Cart Badge Is Hidden When Cart Is Empty
    [Tags]    functional    REQ-INV-006
    [Documentation]    Given the user has just logged in and landed on the Inventory page
    ...                When the cart is empty
    ...                Then the cart badge is not displayed
    Go To Inventory With Clean Cart
    ${count}=    Get Cart Badge Count
    Should Be Equal As Integers    ${count}    0

TC-INV-007: Cart Badge Increments As Items Are Added
    [Tags]    functional    REQ-INV-007
    [Documentation]    Given the cart is empty
    ...                When 2 items are added sequentially
    ...                Then the badge shows 1, then 2
    Go To Inventory With Clean Cart
    Add Item To Cart    Sauce Labs Backpack
    ${count}=    Get Cart Badge Count
    Should Be Equal As Integers    ${count}    1
    Add Item To Cart    Sauce Labs Bike Light
    ${count}=    Get Cart Badge Count
    Should Be Equal As Integers    ${count}    2

TC-INV-008: Add Then Remove Resets Cart Badge To Zero
    [Tags]    functional    REQ-INV-008
    [Documentation]    Given the user adds 1 item
    ...                When clicking Remove on that item
    ...                Then the badge returns to zero
    Go To Inventory With Clean Cart
    Add Item To Cart    Sauce Labs Backpack
    ${count}=    Get Cart Badge Count
    Should Be Equal As Integers    ${count}    1
    Remove Item From Inventory    Sauce Labs Backpack
    ${count}=    Get Cart Badge Count
    Should Be Equal As Integers    ${count}    0
