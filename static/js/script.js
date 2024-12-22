// Event Listener
// - About Page
const navItems = document.querySelectorAll('.education_tab_selection button');
navItems.forEach(item => {
    item.addEventListener('click', () => {
        navItems.forEach(navItem => {
            navItem.classList.remove('selected')
        })
        item.classList.add('selected')
    })
});

const images = ["src/baymax.png", "src/KDU Logo.png"];
let currentIndex = 0;

document.getElementById("showImageBtn").addEventListener("click", function () {
    populateThumbnails();
    showImage(currentIndex);
    document.getElementById("imageOverlay").style.display = "block";
});

document.getElementById("closeImageBtn").addEventListener("click", function () {
    document.getElementById("imageOverlay").style.display = "none";
});

// - Skill Page


//   document.getElementById("showImageBtn").addEventListener("click", function() {
//     document.getElementById("imageOverlay").style.display = "block";
// });

// document.getElementById("closeImageBtn").addEventListener("click", function() {
//     document.getElementById("imageOverlay").style.display = "none";
// });

// Function
function opentab(event) {
    var i, x;

    x = document.getElementsByClassName("tab_effect");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }

    var blockShowID = event.target.innerText;
    document.getElementById(blockShowID).style.display = "block";
}

function populateThumbnails() {
    const thumbnailContainer = document.getElementById("thumbnailContainer");
    thumbnailContainer.innerHTML = "";

    images.forEach((image, index) => {
        const thumbnail = document.createElement("img");
        thumbnail.src = image;
        thumbnail.className = "thumbnail";
        thumbnail.addEventListener("click", () => showImage(index));
        thumbnailContainer.appendChild(thumbnail);
    });
}

function showImage(index) {
    const currentImage = document.getElementById("currentImage");
    currentImage.src = images[index];
    currentIndex = index;
}