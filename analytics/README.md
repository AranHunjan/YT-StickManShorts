# Performance data

`performance.csv` is filled in by hand from each platform's analytics, one row per episode per platform. `/performance` reads it, together with each episode's hook style, shape, topic type and listening score, and writes recommendations to `docs/INSIGHTS.md`. Nothing here changes how episodes are made until you adopt a recommendation.

Record each episode **7 days after posting** (`measured_after_days` = 7), so episodes are compared at the same age.

| Column | Where to find it (YouTube Studio: the Short, then Analytics) |
|---|---|
| `episode` | The episode number, e.g. `2` |
| `platform` | `youtube`, `tiktok`, `instagram` or `facebook` |
| `posted` | Date posted, `2026-11-08` |
| `views` | Views |
| `viewed_pct` | "Viewed vs. swiped away": the % who chose to watch. This is what the hook decides |
| `avg_pct_viewed` | Average percentage viewed (over 100% means people rewatched) |
| `avg_view_s` | Average view duration in seconds |
| `likes`, `comments`, `shares`, `subs` | Likes, comments, shares, subscribers gained |
| `drop_at_s` | In the retention graph, the second where the biggest drop starts (leave blank if none) |
| `notes` | Anything odd: posted late, a big account shared it, a copyright claim... |

YouTube matters most for the hook test, so fill in YouTube first; the other platforms are optional. Pulling these numbers automatically is possible later (YouTube Analytics API), but needs a Google Cloud sign-in set up on your account (docs/OPEN_QUESTIONS.md).
