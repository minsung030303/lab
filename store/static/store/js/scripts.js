document.addEventListener("DOMContentLoaded", () => {
    const track = document.getElementById("bannerTrack");
    const cards = Array.from(track.children);
    const visible = 3;
    let index = 1;

    // 복제 카드 추가
    for (let i = 0; i < visible; i++) {
        const clone = cards[i].cloneNode(true);
        track.appendChild(clone);
    }

    setInterval(() => {
        index++;
        track.style.transform = `translateX(-${index * (100 / visible)}%)`;

        if (index === cards.length) {
            setTimeout(() => {
                track.style.transition = "none";
                index = 0;
                track.style.transform = "translateX(0)";
                void track.offsetWidth;
                track.style.transition = "transform 0.6s ease";
            }, 600);
        }
    }, 3000);
});
