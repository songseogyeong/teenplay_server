const pick = document.querySelector(".main-notice-choice-pick");
const nonpick = document.querySelector(".main-notice-choice-nonpick");
const noticeButton = document.querySelector(".main-notice-button");
const noticeButtonadd = document.querySelector(".main-qu-button");

pick.addEventListener("click", () => {
    const notices = document.querySelectorAll(".main-notice-content-warp");
    const noticesadd = document.querySelectorAll(".main-notice-qu-warp");
    notices.forEach((notice) => {
        notice.classList.remove("hidden");
    });

    noticesadd.forEach((noticeadd) => {
        noticeadd.classList.add("hidden");
    });

    noticeButton.classList.remove("hidden");
    noticeButtonadd.classList.add("hidden");
    pick.classList.add("main-notice-choice-pick");
    pick.classList.remove("main-notice-choice-nonpick");
    nonpick.classList.remove("main-notice-choice-pick");
    nonpick.classList.add("main-notice-choice-nonpick");
});

nonpick.addEventListener("click", () => {
    const notices = document.querySelectorAll(".main-notice-content-warp");
    const noticesadd = document.querySelectorAll(".main-notice-qu-warp");
    notices.forEach((notice) => {
        notice.classList.add("hidden");
    });
    noticesadd.forEach((noticeadd) => {
        noticeadd.classList.remove("hidden");
    });

    noticeButton.classList.add("hidden");
    noticeButtonadd.classList.remove("hidden");
    pick.classList.remove("main-notice-choice-pick");
    pick.classList.add("main-notice-choice-nonpick");
    nonpick.classList.add("main-notice-choice-pick");
    nonpick.classList.remove("main-notice-choice-nonpick");
});
