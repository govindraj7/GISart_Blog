//! ///// vanilla js & anime.js code /////
//* ///// about pg img manipulation ///// ------------------------------------------------------------------------------------------------------------------------ */

// her0 & nav GISart fade animation
var textWrapper = document.querySelector(".text-fade-in");
textWrapper.innerHTML = textWrapper.textContent.replace(
  /\S/g,
  "<span class='letter'>$&</span>"
);

anime
  .timeline({ loop: true })
  .add({
    targets: ".text-fade-in .letter",
    opacity: [0, 1],
    easing: "easeInOutQuad",
    duration: 2250,
    delay: (el, i) => 150 * (i + 1),
  })
  .add({
    targets: ".text-fade-in",
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000,
  });

anime({
  targets: ".staggering .el",
  translateX: 90,
  duration: 1500,
  delay: anime.stagger(150, { start: 500 }),
});

//* ///// about page img manipulation ///// ------------------------------------------------------------------------------------------------------------------------ */

function jsTest2(image) {
  image.src = "static/images/Kazakhstan.png";
}

// kazakhstan imgs
function KazakImage1(image) {
  image.src = "static/images/Kazakhstan.png";
}

function KazakImage2(image) {
  image.src = "static/images/Kazakhstan-2.png";
}

// algeria imgs

function algeImage1(image) {
  image.src = "static/images/Algeria-2.png";
}

function algeImage2(image) {
  image.src = "static/images/Algeria.png";
}
