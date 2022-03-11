
$("#register-form").on('submit',function(e){
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
                alert(data)
            },
            error:function(result){
                alert(result.responseText)
            }

        }
    )
})