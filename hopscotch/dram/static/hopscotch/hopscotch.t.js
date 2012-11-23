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
        name: { },
        maker: {},
        manu_desc: {title: "Maker's description"},
        drink_type: {type: "Select", options: ["Whiskey","Scotch","Beer","Wine"],title: "Type of drink"},
        age: {},
        release_date: {title: "Release date"},
        rating: {type: "Radio", options: [1,2,3,4,5]},
        personal_desc: {title: "My description"}
    }
})


function error(err) {
    $('#content').prepend('<div class="alert alert-error">Something went wrong, here.</div>');
}

function drink_hover_on(obj) {
    $(obj).append('<a class="drink-edit" href="javascript: void(0);"><span class="label label-info">Edit</span></a>');

    defaults = {
        'personal_desc': $(obj).find('.personal_desc p').html(),
        'rating': $(obj).find('.rating-star-container p').length
    }


    var form = new Backbone.Form({
        schema: {
            rating: {type: "Radio", options: [1,2,3,4,5]},
            personal_desc: {title: "My description"}
        },
        data: defaults,
    }).render();

    $('#checkin_form').prepend(form.el);

    $('.drink-edit').click(function(){
        $('#editmodal').modal();
        $('#editmodal .modal-body .bbf-form').remove();
        $('#editmodal').css('display','block');
        $('#editmodal .modal-body').append(form.el);

        $('#editmodal .btn.edit-delete').click(function(){
            delete_checkin($(obj).attr('id'));
            $('#editmodal').modal('hide');
        });
        $('#editmodal .btn.edit-edit').click(function(){
            data = {
                'rating': parseInt($('#editmodal .bbf-form :checked').val()),
                'personal_desc': $('#editmodal #personal_desc').val()
            }
            edit_checkin($(obj).attr('id'), data);
        });
    });


}
function drink_hover_off(obj) {
    $('.drink-edit').remove();
}

function drink_hover(){
    $('.drink-checkin').hover(
        function(){
            drink_hover_on($(this));
        },
        function() {
            drink_hover_off($(this));
        }
    );
}

function delete_checkin(obj_id) {
        $.ajax({
        type: 'DELETE',
        url: '/api/v1/checkin/' + obj_id,
        error: function(err){
            if (err['status'] === 204) {
                $('#content').prepend('<div class="alert alert-success">Checkin removed.</div>');
                location.reload(true);
            } else {
                error(err);
            }
        },
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });
}
function edit_checkin(obj_id) {
        $.ajax({
        type: 'PATCH',
        url: '/api/v1/checkin/' + obj_id,
        data: JSON.stringify(data),
        error: function(err){
            if (err['status'] === 202) {
                $('#content').prepend('<div class="alert alert-success">Checkin Updated.</div>');
                location.reload(true);
            } else {
                error(err);
            }
        },
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });
}

function create_drink(type_of_enjoyment) {
    form.commit();
    create_drink_obj = form.getValue();
    checkin_obj = {
        'rating': create_drink_obj.rating,
        'personal_desc': create_drink_obj.personal_desc,
        'user_id': user_id,
    }
    create_drink_obj.created_by_user = user_id;
    delete create_drink_obj.rating;
    delete create_drink_obj.personal_desc;
    create_drink_obj.age = parseInt(create_drink_obj.age);

    if (create_drink_obj.release_date === "") {
        create_drink_obj.release_date = null
    } else {
        create_drink_obj.release_date = new Date(create_drink_obj.release_date)
    }


    $.ajax({
        type: 'POST',
        url: '/api/v1/drink/',
        data: JSON.stringify(create_drink_obj),
        error: function(err){
            if (err['status'] === 201) {
                response_json = JSON.parse(err['responseText']);
                checkin_obj.drink_id = response_json.id
                if (type_of_enjoyment === 'enjoying') {
                    checkin_obj.enjoying = true;
                } else if (type_of_enjoyment === 'own') {
                    checkin_obj.own = true;
                }
                checkin_drink(checkin_obj)
            } else {
                error(err);
            }
        },
        dataType: "application/json",
        processData:  false,
        contentType: "application/json"
    });
}

function checkin_drink(data){
       $.ajax({
        type: 'POST',
        url: '/api/v1/checkin/',
        data: JSON.stringify(data),
        dataType: "application/json",
        processData:  false,
        error: function(err){
            if (err['status'] === 201) {
                window.location.href = "/user/"+ username;

            } else {
                error(err);
            }
        },
        contentType: "application/json"
    });
}

function search_drinks() {
    var search_params = $('#search input').val()
    $.getJSON('/api/v1/drink/?format=json' + '&' + 'name__icontains=' + search_params)
    .success(function(data){ search_results(data) });

}
function search_drinks_by_user(user_id, page) {
    $.getJSON('/api/v1/checkin/?format=json&user_id=' + user_id + '&' + page + '=true')
        .success(function(data){ search_results_user(data, page) })
        .error(function(err){ console.log(err); });
}

function pr(tagname, value, classes){
    // Prints item to HTML
    return("<" + tagname + " class='" + classes + "'>" + value + "</" + tagname + ">")
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
            '<div id="' +value['id']+ '" class="drink span4">',
            pr('h2', value['name'],'drink-name'),
            pr('p', value['maker'], 'drink-maker'),
        ]
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
    drink_hover();
}

function search_results_user(data, div) {
    $('.search_results_' + div).html('');
    $.each(data['objects'],function(key, value){
        html_list = [
            '<div id="' +value['id']+ '" class="drink drink-checkin span4">',
            pr('h2', value['drink']['name'],'drink-name'),
            pr('p', value['drink']['maker'], 'drink-maker'),
        ]
        html_list.push('<div class="rating-star-container">')
        if (value['rating'] !== null) {
            rating = parseInt(value['rating']);
            _.each(_.range(rating), function(key) {
                html_list.push(pr('p', '', 'rating-star'))
            });

        }
        html_list.push("</div>")
        if (value["personal_desc"] !== null) {
            html_list.push(pr('div  class="personal_desc"', "<strong>My notes</strong>" + pr('p', value['personal_desc'])));
        }
        if (value["drink"]["manu_desc"] !== null) {
            html_list.push(pr('div class="manu_desc"', "<strong>Maker's description</strong>" + pr('p', value["drink"]['manu_desc'])));
        }
        html = html_list.join("");
        html += "</div>"
        $('.search_results_'+div).append(html);
        drink_hover();
    })
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
        'drink_id': $(obj).attr('id'),
        'user_id': user_id
    }
    console.log(obj)
    $('.modal-header h3').html("Check in to " + $(obj).find('h2').html());
    $('#tasting-notes').val($(obj).find('.personal_desc p').html());
    set_rating($(obj).find('.rating').html())
    $('#checkinmodal').css('display','block');
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
