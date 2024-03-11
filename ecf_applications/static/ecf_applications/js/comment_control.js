const addCommentButtons = document.querySelectorAll('#add-comment');
const commentBoxes = document.querySelectorAll('#comment-box');

addCommentButtons.forEach(button => {
    button.onclick = (e) => {
        e.preventDefault();

        button.textContent = button.textContent === 'Add Comment' ? 'Cancel' : 'Add Comment';

        const commentBox = button.parentElement.querySelector('#comment-box');
        commentBox.classList.toggle('hidden');
        commentBox.toggleAttribute('disabled');
        commentBox.toggleAttribute('required');
        commentBox.focus();
    }
});


const callback = function(mutationsList, observer) {
    for(let mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'disabled') {
            let submitButton = document.querySelector('#submit-comments');
            let allDisabled = true;

            commentBoxes.forEach(commentBox => {
                if (!commentBox.disabled) {
                    allDisabled = false;
                }
            });

            if (allDisabled) {
                submitButton.classList.add('hidden');
            } else {
                submitButton.classList.remove('hidden');
            }            
        }
    }
};

// Create an observer instance linked to the callback function
const observer = new MutationObserver(callback);

// Start observing the comment boxes with the configured parameters
commentBoxes.forEach(commentBox => {
    observer.observe(commentBox, { attributes: true });
});