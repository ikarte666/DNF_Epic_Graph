window.onload = function () {
    let search = document.getElementById("search");

    search.addEventListener(
        "click",
        () => {
            let name = document.getElementById("id_char_name");
            let start_date = document.getElementById("id_start_date");
            let end_date = document.getElementById("id_end_date");
            let first_end_date = end_date;
            let today = new Date();
            let today_month = today.getMonth() + 1;
            let today_date = today.getDate();

            today_month = "00" + today_month.toString();
            today_month = today_month.slice(-2);

            today_date = "00" + today_date.toString();
            today_date = today_date.slice(-2);

            let today_str =
                today.getFullYear().toString() +
                "-" +
                today_month +
                "-" +
                today_date;

            start_date = start_date.value;
            start_date = start_date.replace(/-/g, "/");
            start_date = start_date + "/00:00:00";

            end_date = end_date.value;
            if (today_str == end_date) {
                let today_time =
                    "/" +
                    today.getHours().toString() +
                    ":" +
                    today.getMinutes().toString() +
                    ":" +
                    today.getSeconds().toString();

                end_date = end_date.replace(/-/g, "/");
                end_date = end_date + today_time;
            } else {
                end_date = end_date + "/23:59:59";
            }

            let s_date = new Date(start_date);
            let e_date = new Date(end_date);

            alert(today);
            alert(s_date);
            alert(e_date);

            if (name.value == "") {
                alert("캐릭터 이름을 입력해주세요");
                event.preventDefault();
            } else if (start_date.value == "" || first_end_date.value == "") {
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
        },
        { once: false }
    );
};
