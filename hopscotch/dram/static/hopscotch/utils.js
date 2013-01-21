var is_closed = false;

if (_.contains(document.cookie.split('; '), "hopscotch_beta_header_closed=true")) {
    is_closed = true;
    $(".beta-header").hide();
}

$(".beta-header .beta-close").click(function(){
    if (is_closed === false){
        $(".beta-header").hide();
        document.cookie = "hopscotch_beta_header_closed=true; ";
    }
});