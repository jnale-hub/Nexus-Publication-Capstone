document.addEventListener("DOMContentLoaded", () => {
    
    document.getElementById('toggle-comments').addEventListener('click', function (event) {
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
})
