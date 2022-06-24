//  about page image changes

function jsTest2(image) {
  image.src = "static/images/Kazakhstan.jpeg";
}

// kazakhstan
function KazakImage1(image) {
  image.src = "static/images/Kazakhstan.jpeg";
}

function KazakImage2(image) {
  image.src = "static/images/Kazakhstan-2.jpeg";
}

// alge
function algeImage1(image) {
  image.src = "static/images/Algeria-2.jpeg";
}

function algeImage2(image) {
  image.src = "static/images/Algeria.jpeg";
}

// * ///// anime.js code /////

// links slide in
// let slide_ltr = anime({
//   targets: ".slide-ltr",
//   translateX: 150,
//   delay: 1500,
//   easing: "easeInOutSine",
// });

var textWrapper = document.querySelector(".text-fade-in");
textWrapper.innerHTML = textWrapper.textContent.replace(
  /\S/g,
  "<span class='letter'>$&</span>"
);

// title fade animation
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

//  enlarge
// anime({
//   targets: ".space-effect",
//   scale: 1.5,
//   direction: "alternate",
//   loop: true,
//   easing: "easeInOutSine",
//   duration: 50000,
// });

anime({
  targets: ".staggering .el",
  translateX: 160,
  duration: 1500,
  delay: anime.stagger(150, { start: 500 }), // delay starts at 500ms then increase by 100ms for each elements.
});
