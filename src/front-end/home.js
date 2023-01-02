$(document).ready(function () {
  // This function will be executed when the document is ready

  // get recent posts from the server
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/api/v1/recent",
    success: function (response) {
      // This function will be executed if the request succeeds
      let obj = Object.values(response.msg);

      // Loop through all cards and add postId attribute
      let num = 0;
      $(".card").each(function () {
        let postId = obj[num].postId;
        $(this).attr("postId", postId);
        num += 1;
      });

      // Loop through all the cards and fill the category
      num = 0;
      $(".card h5").each(function () {
        let category = obj[num].category;
        $(this).text(category);
        num += 1;
      });

      // Loop through all the cards and fill the title
      num = 0;
      $(".card p").each(function () {
        let desc = obj[num].title;
        $(this).text(desc);
        num += 1;
      });

      // Loop through all the cards and fill the time
      num = 0;
      $(".card #duration").each(function () {
        let duraton = obj[num].duration;
        $(this).text(duraton);
        num += 1;
      });

      // Add a "Read More" button to the card when the user hovers over it
      $(".card").hover(
        function () {
          $(this)
            .find(".card-footer")
            .append(
              '<button class="btn btn-primary" id="Read">Read More</button>'
            );
        },
        function () {
          // Remove the button when the user moves the mouse away from the card
          $(this).find("#Read").remove();
        }
      );
    },
    error: function () {
      // This function will be executed if the request fails
      // do something
    },
  });

  // Add a click event handler for the "Read More" button
  $(document).on("click", "#Read", function () {
    let card = $(this).closest(".card");
    let postId = card.attr("postId");
    let userId = 2;
    window.location.href = "post.html?postId=" + postId + "&userId=" + userId;
  });
});
