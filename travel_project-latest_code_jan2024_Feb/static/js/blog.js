// Function to display blog posts
function displayBlogPosts() {
    const blogPostsContainer = document.getElementById("blog-posts");
    blogPostsContainer.innerHTML = ""; // Clear existing posts

    blogPosts.forEach(post => {
        const postElement = document.createElement("article");
        const mediaDiv = document.createElement("div");
        mediaDiv.classList.add("post-media");
        const contentDiv = document.createElement("div");
        contentDiv.classList.add("post-content");

        if (post.media.endsWith('.mp4')) {
            const videoElement = document.createElement('video');
            videoElement.src = post.media;
            videoElement.controls = true;
            mediaDiv.appendChild(videoElement);
        } else {
            const imageElement = document.createElement('img');
            imageElement.src = post.media;
            imageElement.alt = post.title;
            mediaDiv.appendChild(imageElement);
        }

        contentDiv.innerHTML = `
            <h2>${post.title}</h2>
            <p>${post.content}</p>
        `;

        
        postElement.appendChild(contentDiv);
        blogPostsContainer.appendChild(postElement);
        postElement.appendChild(mediaDiv);
    });
}

// Function to handle choosing media from local files
function chooseMedia() {
    const fileInput = document.getElementById("file-input");
    fileInput.click(); // Trigger click event on the hidden file input
}

// Function to display the selected file path
function displayFilePath() {
    const fileInput = document.getElementById("file-input");
    const filePathDisplay = document.getElementById("file-path-display");
    filePathDisplay.textContent = fileInput.value; // Display the selected file path
}

// Function to add a new blog post
function addBlogPost(event) {
    event.preventDefault();
    
    const titleInput = document.getElementById("post-title");
    const contentInput = document.getElementById("post-content");
    const fileInput = document.getElementById("file-input");

    const title = titleInput.value;
    const content = contentInput.value;
    const media = URL.createObjectURL(fileInput.files[0]); // Get the local file URL

    if (title && content && media) {
        const newPost = { title, content, media };
        blogPosts.push(newPost);
        displayBlogPosts(); // Re-render all blog posts
        titleInput.value = ''; // Clear the input fields
        contentInput.value = '';
        fileInput.value = ''; // Clear the file input
        document.getElementById("file-path-display").textContent = ''; // Clear the file path display
    } else {
        alert("Please fill in all fields and choose a media file.");
    }
}

// Call the function to display initial blog posts when the page loads
window.onload = function() {
    displayBlogPosts();
    const addPostForm = document.getElementById("add-post-form");
    const chooseMediaButton = document.getElementById("choose-media");
    const fileInput = document.getElementById("file-input");

    addPostForm.addEventListener("submit", addBlogPost);
    chooseMediaButton.addEventListener("click", chooseMedia);
    fileInput.addEventListener("change", displayFilePath);
};
