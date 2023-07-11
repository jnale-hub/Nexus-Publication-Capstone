document.addEventListener("DOMContentLoaded", function() {
    // Toggle comments section
    document.getElementById('toggle-comments').addEventListener('click', function(event) {
        event.preventDefault();
        var commentsSection = document.getElementById('comments-section');
        if (commentsSection.style.display === 'none') {
            commentsSection.style.display = 'block';
            this.textContent = 'Hide Comments';
        } else {
            commentsSection.style.display = 'none';
            this.textContent = 'View Comments';
        }
    });

    // Pagination for comments
    const commentItems = document.querySelectorAll(".comment-item");
    const seeMoreButton = document.getElementById("see-more-button");

    const commentsToShow = 5;
    let visibleComments = commentsToShow;

    // Show initial comments
    for (let i = 0; i < visibleComments; i++) {
        if (commentItems[i]) {
            commentItems[i].style.display = "block";
        }
    }

    // Hide "See More" button if there are no more comments to show
    if (visibleComments >= commentItems.length) {
        seeMoreButton.style.display = "none";
    }

    seeMoreButton.addEventListener("click", function() {
        // Show the next batch of comments
        for (let i = visibleComments; i < visibleComments + commentsToShow; i++) {
            if (commentItems[i]) {
                commentItems[i].style.display = "block";
            }
        }

        visibleComments += commentsToShow;

        // Hide "See More" button if there are no more comments to show
        if (visibleComments >= commentItems.length) {
            seeMoreButton.style.display = "none";
        }
    });
});
