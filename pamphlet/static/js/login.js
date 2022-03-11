
$("#login-form").on('submit',function(e){
    e.preventDefault()
    var form = $(this)
    var actionUrl = form.attr('action')
    console.log("called")
    $.ajax(
        {
            type:"POST",
            url:actionUrl,
            data:form.serialize(),
            success:function(data){
                window.location.href="/"
            },
            error:function(result){
                alert(result.responseText)
            }

        }
    )
})