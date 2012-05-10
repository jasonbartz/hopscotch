/*

The HopScotch Master JS Library.

v 0.1.0 beta

This library controls the feeds, checkins and cellar view of the hpsct.ch app.

Requires:
    jquery
    underscore.js
    backbone.js
    bootstrap.js (for forms)

License: MIT (http://www.opensource.org/licenses/MIT)

*/

(function(){

// Assign `this` to root, so it can be called if necessary
var root = this;

// Create the initial Library variable that will store all of our methods.
var HopScotch;

// Assign the Library variable to `this` (root)
var HopScotch = root.HopScotch = {};

// Set defaults, including version and base settings
HopScotch.__version__ = '0.1.0';

// Uses Jquery by default
var $ = root.jQuery;

var Error = HopScotch.Error = {
    /* Error Reporting Object

    Available methods:

    :: on ("div to be added to", "error message")

    :: off ("div to remove error from")

    */
    on: function(div, msg) {
        $(div).prepend('<div class="alert alert-error">' + msg + '</div>');
        return(null);
    },
    off: function(div) {
        $(div + ' .alert').remove();
        return(null);
    }
}

var Search = HopScotch.Search = function(){
    /* Search Object

    For calling API and Search APIs and ingests JSON

    Available Methods:

    :: search (search_parameter_string)

    Static:

    :: defaults
        api version
        error_div
    */

    var search_root = this;
    
    this.defaults = { version: 'v1', error_div: '#content' },
    this.results = {},
    // this.search = function(search_parameter_string){
    //     $.getJSON('/api/' + this.defaults.version + 
    //                 '/drink/?format=json&' + 
    //                 search_parameter_string)
    //         .success(function(data){ 
    //             search_root.results = data;
    //         })
    //         .error(function(err){ 
    //             HopScotch.Error.on(this.defaults.error_div, 
    //                               'An error occured.')
    //     });
    // }
    this.search = function(search_parameter_string) {
        $.ajax({
            type: 'GET',
            url: '/api/' + this.defaults.version + '/drink/?format=json&' + search_parameter_string,
            async: false,
            error: function(data){
                search_root.results = JSON.parse(data.responseText);
                // if (err['status'] === status_ok) {
                //     this.results = data;
                // } else {
                //     HopScotch.Error.on(HopScotch.Search.defaults.error_div, 
                //                       'An error occured.')    
                // }
            },
            dataType: "application/json",
            processData:  false,
            contentType: "application/json"
        });
    }
}

var Checkin = HopScotch.Checkin = function(){
    /* Checkin Object

    For checking in and creating drinks

    Available Methods:


    :: send (resource, data, http type, status to be ok)
    :: create (data)
    :: checkin (data)
    :: edit (data)
    :: delete (data)
    
    Static:

    :: defaults
    
    */
    this.defaults = { version: 'v1' },
    this.response = {},
    this.send = function(resource, data_obj, http_type, status_ok) {
        $.ajax({
            type: http_type,
            url: '/api/' + HopScotch.Checkin.defaults.version + 
                 '/'+ resource +'/',
            data: JSON.stringify(data_obj),
            error: function(err){
                if (err['status'] === status_ok) {
                    HopScotch.Checkin.response = data;
                } else {
                    HopScotch.Error.on(HopScotch.Search.defaults.error_div, 
                                      'An error occured.')    
                }
            },
            dataType: "application/json",
            processData:  false,
            contentType: "application/json"
        });
    },
    this.create = function(data) {

        // Parse Age
        data.age = parseInt(data.age);

        // Parse Date
        if (data.release_date === "") {
            data.release_date = null    
        } else {
            data.release_date = new Date(data.release_date)    
        }

        HopScotch.Checkin.send('drink', data, 'POST', 201)
    },
    this.checkin = function(data) {
        HopScotch.Checkin.send('checkin', data, 'POST', 201)
    },
    this.edit = function(data) {
        HopScotch.Checkin.send('checkin', data, 'PATCH', 202)
    },
    this.delete = function(data) {
        HopScotch.Checkin.send('checkin', data, 'DELETE', 204)
    }
}

var Display = HopScotch.Display = {
    /* Checkin Object

    For manipulating the DOM and adding things to the page

    Available Methods:
    
    Static:

    :: defaults

    */
    to_html: function (tagname, value, classes){
    // Prints item to HTML
        return("<" + tagname + " class='" + classes + "'>" + value + "</" + tagname + ">")
    }
}

var Drink = HopScotch.Drink = Backbone.Model.extend({
    schema: {
        name: { },
        maker: {},
        manu_desc: {title: "Maker's description"},
        drink_type: {type: "Select", options: ["Whiskey","Scotch","Beer","Wine"],title: "Type of drink"},
        age: {},
        release_date: {title: "Release date"},
        rating: {type: "Radio", options: [1,2,3,4,5]},
        personal_desc: {title: "My description"}
    }
});

}).call(this);

