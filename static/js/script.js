// script.js
// dark mode

document.addEventListener('DOMContentLoaded', function () {
    var icon = document.getElementById("dark-icon");
    var navbar = document.querySelector("nav");
    var cards = document.getElementsByClassName("card-body");
    var cardtxt = document.getElementsByClassName("card-text");
    var cardtit = document.getElementsByClassName("card-title");

    icon.onclick = function () {
        document.body.classList.toggle("dark-theme");
        navbar.classList.toggle("dark-theme");

        // Loop through each card element and toggle the class
        for (var i = 0; i < cards.length; i++) {
            cards[i].classList.toggle("dark-theme");
        }

        // The same applies to cardtxt and cardtit if they are collections
        // Loop through each cardtxt element and toggle the class
        for (var i = 0; i < cardtxt.length; i++) {
            cardtxt[i].classList.toggle("dark-theme");
        }

        // Loop through each cardtit element and toggle the class
        for (var i = 0; i < cardtit.length; i++) {
            cardtit[i].classList.toggle("dark-theme");
        }
        if (navbar.classList.contains("dark-theme")) {
            icon.src = "{% static 'img/sun.png' %}";
        } else {
            icon.src = "{% static 'img/moon.png' %}";
        }
        

    };
});



// counter
const counters = document.querySelectorAll(".counters h1 span");
const container = document.querySelector(".counters");
let activated = false;

window.addEventListener("scroll", () => {
    const screenWidth = window.innerWidth;
    const isLargeScreen = screenWidth >= 1025 && screenWidth <= 1600;

    const scrollConditionLarge = (
        window.pageYOffset > container.offsetTop - container.offsetHeight - 200 &&
        activated === false && isLargeScreen
    );

    const scrollConditionSmall = (
        window.pageYOffset < container.offsetTop - container.offsetHeight - 500 ||
        window.pageYOffset === 0
    );

    if (scrollConditionLarge || scrollConditionSmall) {
        counters.forEach((counter) => {
            counter.innerText = 0;
            let count = 0;

            function updateCount() {
                const target = parseInt(counter.dataset.count);
                if (count < target) {
                    count++;
                    counter.innerText = count;
                    setTimeout(updateCount, 1);
                } else {
                    counter.innerText = target;
                }
            }

            updateCount();
            activated = true;
        });
    } else if (
        window.pageYOffset < container.offsetTop - container.offsetHeight - 500 ||
        window.pageYOffset === 0
    ) {
        counters.forEach((counter) => {
            counter.innerText = 0;
        });
        activated = false;
    }
});

