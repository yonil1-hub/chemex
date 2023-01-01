$(document).ready(function () {
  //function that applies replies
  function appnedReplies(replies) {
    $.each(replies, function (index, reply) {
      $("#allcomments").append(`
      <div class="reply hidden">
        <p class="text">${reply.body}
        </p>
        <hr/>
        <small class="meta">Posted by ${reply.user}, ${reply.duration}</small>
      </div>
      `);
    });
  }
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/api/v1/post/16",
    // handle success
    success: function (response) {
      let postinfo = response.msg["post_info"];
      let userinfo = response.msg["user_info"];
      let commentinfo = response.msg["comment_info"];
      $("#post_title1").text(postinfo.title);
      $("#post_title2").text(postinfo.title);
      $("#author").text(userinfo.username);
      $("#category").text(postinfo.category);
      $("#duration").text(postinfo.duration);
      $(".body").html(postinfo.body);
      $("#noOfLikes").text(postinfo.likes);

      // handle comments
      let comments = Object.values(commentinfo);
      if (comments.length === 0) {
        $("#commentContainer").hide();
      } else {
        $.each(comments, function (index, value) {
          $("#allcomments").append(`
  <div class="comment">
    <p class="text">${value.body}
    </p>
    <hr/>
    <small class="meta">Posted by ${value.user}, ${value.duration}</small>
    <button class="btn btn-primary btn-sm reply-button">Reply</button>
    <button class="btn btn-primary btn-sm showrepliesbtn">
      Show Replies
    </button>
  </div>
`);
          if (value.replies) {
            appnedReplies(value.replies);
          }
        });
      }
    },

    // error handling
    error: function (response) {
      alert("Nooooo");
    },
  });

  // handle the clapping_hands
  $("#clapping_icon").click(function () {
    if ($(this).hasClass("liked")) {
      $(this).removeClass("liked");
      //update database
      let data = { data: "dislike" };
      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/v1/handle/likes/8",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success: function (response) {
          //update the post
          $("#noOfLikes").text(parseInt($("#noOfLikes").text()) - 1);
        },
        error: function (response) {
          console.log(response.responseJSON.msg);
        },
      });
    } else {
      $(this).addClass("liked");
      // update the database
      let data = { data: "like" };
      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/v1/handle/likes/8",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success: function (response) {
          //update the post
          $("#noOfLikes").text(parseInt($("#noOfLikes").text()) + 1);
        },
        error: function (response) {
          console.log(response.responseJSON.msg);
        },
      });
    }
  });

  //handle comment submit
  $("#commentSubmit").click(function (event) {
    event.preventDefault();
    let comment = $("#newComment").val();
    data = { body: comment, userId: 1 };
    if (comment.length < 5) {
      $("#shortComment").text("The comment is too short");
    } else {
      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/v1/handle/comment/8",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (response) {
          //do something
        },
        error: function (response) {
          //do something
        },
      });
    }
    $("#newComment").focus(function () {
      $("#shortComment").hide();
    });
  });

  //handle show replies button
  $(".showrepliesbtn").click(function () {
    alert("clicked");
  });
});
