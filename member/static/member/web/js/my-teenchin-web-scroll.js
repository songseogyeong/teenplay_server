const postLists = document.querySelectorAll(".teenchin-list-add");

postLists.forEach((postList) => {
    let startX = 0;
    let listX = 0;
    let isDragging = false;

    const onScrollStart = (e) => {
        startX = getClientX(e);
        isDragging = true;
        postList.style.transition = ""; // 드래그 시작할 때 transition 제거
    };

    const onScrollMove = (e) => {
        if (!isDragging) return;
        const nowX = getClientX(e);
        const diffX = nowX - startX;
        setTranslateX(listX + diffX);
    };

    const onScrollEnd = () => {
        if (!isDragging) return;
        isDragging = false;
        listX = getTranslateX();
        postList.style.transition = `transform 0.3s ease`; // 드래그 끝날 때 transition 추가
    };

    const getClientX = (e) => {
        return e.touches ? e.touches[0].clientX : e.clientX;
    };

    const getTranslateX = () => {
        const transformMatrix = getComputedStyle(postList).transform;
        if (transformMatrix === 'none') {
            return 0;
        }
        return parseFloat(transformMatrix.split(',')[4]);
    };

    const setTranslateX = (x) => {
        postList.style.transform = `translateX(${x}px)`;
    };

    const bindEvents = () => {
        postList.addEventListener("mousedown", onScrollStart);
        postList.addEventListener("touchstart", onScrollStart, { passive: true });
        window.addEventListener("mousemove", onScrollMove);
        window.addEventListener("touchmove", onScrollMove, { passive: true });
        window.addEventListener("mouseup", onScrollEnd);
        window.addEventListener("touchend", onScrollEnd);
    };

    const unbindEvents = () => {
        window.removeEventListener("mousemove", onScrollMove);
        window.removeEventListener("touchmove", onScrollMove);
        window.removeEventListener("mouseup", onScrollEnd);
        window.removeEventListener("touchend", onScrollEnd);
    };

    bindEvents();
});