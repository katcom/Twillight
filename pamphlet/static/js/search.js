
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


