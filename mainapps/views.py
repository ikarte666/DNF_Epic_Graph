import requests
import json
import os
import datetime
from urllib import parse
from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from . import forms


def main_view(request):
    form = forms.SearchForm()
    return render(request, "main/home.html", {"form": form})


def search_view(request):
    def switch(x):
        return {
            "cain": "카인",
            "hilder": "힐더",
            "prey": "프레이",
            "casillas": "카시야스",
            "siroco": "시로코",
            "diregie": "디레지에",
            "anton": "안톤",
            "bakal": "바칼",
        }[x]

    #  변수 값 세팅 및 apikey 가져오기
    server = request.GET.get("server")
    name = request.GET.get("char_name")
    s_date = request.GET.get("start_date")
    s_date += " 00:00"
    e_date = request.GET.get("end_date")
    e_date2 = e_date
    day_count = 0
    all_count = 0
    max_count = 0
    avg_count = 0

    today = datetime.datetime.now()
    today_date = today.strftime("%Y-%m-%d")

    if e_date == today_date:
        e_date += " " + today.strftime("%H:%M")
    else:
        e_date += " 23:59"

    secret_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "secrets.json"
    )

    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

    apikey = get_secret("API_KEY")
    encoded_name = parse.quote(name)

    #  characterId 얻기
    first_request_url = f"https://api.neople.co.kr/df/servers/{server}/characters?characterName={encoded_name}&apikey={apikey}"
    first_response = requests.get(first_request_url)

    first_data = json.loads(first_response.text)
    first_data = first_data["rows"][0]

    char_id = first_data["characterId"]

    # 타임라인 가져오기
    timeline_request = f"https://api.neople.co.kr/df/servers/{server}/characters/{char_id}/timeline?limit=100&code=505,507,513,504&startDate={s_date}&endDate={e_date}&next=&apikey={apikey}&next="
    timeline_response = requests.get(timeline_request)
    loaded_data = json.loads(timeline_response.text)

    # 타임라인에서 에픽먹은 날짜 추출
    timeline_data = loaded_data["timeline"]["rows"]

    # 데이터가 100개가 넘을 경우 next 받아서 처리
    while loaded_data["timeline"]["next"] is not None:
        next_key = loaded_data["timeline"]["next"]
        timeline_request = f"https://api.neople.co.kr/df/servers/{server}/characters/{char_id}/timeline?limit=100&code=505,507,513,504&apikey={apikey}&next={next_key}"
        timeline_response = requests.get(timeline_request)
        loaded_data = json.loads(timeline_response.text)
        timeline_data += loaded_data["timeline"]["rows"]

    dict_data = {}

    # 시작일과 종료일 사이의 모든 날을 구해서 리스트로 만듦
    d_start_date = s_date[0:10]
    d_start_date = datetime.date(
        int(d_start_date.split("-")[0]),
        int(d_start_date.split("-")[1]),
        int(d_start_date.split("-")[2]),
    )
    d_end_date = datetime.date(
        int(e_date2.split("-")[0]), int(e_date2.split("-")[1]), int(e_date2.split("-")[2]),
    )
    delta = d_end_date - d_start_date
    datelist = []

    for day in range(delta.days + 1):
        day_count += 1
        datelist.append(d_start_date + datetime.timedelta(days=day))

    #  날짜 리스트 월-일 까지만 잘라서 저장
    for i, day in enumerate(datelist):
        datelist[i] = str(datelist[i])
        datelist[i] = datelist[i][5:10]

    #  날짜를 월일 까지만 자르고 딕셔너리에 값 추가
    for data in timeline_data:
        date = data["date"]
        date = date[5:10]

        try:
            dict_data[date] += 1
        except Exception:
            dict_data[date] = 1
        finally:
            all_count += 1  # 에픽 총 카운트 더해줌
            if dict_data[date] > max_count:
                max_count = dict_data[date]

    #  날짜 리스트를 돌면서 딕셔너리에 없는 날짜 값을 0으로 추가(에픽 못먹은날)
    for day in datelist:
        try:
            dict_data[day] += 0
        except Exception:
            dict_data[day] = 0

    sdict_data = sorted(dict_data.items())  # 딕셔너리 값을 날짜순으로 정렬(오름차순)
    json_data = {}

    for i in sdict_data:
        json_data[i[0]] = i[1]  # json 데이터(완전한 딕셔너리)로 만듦

    keys = list(json_data.keys())
    values = list(json_data.values())
    avg_count = round(all_count / day_count, 1)
    server_name = switch(server)

    context = {
        "date": keys,
        "count": values,
        "max_count": max_count,
        "avg_count": avg_count,
        "all_count": all_count,
        "name": name,
        "server": server,
        "server_name": server_name,
        "char_id": char_id,
    }

    return render(request, "main/search.html", context=context,)
