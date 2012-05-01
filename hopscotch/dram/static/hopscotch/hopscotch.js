/*

The HopScotch Master JS Library.

v 0.0.1 prototype

This library controls the feeds, checkins and cellar view of the Hopscotch app.

Requires:
    zepto.js (lightweight jquery port)
    underscore.js
    backbone.js
    bootstrap.js (for forms)

License: MIT (http://www.opensource.org/licenses/MIT)

*/

// TODO: Enable this function
// (function(){

//  // Set up intial variables


// }).call(this);

/*

Model out Drink classes

*/

// HopScotch = (function(){

var Drink = Backbone.Model.extend({
    age: Number,
    created_by_user: Number,
    drink_id: String,
    drink_type: String,
    enjoying: Boolean,
    id: String,
    maker: String,
    maker_type: String,
    manu_desc: String,
    name: String,
    own: Boolean,
    personal_desc: String,
    rating: Number,
    release_date: Date,
    resource_uri: String,
    schema: {
        name: {},
        maker: {},
        personal_desc: {},
        manu_desc: {},
        drink_type: {type: "Select", options: ["Whiskey","Scotch","Beer","Wine"]},
        enjoying: { type: "Checkbox" },
        own: { type: "Checkbox" }
        // rating: { type: "Radio", options: [1,2,3,4,5], editorClass: "rating" }
        // age: {}
        // release_date: {}
    }
})

var drink = new Drink();

var form = new Backbone.Form({
    model: drink
}).render();

function render_drink(){
    $('#checkin_form').prepend(form.el);
    return('Success');
}

//render_drink();

function create_drink() {
    form.commit();
    $.ajax({
        type: 'POST',
        url: '/api/v1/drink/',
        data: JSON.stringify(form.getValue()),
        // success: console.log('success'),
        // error: function(err){console.log(err['responseText'])},
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });
}

function checkin_drink(data){
       $.ajax({
        type: 'POST',
        url: '/api/v1/userdrink/',
        data: JSON.stringify(data),
        dataType: "application/json",
        processData:  false,
        error: function(err){console.log(err)},
        contentType: "application/json"
    }); 
}

function search_drinks() {
    var search_params = $('#search input').val()
    $.getJSON('/api/v1/drink/?format=json' + '&' + 'name__icontains=' + search_params)
    .success(function(data){ search_results(data) });

}
function search_drinks_by_user(user_id) {
    $.getJSON('/api/v1/userdrink/?format=json' + '&' + 'user_id__in=' + user_id)
    .success(function(data){ search_results_user(data) }).error(function(err){ console.log(err); });

}

function pr(tagname, value){
    // Prints item to HTML
    return("<" + tagname + ">" + value + "</" + tagname + ">")
}
function pr_checkbox(label, bool) {
    var checked = 'checked';
    
    if (bool !== true) {
        checked = '';
    }
    return('<div class="control-group">' + 
            '<label class="control-label" for="' + label + '"><strong>I ' + label + '</strong></label>' +
            '<div class="controls">' +
            '<input type="checkbox" disabled name="' + label + '" '+ checked + ' />' + 
            '</div></div>')
    
}

function search_results(data) {
    $('.search_results').html('');
    $.each(data['objects'],function(key, value){
        html_list = [
            '<div id="' +value['id'] +'" class="drink">',
            pr('h2', value['name']),
            pr('p', value['maker']),
            pr_checkbox('Own ', value['own']),
            pr_checkbox('Enjoyed ', value['enjoying']),
            pr('p class="rating"', value['rating'])
        ]
        if (value["personal_desc"] !== null) {
            html_list.push(pr('div  class="personal_desc"', "<strong>My notes</strong>" + pr('p', value['personal_desc'])));
        }
        if (value["manu_desc"] !== null) {
            html_list.push(pr('div class="manu_desc"', "<strong>Maker's description</strong>" + pr('p', value['manu_desc'])));
        }
        html = html_list.join("");
        html += "</div>"
        $('.search_results').append(html);
        
    })
    $('.drink').click(function(){
        checkin(this);
    });
}

function search_results_user(data) {
    $('.search_results').html('');
    $.each(data['objects'],function(key, value){
        html_list = [
            '<div id="' +value['drink_id']+ '" class="drink">',
            pr('h2', value['drink']['name']),
            pr('p', value['drink']['maker']),
            pr_checkbox('Own ', value['own']),
            pr_checkbox('Enjoyed ', value['enjoying']),
            pr('p class="rating"', value['rating'])
        ]
        if (value["personal_desc"] !== null) {
            html_list.push(pr('div  class="personal_desc"', "<strong>My notes</strong>" + pr('p', value['personal_desc'])));
        }
        if (value["drink"]["manu_desc"] !== null) {
            html_list.push(pr('div class="manu_desc"', "<strong>Maker's description</strong>" + pr('p', value['manu_desc'])));
        }
        html = html_list.join("");
        html += "</div>"
        $('.search_results').append(html);
        
    })
    $('.drink').click(function(){
        checkin(this);
    });
}

function checkin(obj) {
    
    function get_checkin_info() {
        return({
            'personal_desc': $('#tasting-notes').val(),
            'rating': $('.rating-radio:checked').val()
        })
    }
    function set_rating(value) {
        $('.rating-radio[value="' + value + '"]').attr('checked',true);
    }

    checkin_obj = {
        // 'object_id': $(obj).attr('id'),
        // 'drink_id': $(obj).attr('drink_id'),
        'drink_id': $(obj).attr('id'),
        'user_id': user_id
    }
    console.log(obj)
    $('.modal-header h3').html("Check in to " + $(obj).find('h2').html());
    $('#tasting-notes').val($(obj).find('.personal_desc p').html());
    set_rating($(obj).find('.rating').html())
    
    $('#checkinmodal').modal('show');
    $('.btn-checkin').click(function(){
        _.extend(checkin_obj, get_checkin_info());
        _.extend(checkin_obj, { enjoying: true });
        checkin_drink(checkin_obj);
        $('#checkinmodal').modal('hide');
    });
    $('.btn-cabinet').click(function(){
        _.extend(checkin_obj, get_checkin_info());
        _.extend(checkin_obj, { own: true });
        checkin_drink(checkin_obj);
        $('#checkinmodal').modal('hide');
    });

}

$('#checkinmodal').modal();
$('#checkinmodal').modal('hide');

// Buttons
$('#submit').click(function(){
    create_drink();
});
$('#search button').click(function(){
    search_drinks();
});


// }).call(this);
// function checkin() {
//  //Check in to a drink
    

// }