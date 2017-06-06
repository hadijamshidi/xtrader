/**
 * Created by hadi on 11/22/16.
 */


var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
// $('#frm').submit(function(e){
//     alert('run');
//     e.preventDefault();
// });

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};
function activate(idd) {
    var ids = ['sign_in', 'sign_up'];
    ids.forEach(function (i) {
        if (i != idd) {
            document.getElementById(i+'_container').setAttribute('style', 'main: none');
        } else {
            document.getElementById(i+'_container').setAttribute('style', 'main: block');

        }
        if (i != idd) {
            document.getElementById(i).setAttribute('class', 'item');
            document.getElementById(i).setAttribute('style', 'cursor:pointer');
        } else {
            document.getElementById(i).setAttribute('class', 'active item');
            document.getElementById(i).setAttribute('style', 'cursor:default');

        }
    });
}

var menus = ['our_company','about_us','contact_us'];

function sign_up(){
    console.log('sign');
    var ids = ['Fname','Lname','Uname','email','Upass'];
    var form = {};
    ids.forEach(function(id){
        form[id] = document.getElementById(id).value;
    });
    console.log(form);
    $.ajax({
        type: 'POST',
        url: "/sign-up",
        data: {
            param: JSON.stringify(form),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (result) {
            result = JSON.parse(result);
            console.log(result);
        }
    })

}
function login(){
    var name = document.getElementById('uname').value;
    var psw = document.getElementById('psw').value;
    var user = {'name':name,'pass':psw};
    $.ajax({
        type: 'POST',
        url: "/login",
        data: {
            param: JSON.stringify(user),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (result) {
            result = JSON.parse(result);
            console.log(result);
        }
    })

}
