*** Settings ***
Resource    common.resource

*** Keywords ***
Get Product Count
    [Documentation]    Return the number of inventory items.
    ${items}=    Get WebElements    css=.inventory_item
    ${count}=    Get Length    ${items}
    RETURN    ${count}

Get Product Names
    [Documentation]    Return a list of product names.
    ${elements}=    Get WebElements    css=.inventory_item .inventory_item_name
    ${names}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        Append To List    ${names}    ${text}
    END
    RETURN    ${names}

Get Product Prices
    [Documentation]    Return a list of product prices as floats.
    ${elements}=    Get WebElements    css=.inventory_item .inventory_item_price
    ${prices}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${clean}=    Replace String    ${text}    $    ${EMPTY}
        ${price}=    Convert To Number    ${clean}
        Append To List    ${prices}    ${price}
    END
    RETURN    ${prices}

Add Item To Cart
    [Documentation]    Click Add to cart button for the product matching ${product_name}.
    [Arguments]    ${product_name}
    ${btn}=    Get WebElement
    ...    xpath=//div[@class='inventory_item' and contains(.,'${product_name}')]//button
    Click Button    ${btn}

Remove Item From Inventory
    [Documentation]    Click Remove button for the product matching ${product_name}.
    [Arguments]    ${product_name}
    ${btn}=    Get WebElement
    ...    xpath=//div[@class='inventory_item' and contains(.,'${product_name}')]//button
    JS Click Element    ${btn}

Get Cart Badge Count
    [Documentation]    Return cart badge number, or 0 if not visible.
    ${visible}=    Run Keyword And Return Status
    ...    Element Should Be Visible    css=.shopping_cart_badge
    IF    ${visible}
        ${text}=    Get Text    css=.shopping_cart_badge
        ${count}=    Convert To Integer    ${text}
        RETURN    ${count}
    END
    RETURN    ${0}

Sort Inventory By
    [Documentation]    Select a sort option by visible text.
    [Arguments]    ${option}
    Select From List By Label    css=[data-test="product-sort-container"]    ${option}

Go To Cart
    [Documentation]    Click the cart link and wait for cart page.
    JS Click Element    css=.shopping_cart_link
    Wait Until Element Is Visible    css=[data-test="checkout"]    timeout=${TIMEOUT}

Inventory Should Be Loaded
    [Documentation]    Verify the inventory page title.
    Wait Until Page Contains    Products    timeout=${TIMEOUT}
