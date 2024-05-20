// 공지사항을 생성하는 함수
function generateNotice2(title, date, content) {
    return `
    <div class="main-notice-qu-warp"> 
        <div class="main-notice-content-container">
            <div>
                <div class="main-notice-content-container-title">
                    <div class="main-notice-content-container-title-in">
                        <div class="main-notice-content-container-title-text">
                            ${title}
                        </div>
                    </div>
                    <svg stroke-width="2" stroke="currentColor" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="main-notice-content-container-title-svg">
                        <path class="arrow" stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                <div class="main-notice-content-container-date">
                    ${date}
                </div>
            </div>
        </div>
        <div class="main-notice-content-container-content">
            <div class="main-notice-text">
                ${content}
            </div>
        </div>
    </div>
    `;
}

// 새로운 공지사항을 추가하는 함수
function addNotices2() {
    const notices = [
        {
            title: "자주묻는 질문 추가1",
            date: "2024.02.12",
            content: "<p>자주묻는 질문1.</p>",
        },
        {
            title: "자주묻는 질문 추가2",
            date: "2024.02.13",
            content: "<p>자주묻는 질문2.</p>",
        },
        {
            title: "자주묻는 질문 추가3",
            date: "2024.02.14",
            content: "<p>자주묻는 질문3.</p>",
        },
        {
            title: "자주묻는 질문 추가4",
            date: "2024.02.15",
            content: "<p>자주묻는 질문4.</p>",
        },
        {
            title: "자주묻는 질문 추가5",
            date: "2024.02.16",
            content: "<p>자주묻는 질문5.</p>",
        },
    ];

    const noticeContainer = document.querySelector(".main-notice-all");
    const noticeButton = document.querySelector(".main-qu-button");

    for (let i = 0; i < notices.length; i++) {
        const noticeHTML = generateNotice2(
            notices[i].title,
            notices[i].date,
            notices[i].content
        );
        const newNoticeElement = createElementFromHTML(noticeHTML);
        noticeContainer.insertBefore(newNoticeElement, noticeButton);
        initializeNotice(newNoticeElement);
    }
}

// HTML 문자열로부터 요소를 생성하는 함수
function createElementFromHTML(htmlString) {
    const div = document.createElement("div");
    div.innerHTML = htmlString.trim();
    return div.firstChild;
}

// 클릭 이벤트 초기화 함수
function initializeNotice(noticeElement) {
    const content = noticeElement.querySelector(
        ".main-notice-content-container-content"
    );
    const path = noticeElement.querySelector(
        ".main-notice-content-container-title-svg path"
    );

    noticeElement.addEventListener("click", () => {
        content.classList.toggle("active");
        if (content.classList.contains("active")) {
            path.setAttribute("d", "M5 15l7-7 7 7");
        } else {
            path.setAttribute("d", "M19 9l-7 7-7-7");
        }
    });
}

// '더보기' 버튼을 클릭했을 때 새로운 공지사항을 추가
const noticeButton2 = document.querySelector(".main-qu-button");
noticeButton2.addEventListener("click", addNotices2);

// 초기화 함수를 통해 기존 공지사항에 클릭 이벤트 적용.
const existingNotices2 = document.querySelectorAll(".main-notice-qu-warp");
existingNotices2.forEach((notice) => {
    initializeNotice(notice);
});
