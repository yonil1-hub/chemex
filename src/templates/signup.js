// function matchPassword() {
//   let pw1 = document.getElementById("passowrd").value;
//   let pw2 = document.getElementsByClassName("comfrim").value;
//   console.log(pw1, pw2);
// }
$(function () {
  $("form").submit(function (event) {
    $.ajax({
      data: {
        firstName: $("#firstName").val(),
        lastName: $("#lastName").val(),
        email: $("#email").val(),
        username: $("#username").val(),
        password: $("#password").val(),
      },
      type: "POST",
      url: "http://127.0.0.1:5000/api/v1/auth/signup",
      headers: { "Content-Type": "application/json " },

      error: function (e) {
        console.log(e);
      },
    });
    event.preventDefault();
  });
});
