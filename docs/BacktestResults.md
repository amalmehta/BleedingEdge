# Backtest Results (generated)

Window 04 Jan 2021 – 29 Dec 2025, 65 four-week windows. Signals used: arxiv, github, funding. Not yet used (need API keys): citations, labs.

All thresholds are invented starting parameters from BleedingEdge.md.

## (a) Lead on the test topics (lead weights untuned, all 1)

| Topic | First heating-up flag | Research crowd arrives | Lead | ≥ 8 weeks? | arXiv-only baseline lead | First HN story ≥50 pts |
|---|---|---|---|---|---|---|
| RL for LLM reasoning (GRPO / RLVR) | Dec 2024 (trend) | Apr 2025 | 16 wk | yes | 16 wk | Jan 2025 |
| Diffusion policies | Jan 2024 (burst) | May 2024 | 16 wk | yes | 16 wk | — |
| Vision-language-action models | Jun 2024 (trend) | May 2025 | 48 wk | yes | 52 wk | Dec 2024 |

**Criterion (a): passes** (needs ≥ 2 of 3 topics with a lead of ≥ 8 weeks).

![RL for LLM reasoning (GRPO / RLVR)](img/backtest-grpo_rlvr.png)
![Diffusion policies](img/backtest-diffusion_policy.png)
![Vision-language-action models](img/backtest-vla.png)

## Lead weights

Share of test topics where the signal on its own rose ≥ 8 weeks before the research crowd arrived. Topics that never reached consensus can't be judged and are left out.

| Signal | First own rise, per test topic | Lead weight |
|---|---|---|
| arxiv | grpo_rlvr: Dec 2024, diffusion_policy: Jan 2024, vla: May 2024 | 1.00 |
| github | grpo_rlvr: —, diffusion_policy: Feb 2024, vla: Feb 2025 | 0.67 |
| funding | grpo_rlvr: Feb 2024, diffusion_policy: —, vla: Jul 2021 | 0.67 |

## (b) Precision on workshop-title candidates, 2024

| Method | Flags (topic-windows) | Reached consensus in 12 months | Precision | Distinct topics flagged | Distinct topic precision |
|---|---|---|---|---|---|
| untuned | 16 | 1 | 6% | 12 | 8% |
| tuned | 16 | 1 | 6% | 12 | 8% |
| baseline arxiv only | 77 | 1 | 1% | 28 | 4% |

**Criterion (b): fails** (needs precision ≥ 50% with tuned lead weights).

## Queries behind every count

Each test topic's counts come from these queries (first page shown; the code paginates and splits date ranges).

**RL for LLM reasoning (GRPO / RLVR)**
- arXiv "group relative policy optimization": https://export.arxiv.org/api/query?search_query=%28ti%3A%22group%20relative%20policy%20optimization%22%20OR%20abs%3A%22group%20relative%20policy%20optimization%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- arXiv "verifiable rewards": https://export.arxiv.org/api/query?search_query=%28ti%3A%22verifiable%20rewards%22%20OR%20abs%3A%22verifiable%20rewards%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- arXiv "GRPO": https://export.arxiv.org/api/query?search_query=%28ti%3A%22GRPO%22%20OR%20abs%3A%22GRPO%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- GitHub "verifiable rewards" (2021 slice): https://github.com/search?type=repositories&q=%22verifiable+rewards%22+in%3Aname%2Cdescription+created%3A2021-01-04..2021-12-31
- HN "GRPO": https://hn.algolia.com/api/v1/search_by_date?query=%22GRPO%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0
- HN "verifiable rewards": https://hn.algolia.com/api/v1/search_by_date?query=%22verifiable+rewards%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0
- HN "group relative policy optimization": https://hn.algolia.com/api/v1/search_by_date?query=%22group+relative+policy+optimization%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0

**Diffusion policies**
- arXiv "diffusion policy": https://export.arxiv.org/api/query?search_query=%28ti%3A%22diffusion%20policy%22%20OR%20abs%3A%22diffusion%20policy%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- arXiv "diffusion policies": https://export.arxiv.org/api/query?search_query=%28ti%3A%22diffusion%20policies%22%20OR%20abs%3A%22diffusion%20policies%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- GitHub "diffusion policy" (2021 slice): https://github.com/search?type=repositories&q=%22diffusion+policy%22+in%3Aname%2Cdescription+created%3A2021-01-04..2021-12-31
- HN "diffusion policy": https://hn.algolia.com/api/v1/search_by_date?query=%22diffusion+policy%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0
- HN "diffusion policies": https://hn.algolia.com/api/v1/search_by_date?query=%22diffusion+policies%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0

**Vision-language-action models**
- arXiv "vision-language-action": https://export.arxiv.org/api/query?search_query=%28ti%3A%22vision-language-action%22%20OR%20abs%3A%22vision-language-action%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- arXiv "VLA model": https://export.arxiv.org/api/query?search_query=%28ti%3A%22VLA%20model%22%20OR%20abs%3A%22VLA%20model%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- arXiv "VLA models": https://export.arxiv.org/api/query?search_query=%28ti%3A%22VLA%20models%22%20OR%20abs%3A%22VLA%20models%22%29%20AND%20submittedDate%3A%5B202101040000%20TO%20202512292359%5D&start=0&max_results=1000&sortBy=submittedDate&sortOrder=ascending
- GitHub "vision-language-action" (2021 slice): https://github.com/search?type=repositories&q=%22vision-language-action%22+in%3Aname%2Cdescription+created%3A2021-01-04..2021-12-31
- GitHub "VLA model" (2021 slice): https://github.com/search?type=repositories&q=%22VLA+model%22+in%3Aname%2Cdescription+created%3A2021-01-04..2021-12-31
- HN "vision-language-action": https://hn.algolia.com/api/v1/search_by_date?query=%22vision-language-action%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0
- HN "VLA model": https://hn.algolia.com/api/v1/search_by_date?query=%22VLA+model%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0
- HN "VLA models": https://hn.algolia.com/api/v1/search_by_date?query=%22VLA+models%22&tags=story&typoTolerance=false&restrictSearchableAttributes=title&numericFilters=points%3E%3D50%2Ccreated_at_i%3E%3D1609718400%2Ccreated_at_i%3C1766966400&hitsPerPage=1000&page=0
