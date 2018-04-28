$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_id").val(res.promotion_id);
        $("#promotion_name").val(res.name);
        $("#promotion_product_id").val(res.product_id);
        $("#promotion_discount_ratio").val(res.discount_ratio);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_name").val("");
        $("#promotion_product_id").val("");
        $("#promotion_discount_ratio").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function clear_list() {
        $("#flash_message").empty();
        $("#search_results").empty();
    }

    function list_one_promotion(res) {
        $("#search_results").empty();
        $("#search_results").append('<table class="table-striped">');
        var header = '<tr>'
        header += '<th style="width:10%">ID</th>'
        header += '<th style="width:40%">Name</th>'
        header += '<th style="width:10%">Product</th>'
        header += '<th style="width:10%">Discount</th>'
        header += '<th style="width:10%">Counter</th></tr>'
        $("#search_results").append(header);
        var row = "<tr><td>"+res.promotion_id+"</td><td>"+res.name+"</td><td>"+res.product_id+"</td><td>"+res.discount_ratio+"</td><td>"+res.counter+"</td></tr>";
        $("#search_results").append(row);
        $("#search_results").append('</table>');
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#promotion_name").val();
        var product_id = $("#promotion_product_id").val();
        var discount_ratio = $("#promotion_discount_ratio").val();

        var data = {
            "name": name,
            "product_id": parseInt(product_id),
            "discount_ratio": parseInt(discount_ratio)
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
            list_one_promotion(res)
        });

        ajax.fail(function(res){
            clear_list()
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        var promotion_id = $("#promotion_id").val();
        var name = $("#promotion_name").val();
        var product_id = $("#promotion_product_id").val();
        var discount_ratio = $("#promotion_discount_ratio").val();

        var data = {}
        if (name) {
            data.name = name
        }
        if  (product_id) {
            data.product_id = parseInt(product_id)
        }
        if  (discount_ratio) {
            data.discount_ratio = parseInt(discount_ratio)
        }

        var ajax = $.ajax({
                type: "PUT",
                url: "/promotions/" + promotion_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
            list_one_promotion(res)
        });

        ajax.fail(function(res){
            clear_list()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        var promotion_id = $("#promotion_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/promotions/" + promotion_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
            list_one_promotion(res)
        });

        ajax.fail(function(res){
            clear_form_data()
            clear_list()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Redeem a Promotion
    // ****************************************

    $("#redeem-btn").click(function () {

        var promotion_id = $("#promotion_id").val();

        var ajax = $.ajax({
            type: "POST",
            url: "/promotions/" + promotion_id + "/redeem",
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            list_one_promotion(res)
        });

        ajax.fail(function(res){
            clear_form_data()
            clear_list()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        var promotion_id = $("#promotion_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/promotions/" + promotion_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(){
            clear_form_data()
            clear_list()
            flash_message("Promotion with ID [" + promotion_id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            clear_list()
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the Promotion
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promotion_id").val("");
        clear_form_data()
        clear_list()
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {

      var name = $("#promotion_name").val();
      var product_id = $("#promotion_product_id").val();
      var discount_ratio = $("#promotion_discount_ratio").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (product_id) {
            if (queryString.length > 0) {
                queryString += '&product_id=' + product_id
            } else {
                queryString += 'product_id=' + product_id
            }
        }
        if (discount_ratio) {
            if (queryString.length > 0) {
                queryString += '&discount_ratio=' + discount_ratio
            } else {
                queryString += 'discount_ratio=' + discount_ratio
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/promotions?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:10%">Product</th>'
            header += '<th style="width:10%">Discount</th>'
            header += '<th style="width:10%">Counter</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                promotion = res[i];
                var row = "<tr><td>"+promotion.promotion_id+"</td><td>"+promotion.name+"</td><td>"+promotion.product_id+"</td><td>"+promotion.discount_ratio+"</td><td>"+promotion.counter+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_list()
            flash_message(res.responseJSON.message)
        });

    });

})
