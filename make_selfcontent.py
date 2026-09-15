import json
from yt_dlp import YoutubeDL

OUTPUT_FILE = "selfcontent.json"

PLAYLISTS = {
    "S2cret Diary": "https://youtube.com/playlist?list=PLHhitGId-8_8qk290cECozARss-80la1H",
    "Crunchy Hearts": "https://youtube.com/playlist?list=PLHhitGId-8_97cfBuqzBvk7GcQmnj8nGk",
    "Performances & Choreography": "https://youtube.com/playlist?list=PLHhitGId-8__Axy6uacn8BCbYjaXANXvS",
    "Production BH2ND": "https://youtube.com/playlist?list=PLHhitGId-8_8WSp0-1ZRQOPTEmrzYP1l7",
    "Hearts Chase": "https://youtube.com/playlist?list=PLHhitGId-8_-qN8hVnfORFmmanYP3jSkB",
    "Daily BH2ND": "https://youtube.com/playlist?list=PLHhitGId-8_8Nad5Dc8ManzhEKDkRuocT",
    "2025 Holiday Vlogs": "https://youtube.com/playlist?list=PLHhitGId-8__gcNOZQPcYfNveOb81iq32",
    "2026 Holiday Vlog": "https://youtube.com/playlist?list=PLHhitGId-8_8TW3vys4E3FzvSv_9MdzBZ",
    "둘셋하투하": "https://youtube.com/playlist?list=PLHhitGId-8_96Mutvd_sIurOZ9ueBrL-3",
}

ydl_opts = {
    "quiet": False,
    "skip_download": True,
    "extract_flat": "discard_in_playlist",
}

videos = []

with YoutubeDL(ydl_opts) as ydl:

    for category, playlist_url in PLAYLISTS.items():

        print(f"\n[{category}] 수집 시작")

        try:
            playlist = ydl.extract_info(
                playlist_url,
                download=False
            )

            entries = playlist.get("entries", [])

            count = 0

            for entry in entries:

                if not entry:
                    continue

                video_id = entry.get("id")

                if not video_id:
                    continue

                title = entry.get("title", "")

                videos.append({
                    "videoId": video_id,
                    "title": title,
                    "date": "",
                    "category": category
                })

                count += 1

            print(f"{category}: {count}개")

        except Exception as e:

            print(f"{category} 오류:")
            print(e)


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        videos,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"\n총 {len(videos)}개 영상 수집")