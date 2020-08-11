window.onload = function () {
    let name = document.getElementById("id_char_name");
    let search = document.getElementById("search");
    let start_date = document.getElementById("id_start_date");
    let end_date = document.getElementById("id_end_date");

    search.addEventListener("click", () => {
        end_date = end_date.value;
        end_date = end_date.replace(/-/g, "/");
        end_date = end_date + "/00:00:00";

        let s_date = new Date(start_date.value);
        let e_date = new Date(end_date);
        let today = new Date();

        if (name.value == "") {
            alert("캐릭터 이름을 입력해주세요");
            event.preventDefault();
        } else if (start_date.value == "" || end_date.value == "") {
            alert("기간을 정확히 입력해주세요");
            event.preventDefault();
        } else if (s_date > today || e_date > today) {
            alert("시작일과 종료일은 오늘을 넘을 수 없습니다");
            event.preventDefault();
        } else if (s_date > e_date) {
            alert("시작일이 종료일보다 큽니다");
            event.preventDefault();
        }
        if ((e_date - s_date) / 1000 / 60 / 60 / 24 > 90) {
            alert("최대 90일까지 조회 가능합니다");
            event.preventDefault();
        }
    });
};
