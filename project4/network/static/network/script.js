document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".edit-button").forEach(button => {
        button.addEventListener("click", function() {
           const idPost = button.dataset.postId;
           console.log(idPost);
        //    const post = document.getElementById(`post-${idPost}`);
           const post = document.getElementById("post-"+idPost);
           const content = post.querySelector(".post-content");
           content.classList.add("d-none");

           const contentEdit = post.querySelector(".post-edit");
           contentEdit.classList.remove("d-none");
           button.classList.add("d-none");

           const contenCurrent = content.querySelector(".card-text").textContent;
           console.log(contenCurrent);
           const newContent = contentEdit.querySelector(".edit-text");
           newContent.value = contenCurrent;

           const saveButton = post.querySelector(".save-text");
           saveButton.addEventListener("click", function(){
            fetch(`/edit-post/${idPost}`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ content: newContent.value })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            alert(data.error);
                            return;
                        }
                        const contentUpDated = data.content;
                        const elementContent = content.querySelector(".card-text");
                        elementContent.textContent = contentUpDated;
                        content.classList.remove("d-none");
                        contentEdit.classList.add("d-none");
                        button.classList.remove("d-none");
                        
                        });
           })

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
