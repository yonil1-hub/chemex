$(document).ready(function () {
  //handle homepage

  // get recent posts
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/api/v1/recent",
    success: function (response) {
      let obj = Object.values(response.msg);

      //fill all the titles
      let num = 0;
      $(".card h5").each(function () {
        let category = obj[num].category;
        $(this).text(category);
        num += 1;
      });
      // fill the descriptions
      num = 0;
      $(".card p").each(function () {
        let desc = obj[num].description;
        $(this).text(desc);
        num += 1;
      });
    },
  });
  // $("#readmore1").click(function (e) {
  //   e.preventDefault();
  //   postId = 16;
  //   userId = 1;
  //   window.location.href = "post.html?postId=" + postId + "&userId=" + userId;
  // });
});
