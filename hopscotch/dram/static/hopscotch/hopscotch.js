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

function search_drinks() {
    $.getJSON('/api/v1/drink/?format=json' + '&' + 'name__icontains=lagavulin')
    .success(function(data){ search_results(data) });
}

function search_results(data) {
    
    $.each(data['objects'],function(key, value){
        drink_obj = new Drink(value);
        var DrinkView = Backbone.View.extend({
            model: drink_obj,
        });
        view_instance = new DrinkView();
        console.log(view_instance);
        $('.search_results').html(view_instance.el);    
    })
    
}
// Buttons
$('#submit').click(function(){
    create_drink();
});
$('#search').click(function(){
    search_drinks();
});


// }).call(this);
// function checkin() {
//  //Check in to a drink
    

// }