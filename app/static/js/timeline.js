/**
* Configuration options for date formatting
*/
const DATE_FORMAT_OPTIONS = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric', 
    hour: 'numeric',
    minute: '2-digit',
    timeZone: 'America/New_York', 
    timeZoneName: 'short',
    hour12: true
 };
 
 /**
 * Formats a UTC date string to localized date display
 */
 const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString('en-US', DATE_FORMAT_OPTIONS);
 };
 

 const handlePostDeletion = async (postElement) => {
    const postId = postElement.dataset.postId;
    
    // Confirm deletion with user
    if (!confirm('Are you sure you want to delete this post?')) {
        return;
    }
 
    try {
        const response = await fetch(`${window.APP_URLS.deletePost}${postId}`, {
            method: 'DELETE'
        });
 
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to delete post');
        }
 
        postElement.remove();
    } catch (error) {
        console.error('Delete error:', error);
        alert('Failed to delete post. Please try again.');
    }
 };
 
 /**
 * Initializes the timeline functionality:
 * - Formats all date displays to local timezone
 * - Sets up delete button handlers for admin users
 */
 const initializeTimeline = () => {
    // Format all post dates
    document.querySelectorAll('.post-date').forEach(el => {
        const dateStr = el.getAttribute('data-date');
        if (dateStr) {
            el.textContent = formatDate(dateStr);
        }
    });
 
    // Set up delete button handlers
    document.querySelectorAll('.delete-post').forEach(button => {
        button.addEventListener('click', () => {
            const postElement = button.closest('.box');
            if (postElement) {
                handlePostDeletion(postElement);
            }
        });
    });
 };
 
 // Initialize when DOM is ready
 document.addEventListener('DOMContentLoaded', initializeTimeline);