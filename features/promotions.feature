Feature: The promotion service back-end
    As a Promotion Service Owner
    I need a RESTful API service
    So that I can keep track of all my promotions

Background:
    Given the following promotions
        | id | name         | product_id | discount_ratio |
        |  1 | BlackFriday  | 9999       | 99             |
        |  2 | July4th      | 1785       | 74             |
        |  3 | BackToSchool | 1831       | 80             |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotion Demo REST Service" in the title
    And I should not see "404 Not Found"


##################################
#             Create             #
##################################

Scenario: Create a Promotion
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I set the "Name" to "NewPromotionToCreate"
    And I set the "Product_Id" to "9999"
    And I set the "Discount_Ratio" to "99"
    When I press the "Create" button
    Then I should see the message "Success"
    And I should not see "404 Not Found"
    And I should see "NewPromotionToCreate" in the results

Scenario: Create a Promotion with Bad Product_Id
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I set the "Name" to "NewPromotionToCreate"
    And I set the "Product_Id" to "número uno"
    And I set the "Discount_Ratio" to "99"
    When I press the "Create" button
    Then I should see the message "Invalid promotion"
    And I should not see "404 Not Found"
    And I should not see "NewPromotionToCreate" in the results

Scenario: Create a Promotion with Bad Discount_Ratio
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I set the "Name" to "NewPromotionToCreate"
    And I set the "Product_Id" to "9999"
    And I set the "Discount_Ratio" to "111"
    When I press the "Create" button
    Then I should see the message "Invalid promotion"
    And I should not see "404 Not Found"
    And I should not see "NewPromotionToCreate" in the results


##################################
#             Delete             #
##################################

Scenario: Delete a Promotion
    When I visit the "Home Page"
    And I set the "Id" to "1"
    When I press the "Delete" button
    Then I should see the message "Promotion with ID [1] has been Deleted!"
    And I should not see "404 Not Found"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should not see "BlackFriday" in the results

Scenario: Delete a Promotion That Id Not Found
    When I visit the "Home Page"
    And I set the "Id" to "100"
    When I press the "Delete" button
    Then I should see the message "Promotion with ID [100] has been Deleted!"
    And I should not see "404 Not Found"

Scenario: Delete a Promotion That Wrong Id Type
    When I visit the "Home Page"
    And I set the "Id" to "a"
    When I press the "Delete" button
    Then I should see the message "Server error!"
    And I should not see "404 Not Found"

##################################
#             Redeem             #
##################################

Scenario: Redeem a Promotion
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "0" in the results
    When I press the "Redeem" button
    Then I should see "1" in the results
    And I should not see "0" in the results


##################################
#              List              #
##################################

Scenario: List all the Promotion
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "BlackFriday" in the results
    And I should see "July4th" in the results
    And I should see "BackToSchool" in the results

##################################
#             Query              #
##################################

Scenario: Query Promotions by Name
    When I visit the "Home Page"
    And I set the "Name" to "BlackFriday"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "BlackFriday" in the results
    And I should not see "BackToSchool" in the results

Scenario: Query Promotions by Product id
    When I visit the "Home Page"
    And I set the "Product_Id" to "9999"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "9999" in the results
    And I should not see "1831" in the results

Scenario: Query Promotions by Discount Ratio
    When I visit the "Home Page"
    And I set the "Discount_Ratio" to "74"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "74" in the results
    And I should not see "99" in the results

##################################
#             Update             #
##################################

Scenario: Update a Promotion with partial attribute
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "BlackFriday" in the "Name" field
    When I change "Name" to "WhiteFriday"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "WhiteFriday" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "WhiteFriday" in the results
    And I should not see "BlackFriday" in the results

Scenario: Update a Promotion with full attributes
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "BlackFriday" in the "Name" field
    When I change "Name" to "WhiteFriday"
    And I change "Product_Id" to "8888"
    And I change "Discount_Ratio" to "88"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "WhiteFriday" in the "Name" field
    And I should see "8888" in the "Product_Id" field
    And I should see "88" in the "Discount_Ratio" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "WhiteFriday" in the results
    And I should see "8888" in the results
    And I should see "88" in the results
    And I should not see "BlackFriday" in the results
    And I should not see "9999" in the results
    And I should not see "99" in the results

Scenario: Update a Promotion with discount ratio out of range
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "99" in the "Discount_Ratio" field
    When I change "Discount_Ratio" to "111"
    And I press the "Update" button
    Then I should see the message "Invalid promotion"
    And I should not see "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "99" in the "Discount_Ratio" field
    And I should not see "111" in the results

Scenario: Update a Promotion with wrong value type
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "9999" in the "Product_Id" field
    When I change "Product_Id" to "str"
    And I press the "Update" button
    Then I should see the message "Invalid promotion"
    And I should not see "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "9999" in the "Product_Id" field
    And I should not see "str" in the results

##################################
#             Read               #
##################################

Scenario: Retrive an existing Promotion by promotion ID
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "BlackFriday" in the "name" field
    And I should see "9999" in the "Product_Id" field
    And I should see "99" in the "discount_ratio" field
    Then I should see the message "Success"

Scenario: Retrive an non-existing Promotion by promotion ID
    When I visit the "Home Page"
    And I set the "Id" to "999"
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: Retrive an Promotion attribute other than promotion ID
    When I visit the "Home Page"
    And I set the "Name" to "BlackFriday"
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"
    When I visit the "Home Page"
    And I set the "Product_ID" to "9999"
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"
    When I visit the "Home Page"
    And I set the "Discount_Ratio" to "80"
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"
