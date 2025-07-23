// JavaScript para expandir as respostas ao clicar
document.querySelectorAll(".faq__question").forEach((button) => {
  button.addEventListener("click", () => {
    const faqItem = button.parentElement;
    faqItem.classList.toggle("active");

    document.querySelectorAll(".faq__item").forEach((item) => {
      if (item !== faqItem) {
        item.classList.remove("active");
      }
    });
  });
});

document.addEventListener("click", function (event) {
  if (!event.target.closest(".faq__item")) {
    document.querySelectorAll(".faq__item").forEach((item) => {
      item.classList.remove("active");
    });
  }
});
document.addEventListener("DOMContentLoaded", function () {
  window.addEventListener("load", function () {
    const lazyImages = document.querySelectorAll("img.lazy-image");
    lazyImages.forEach((img) => {
      img.src = img.dataset.src;
      img.removeAttribute("data-src");
    });
  });
});
