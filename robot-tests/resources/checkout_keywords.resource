*** Settings ***
Resource    common.resource

*** Keywords ***
Fill Checkout Info
    [Documentation]    Fill in all three checkout fields.
    [Arguments]    ${first}    ${last}    ${postal}
    Input Text    css=[data-test="firstName"]    ${first}
    Input Text    css=[data-test="lastName"]    ${last}
    Input Text    css=[data-test="postalCode"]    ${postal}

Click Continue
    [Documentation]    Click Continue button on checkout Step One.
    JS Click Element    css=[data-test="continue"]

Click Finish
    [Documentation]    Click Finish button on checkout Step Two.
    JS Click Element    css=[data-test="finish"]
    Wait Until Element Is Visible    css=.complete-header    timeout=${TIMEOUT}

Click Back Home
    [Documentation]    Click Back Home on the confirmation page.
    JS Click Element    css=[data-test="back-to-products"]

Get Checkout Error Text
    [Documentation]    Return the error message text from Step One.
    Wait Until Element Is Visible    css=[data-test="error"]    timeout=${TIMEOUT}
    ${error}=    Get Text    css=[data-test="error"]
    RETURN    ${error}

Get Order Total Text
    [Documentation]    Return the order total label text.
    Wait Until Element Is Visible    css=.summary_total_label    timeout=${TIMEOUT}
    ${total}=    Get Text    css=.summary_total_label
    RETURN    ${total}

Get Checkout Item Count
    [Documentation]    Return number of items on the overview page.
    ${items}=    Get WebElements    css=.cart_item
    ${count}=    Get Length    ${items}
    RETURN    ${count}

Get Confirmation Header
    [Documentation]    Return the complete-header text.
    ${text}=    Get Text    css=.complete-header
    RETURN    ${text}

Cancel Checkout
    [Documentation]    Click Cancel on checkout form.
    JS Click Element    css=[data-test="cancel"]
