// JavaScript to handle button clicks
document.getElementById("likeBtn").addEventListener("click", function() {
  console.log("You liked the content!"); // Log a message to the console
  
  // Add animation to the thumbs-up icon
  var thumbsUpIcon = document.querySelector("#likeBtn i");
  thumbsUpIcon.classList.remove("fa-thumbs-up");
  thumbsUpIcon.classList.add("fa-thumbs-up", "animate-like");
  
  // Add any further actions here if needed
});

// JavaScript to handle button clicks and save like count
let likeCount = 0;

document.getElementById("likeBtn").addEventListener("click", function() {
  likeCount++;
  console.log("You liked the content! Total likes: " + likeCount); // Log a message to the console with the updated like count
  
  // Update the button text with the new like count
  document.getElementById("likeBtn").innerText = "Like (" + likeCount + ")";
  
  // Add animation to the thumbs-up icon
  var thumbsUpIcon = document.querySelector("#likeBtn i");
  thumbsUpIcon.classList.remove("fa-thumbs-up");
  thumbsUpIcon.classList.add("fa-thumbs-up", "animate-like");
  
  // Add any further actions here if needed
});


