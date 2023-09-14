const ratingButtons = document.querySelectorAll('.rating-buttons');

ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        const value = parseInt(event.target.dataset.value);
        const articleId = parseInt(event.target.dataset.article);
        const ratingSum = button.querySelector('.rating-sum');

        const formData = new FormData();

        formData.append('article_id', articleId);
        formData.append('value', value);

        fetch("/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            ratingSum.textContent = data.rating_sum;
        })
        .catch(error => console.log(error));
    });
});