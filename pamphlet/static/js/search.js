$(function() {
    var isClicked = getParameterByName('clicked');  // Load the query string specified by the previous page's link
    if(isClicked) {
        var keyword = getParameterByName('keyword');
        $('#search-keyword-input').attr('value', keyword)
        $("#search-btn").trigger('click')
        console.log(keyword)
    } else {
    } // end if/else
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function getParameterByName(name) 
{
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


$("#search-btn").on('click',function(e){
    var form = $("#search-bar-form")
    var actionUrl = form.attr('action')

    $.ajax(
        {
            type:"POST",
            url:actionUrl,
            data:form.serialize(),
            success:function(data){
                console.log(data)
                display_serach_result(data)
                loadStatusAvatar($('#search-result-container'))
            },
            error:function(result){
                console.log(result.responseText)
            }

        }
    )
})
function toUserProfilePage(user_id){
    console.log('exe')
    window.location.href="/user/"+user_id
}



