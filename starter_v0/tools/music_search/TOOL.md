---
name: music_search
track: bonus
kind: live_api
provider: iTunes Search API
requires_env: []
inputs: [query, max_results]
outputs: [items]
side_effect: false
---
# music_search

Tìm kiếm bài hát / nhạc qua iTunes Search API. Trả về tên bài hát, nghệ sĩ, album, link. Miễn phí, không cần API key.
