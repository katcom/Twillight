
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

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

$('#header-search-btn').on('click',function(e){
    console.log('clickfukx')
    window.location.href=`/search-users/?clicked=true&keyword=${$('#header-search-input').val()}`
});


