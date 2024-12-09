document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".edit-button").forEach(button => {
        button.addEventListener("click", function() {
            const postDiv = this.closest(".post");
            const postId = postDiv.dataset.postId;
            const postContentSpan = postDiv.querySelector(".card-text");
            const originalContent = postContentSpan.textContent;

            // Replace content with textarea
            const textarea = document.createElement("textarea");
            textarea.classList.add("w-100");
            textarea.value = originalContent;
            postContentSpan.replaceWith(textarea);

            // Change "Edit" button to "Save"
            this.textContent = "Save";
            this.classList.remove("edit-button");
            this.classList.add("save-button");

            // Handle "Save" button click
            // this.addEventListener("click", function() {
            //     const newContent = textarea.value.trim();

            //     if (!newContent) {
            //         alert("Post content cannot be empty.");
            //         return;
            //     }

            //     fetch(`/edit_post/${postId}/`, {
            //         method: "PUT",
            //         headers: { "Content-Type": "application/json" },
            //         body: JSON.stringify({ content: newContent })
            //     })
            //     .then(response => response.json())
            //     .then(data => {
            //         if (data.error) {
            //             alert(data.error);
            //             return;
            //         }

            //         // Replace textarea with updated content
            //         const updatedSpan = document.createElement("span");
            //         updatedSpan.classList.add("post-content");
            //         updatedSpan.textContent = data.content;
            //         textarea.replaceWith(updatedSpan);

            //         // Change "Save" button back to "Edit"
            //         this.textContent = "Edit";
            //         this.classList.remove("save-button");
            //         this.classList.add("edit-button");
            //     });
            // });
        });
    });
});
