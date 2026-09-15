import json
from pathlib import Path

from yt_dlp import YoutubeDL


# =========================================================
# 설정
# =========================================================

OUTPUT_FILE = "selfcontent.json"


PLAYLISTS = {
    "S2cret Diary":
        "https://youtube.com/playlist?list=PLHhitGId-8_8qk290cECozARss-80la1H",

    "Crunchy Hearts":
        "https://youtube.com/playlist?list=PLHhitGId-8_97cfBuqzBvk7GcQmnj8nGk",

    "Performances & Choreography":
        "https://youtube.com/playlist?list=PLHhitGId-8__Axy6uacn8BCbYjaXANXvS",

    "Production BH2ND":
        "https://youtube.com/playlist?list=PLHhitGId-8_8WSp0-1ZRQOPTEmrzYP1l7",

    "Hearts Chase":
        "https://youtube.com/playlist?list=PLHhitGId-8_-qN8hVnfORFmmanYP3jSkB",

    "Daily BH2ND":
        "https://youtube.com/playlist?list=PLHhitGId-8_8Nad5Dc8ManzhEKDkRuocT",

    "2025 Holiday Vlogs":
        "https://youtube.com/playlist?list=PLHhitGId-8__gcNOZQPcYfNveOb81iq32",

    "2026 Holiday Vlog":
        "https://youtube.com/playlist?list=PLHhitGId-8_8TW3vys4E3FzvSv_9MdzBZ",

    "둘셋하투하":
        "https://youtube.com/playlist?list=PLHhitGId-8_96Mutvd_sIurOZ9ueBrL-3",
}


# =========================================================
# yt-dlp 기본 옵션
# =========================================================

PLAYLIST_OPTIONS = {
    "extract_flat": True,
    "skip_download": True,
    "quiet": True,
    "no_warnings": True,
    "ignoreerrors": True,
}


VIDEO_OPTIONS = {
    "skip_download": True,
    "quiet": True,
    "no_warnings": True,
    "ignoreerrors": True,
}


# =========================================================
# 날짜 변환
# =========================================================

def format_date(upload_date):

    if not upload_date:
        return ""

    if len(upload_date) == 8:
        return (
            f"{upload_date[:4]}-"
            f"{upload_date[4:6]}-"
            f"{upload_date[6:8]}"
        )

    return upload_date


# =========================================================
# 재생목록 가져오기
# =========================================================

def get_playlist_entries(playlist_url):

    with YoutubeDL(PLAYLIST_OPTIONS) as ydl:

        info = ydl.extract_info(
            playlist_url,
            download=False
        )

    if not info:
        return []

    return info.get("entries", [])


# =========================================================
# 영상 정보 가져오기
# =========================================================

def get_video_info(video_id):

    video_url = (
        f"https://www.youtube.com/watch?v={video_id}"
    )

    with YoutubeDL(VIDEO_OPTIONS) as ydl:

        info = ydl.extract_info(
            video_url,
            download=False
        )

    return info


# =========================================================
# 재생목록 하나 처리
# =========================================================

def process_playlist(category, playlist_url):

    print()
    print("=" * 60)
    print(f"[{category}]")
    print("재생목록 확인 중...")

    results = []

    try:

        entries = get_playlist_entries(
            playlist_url
        )

    except Exception as error:

        print(f"재생목록을 불러오지 못했습니다: {error}")

        return results


    total = len(entries)

    print(f"영상 {total}개 발견")


    for index, entry in enumerate(entries, start=1):

        if not entry:
            continue

        video_id = entry.get("id")

        if not video_id:
            continue


        try:

            info = get_video_info(
                video_id
            )

            if not info:
                print(
                    f"  [{index}/{total}] "
                    f"영상 정보 없음"
                )
                continue


            title = (
                info.get("title")
                or entry.get("title")
                or ""
            ).strip()


            upload_date = (
                info.get("upload_date")
                or ""
            )


            video = {
                "videoId": video_id,
                "title": title,
                "date": format_date(
                    upload_date
                ),
                "category": category
            }


            results.append(video)


            print(
                f"  [{index}/{total}] "
                f"{title}"
            )


        except Exception as error:

            print(
                f"  [{index}/{total}] "
                f"정보 가져오기 실패: {error}"
            )


    print(
        f"→ {category}: "
        f"{len(results)}개 저장"
    )

    return results


# =========================================================
# 전체 실행
# =========================================================

def main():

    print()
    print("H2HCHIVE 자체 콘텐츠 JSON 생성기")
    print("=" * 60)
    print(f"재생목록 수: {len(PLAYLISTS)}")
    print()


    all_videos = []


    # -----------------------------------------------------
    # 9개 재생목록 처리
    # -----------------------------------------------------

    for category, playlist_url in PLAYLISTS.items():

        videos = process_playlist(
            category,
            playlist_url
        )

        all_videos.extend(
            videos
        )


    # -----------------------------------------------------
    # JSON 저장
    # -----------------------------------------------------

    output_path = Path(
        OUTPUT_FILE
    )


    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_videos,
            file,
            ensure_ascii=False,
            indent=4
        )


    # -----------------------------------------------------
    # 완료 메시지
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("완료!")
    print()
    print(
        f"총 영상 수: {len(all_videos)}"
    )
    print(
        f"저장 위치: {output_path.resolve()}"
    )
    print("=" * 60)


# =========================================================
# 시작
# =========================================================

if __name__ == "__main__":
    main()