NodeList.prototype.filter = Array.prototype.filter;

const pauseIcons = document.querySelectorAll(".pause");
const playIcons = document.querySelectorAll(".restart");
const videos = document.querySelectorAll(".play-video");
const videoInfos = document.querySelectorAll(".play-info-wrap");
const controlButtons = document.querySelectorAll(".play-control-wrap");
const progressBars = document.querySelectorAll(".progress-bar-now");
const muteIcons = document.querySelectorAll(".mute");
const unmuteIcons = document.querySelectorAll(".unmute");
const videoWraps = document.querySelectorAll(".play-each");
let nowPlaying = document.querySelector(".play-each.playing");
const slideWrap = document.querySelector(".play-items");
const slideContainer = document.querySelector(".play-item");
const likeBtns = document.querySelectorAll(".play-like-btn");
const emptyHeart = document.querySelectorAll(".play-like-icon.empty");
const fullHeart = document.querySelectorAll(".play-like-icon.full");

// 재생 중이 아닌 영상은 일시정지로 시작

videoWraps.forEach((videoWrap, i) => {
    if (!videoWrap.classList.contains("playing")) {
        videos[i].autoplay = false;
    } else {
        videos[i].autoplay = true;
    }
});

videos[0].play();

// 일시정지, 재생 관련 버튼
// false일 때 클릭 시 재생, true일 때 클릭 시 일시정지
globalThis.flags = new Array(videos.length);

videos.forEach((video, i) => {
    video.addEventListener("click", (e) => {
        if (!globalThis.flags[i]) {
            globalThis.flags[i] = true;
            pauseIcons[i].style.display = "none";
            playIcons[i].style.display = "block";
            e.target.pause();
        } else {
            globalThis.flags[i] = false;
            pauseIcons[i].style.display = "block";
            playIcons[i].style.display = "none";
            e.target.play();
        }
    });
});

// 음소거 관련 버튼
muteIcons.forEach((mute) => {
    mute.addEventListener("click", () => {
        muteIcons.forEach((mute) => {
            mute.style.display = "none";
        });
        videos.forEach((video) => {
            video.muted = true;
        });
        unmuteIcons.forEach((unmute) => {
            unmute.style.display = "block";
        });
    });
});

unmuteIcons.forEach((unmute) => {
    unmute.addEventListener("click", (e) => {
        unmuteIcons.forEach((unmute) => {
            unmute.style.display = "none";
        });
        videos.forEach((video) => {
            video.muted = false;
        });
        muteIcons.forEach((mute) => {
            mute.style.display = "block";
        });
    });
});

// 진행도 1초마다 증가
videos.forEach((video, i) => {
    video.addEventListener("timeupdate", (e) => {
        let percent = (e.target.currentTime / e.target.duration) * 100;
        progressBars[i].style.width = `${percent}%`;
    });
});

// 스크롤로 이전/다음 틴플레이 이동

function slideNext(idx) {
    slideContainer.style.transition = `all 0.5s ease-in`;
    slideContainer.style.transform = `translateY(-${window.innerHeight * idx}px)`;
    videoWraps[idx - 1].classList.remove("playing");
    videoWraps[idx].classList.add("playing");
}

function slidePrev(idx) {
    slideContainer.style.transition = `all 0.5s ease-in`;
    slideContainer.style.transform = `translateY(-${window.innerHeight * idx}px)`;
    videoWraps[idx + 1].classList.remove("playing");
    videoWraps[idx].classList.add("playing");
}

function manageScroll(e) {
    e.preventDefault();
    e.stopPropagation();
    return;
}

let idx = 0;
let check = true;
slideWrap.addEventListener("wheel", (e) => {
    manageScroll(e);
    if (!check) return;
    check = false;
    for (let i = 0; i < videoWraps.length; i++) {
        if (videoWraps[i].classList.contains("playing")) {
            idx = i;
            break;
        }
    }
    if (e.deltaY > 0) {
        setTimeout(() => {
            check = true;
        }, 800);
        if (idx == videoWraps.length - 1) {
            return;
        }
        slideNext(idx + 1);
        videos[idx].pause();
        globalThis.flags[idx] = true;
        pauseIcons[idx].style.display = "none";
        playIcons[idx].style.display = "block";
        idx++;
        videos[idx].play();
        globalThis.flags[idx] = false;
        pauseIcons[idx].style.display = "block";
        playIcons[idx].style.display = "none";
    } else {
        setTimeout(() => {
            check = true;
        }, 800);
        if (idx == 0) {
            return;
        }
        slidePrev(idx - 1);
        videos[idx].pause();
        globalThis.flags[idx] = true;
        pauseIcons[idx].style.display = "none";
        playIcons[idx].style.display = "block";
        idx--;
        videos[idx].play();
        globalThis.flags[idx] = false;
        pauseIcons[idx].style.display = "block";
        playIcons[idx].style.display = "none";
    }
});

// 좋아요 아이콘 클릭 시 반영
likeBtns.forEach((button, i) => {
    button.addEventListener("click", () => {
        if (emptyHeart[i].style.display == "none") {
            emptyHeart[i].style.display = "block";
            fullHeart[i].style.display = "none";
        } else {
            emptyHeart[i].style.display = "none";
            fullHeart[i].style.display = "block";
        }
    });
});

// 좋아요 수 증가는 비동기로 좋아요 db에 반영 후 가져와 넣기 때문에
// 현재 화면에서는 구현하지 않습니다.
