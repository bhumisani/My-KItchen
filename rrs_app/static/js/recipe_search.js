
const searchInput = document.getElementById("recipeSearch");
const recipeRows = document.querySelectorAll(".recipe-row");
const noResults = document.getElementById("noResults");

searchInput.addEventListener("input", function () {
    const searchText = searchInput.value.toLowerCase().trim();

    let visibleRows = 0;

    recipeRows.forEach(function (row) {
        const recipeTitle = row
            .querySelector(".recipe-title")
            .textContent
            .toLowerCase();

        if (recipeTitle.includes(searchText)) {
            row.style.display = "";
            visibleRows++;
        } else {
            row.style.display = "none";
        }
    });

    if (visibleRows === 0 && searchText !== "") {
        noResults.style.display = "block";
    } else {
        noResults.style.display = "none";
    }
});