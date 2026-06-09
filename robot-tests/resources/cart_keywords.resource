*** Settings ***
Resource    common.resource

*** Keywords ***
Get Cart Item Count
    [Documentation]    Return the number of items in the cart.
    ${items}=    Get WebElements    css=.cart_item
    ${count}=    Get Length    ${items}
    RETURN    ${count}

Get Cart Item Names
    [Documentation]    Return names of items in the cart.
    ${elements}=    Get WebElements    css=.cart_item .inventory_item_name
    ${names}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        Append To List    ${names}    ${text}
    END
    RETURN    ${names}

Remove Item From Cart
    [Documentation]    Click Remove on the cart item matching ${product_name}.
    [Arguments]    ${product_name}
    ${btn}=    Get WebElement
    ...    xpath=//div[@class='cart_item' and contains(.,'${product_name}')]//button
    Click Button    ${btn}

Cart Should Be Loaded
    [Documentation]    Verify the checkout button is visible.
    Wait Until Element Is Visible    css=[data-test="checkout"]    timeout=${TIMEOUT}

Click Continue Shopping
    [Documentation]    Click Continue Shopping to return to Inventory.
    Click Element    css=[data-test="continue-shopping"]

Click Checkout
    [Documentation]    Click the Checkout button to proceed.
    Click Element    css=[data-test="checkout"]
    Wait Until Element Is Visible    css=[data-test="firstName"]    timeout=${TIMEOUT}

Go To Cart Page
    [Documentation]    Navigate directly to cart URL.
    Go To    ${CART_URL}
    Wait Until Element Is Visible    css=[data-test="checkout"]    timeout=${TIMEOUT}
