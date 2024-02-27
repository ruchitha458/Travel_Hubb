document.addEventListener("DOMContentLoaded", function() {
    // Function to update likes
    function updateLikes(title) {
        // Fetch the JSON file with the likes data
        fetch(file_local)
            .then(response => response.json())
            .then(data => {
                // Update the like count for the specified title
                data[title]++;
                // Send the updated likes data to the server
                fetch("/update_likes", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        // Add authorization token or session identifier here
                    },
                    body: JSON.stringify(data)
                })
                .then(response => {
                    if (response.ok) {
                        console.log("Likes updated successfully.");
                    } else {
                        console.error("Failed to update likes.");
                    }
                })
                .catch(error => {
                    console.error("Error updating likes:", error);
                });
            })
            .catch(error => {
                console.error("Error fetching likes data:", error);
            });
    }

    // Handle like button click
    document.querySelectorAll(".likeBtn").forEach(function(btn) {
        btn.addEventListener("click", function() {
            var title = this.getAttribute("data-title");
            updateLikes(title);
            // Update the like count on the page
            var likeCountSpan = document.getElementById("likeCount-" + title);
            likeCountSpan.textContent = parseInt(likeCountSpan.textContent) + 1;
        });
    });
});
