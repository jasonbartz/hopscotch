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
// Assign the Library variable to `this` (root)
var HopScotch = root.HopScotch = {};

// Set defaults, including version and base settings
HopScotch.__version__ = '0.1.0';

// Uses Jquery by default
var $ = root.jQuery;
var _ = root._;
var debug = true;

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
};

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

    this.search = function(search_parameter_string, resource) {
        $.ajax({
            type: 'GET',
            url: '/api/' + this.defaults.version + '/' + resource + '/?' + search_parameter_string,
            async: false,
            error: function(data){
                search_root.results = JSON.parse(data.responseText);
                if (data['statusText'] === 'OK') {
                    this.results = data;
                } else {
                    HopScotch.Error.on(search_root.defaults.error_div,
                                      'An error occured.');
                }
            },
            dataType: "application/json",
            processData:  false,
            contentType: "application/json"
        });
    };
};

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
    var checkin_root = this;

    this.defaults = { version: 'v1', error_div: '#content'},
    this.response = {},
    this.complete = null,
    this.response_code = null,
    this.response_message = '',

    this.send = function(resource, data_obj, http_type, status_ok) {
        _.once($.ajax({
            type: http_type,
            url: '/api/' + checkin_root.defaults.version +
                 '/'+ resource +'/',
            data: JSON.stringify(data_obj),
            complete: function(data) {
                checkin_root.complete(checkin_root);
            },
            error: function(err){
                if (err['status'] === status_ok) {
                    checkin_root.response = data_obj;
                } else if (err.status >= 500){
                    if (debug === true) {
                        HopScotch.Error.on(checkin_root.defaults.error_div,
                                      'Debug: ' + err['statusText'] + '<br />' + err['responseText']);
                    } else {
                        HopScotch.Error.on(checkin_root.defaults.error_div,
                                      'An error occured.');
                    }
                }
               checkin_root.response_code = err.status;
               checkin_root.response_message = err.responseText;

             },
            dataType: "application/json",
            processData:  false,
            contentType: "application/json"
        }));
    },
    this.create = function(data) {

        // Parse Age
        data.age = parseInt(data.age);

        // Parse Date
        if (data.release_date === "") {
            data.release_date = null;
        } else {
            data.release_date = new Date(data.release_date);
        }

        checkin_root.send('drink', data, 'POST', 201);
    },
    this.checkin = function(data) {
        checkin_root.send('checkin', data, 'POST', 201);
    },
    this.edit = function(data) {
        checkin_root.send('checkin', data, 'PATCH', 202);
    },
    this.delete = function(data) {
        checkin_root.send('checkin', data, 'DELETE', 204);
    };
};

// TODO: Replace with underscore.js templates
var Display = HopScotch.Display = {
    /* Checkin Object

    For manipulating the DOM and adding things to the page

    Available Methods:

    Static:

    :: defaults

    */
    to_html: function (tagname, value, classes){
    // Prints item to HTML
        return("<" + tagname + " class='" + classes + "'>" + value + "</" + tagname + ">");
    }
};

// var Drink = HopScotch.Drink = Backbone.Model.extend({
//     schema: {
//         name: { },
//         maker: {},
//         manu_desc: {title: "Maker's description"},
//         drink_type: {type: "Select", options: ["Whiskey","Scotch","Beer","Wine"],title: "Type of drink"},
//         age: {},
//         release_date: {title: "Release date"},
//         rating: {type: "Radio", options: [1,2,3,4,5]},
//         personal_desc: {title: "My description"}
//     }
// });

}).call(this);

