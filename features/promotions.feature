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
    And I should not see "404 Success Found"
    And I should not see "NewPromotionToCreate" in the results

Scenario: Create a Promotion with Bad Discount_Ratio
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I set the "Name" to "NewPromotionToCreate"
    And I set the "Product_Id" to "9999"
    And I set the "Discount_Ratio" to "111"
    When I press the "Create" button
    Then I should see the message "Invalid promotion"
    And I should not see "404 Success Found"
    And I should not see "NewPromotionToCreate" in the results

##################################
#             Redeem             #
##################################

Scenario: Redeem a Promotion
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "0" in the results
    When I press the "Redeem" button
    Then I should see the message "Success"
    And I should see "1" in the results
    When I press the "Redeem" button
    Then I should see the message "Success"
    And I should see "2" in the results
    When I press the "Redeem" button
    Then I should see the message "Success"
    And I should see "3" in the results
    When I press the "Redeem" button
    Then I should see the message "Success"
    And I should see "4" in the results
    When I press the "Redeem" button
    Then I should see the message "Success"
    And I should see "5" in the results
