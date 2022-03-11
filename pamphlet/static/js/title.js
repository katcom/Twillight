$("#logout-button").on('click',function(e){
    e.preventDefault()

    $.ajax({
        type:'GET',
        url:"/api/logout/",
        success:function(data){
            alert("You have logged out.")
            window.location.href="/"
        },
        error:function(result){
            alert(result.responseText)
        }

    })
})