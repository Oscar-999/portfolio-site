document
  .getElementById("timeline-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch("/api/timeline_post", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("content").value = "";

        let postHtml = `
            <div class="timeline-post">
                <h3>${data.name}</h3>
                <p><strong>${data.email}</strong></p>
                <p>${data.content}</p>
                <p>${new Date(data.created_at).toLocaleString()}</p>
                <img src="https://www.gravatar.com/avatar/${data.email}?s=200&d=identicon" alt="Profile Image">
                <hr>
                </div>
                `;
        document.querySelector(".timeline-posts").insertAdjacentHTML('afterbegin', postHtml);
      })
      .catch((error) => console.error("Error:", error));
  });
