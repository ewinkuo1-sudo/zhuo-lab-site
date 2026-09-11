# 首頁大背景與研究內頁同步紀錄

日期：2026-09-11。起始版本：`1cfd4fa2024ceae8433fc8df7e24f69572fb8b41`，開始時遠端 main 與本機 HEAD 一致。
交付狀態：本機修改與預覽完成，使用者於 2026-09-11 授權提交與發布。實際部署版本與結果以 [GitHub Pages 工作流程](https://github.com/ewinkuo1-sudo/zhuo-lab-site/actions/workflows/publish.yaml) 為準；線上驗證另記於本輪快取目錄的 `online-checks.json`。開始時已有的 `NEXT_SESSION_PLAN.md` 修改與未追蹤的 `FUTURE_ROADMAP.md` 已保留並延續更新。

## 完成內容

- 中英文首頁首圖改為背景層，桌面圖片延伸至頁面邊緣；文字疊在深藍漸層前。手機另行安排背景與文字空間，未強制填滿視窗高度。
- 背景以 `object-fit: contain` 等比例呈現完整圖框。原始影像沒有裁切、改色或重新生成，另提供直接查看完整原圖和 Gallery 的入口；首頁漸層只用於呈現與文字可讀性。
- 文字內容仍遵循 1040 px 上限、手機至少 24 px 留白；保留直角及深藍／青綠／暖白配色。
- 四個研究方向共用首頁名稱、順序、圖片、圖源與舊網址片段；內頁以問題、方法、已發表發現／技術背景、論文、研究狀態與洽詢入口組織。
- 前兩個方向沿用已有論文原圖與 CC BY 4.0，探頭與 AI 維持清楚標示的概念圖；不以模擬結果代表實驗或實機。
- 歷史成果與長期目標、待確認進度分開；2025 食道研究包含 H&E 染色切片的限制已明示。來源與草稿改寫理由見 [來源核對](research-content-audit.md)。
- 首頁主要區塊順序維持不變，仍有 12 位成員摘要、1 位主持人，People 頁保持 13 位完整介紹。
- `TODO_老師確認.md` 加入可逐項回覆的問題；`FUTURE_ROADMAP.md` 更新完成狀態與未來 session 工作順序，README、舊 session 計畫均加上入口。

## 驗證

- Hugo 0.135.0 extended 建置通過，使用 GitHub Pages 專案子路徑 `/zhuo-lab-site/`。
- 既有 `scripts/check_home_redesign.py`：17 個頁面／尺寸組合、47 個站內網址，0 failures；包含首頁圖片、錨點、成員數、窄版選單導覽與主要內頁。
- 最終版補充檢查：320、390、768、1024、1440 px × 中英文首頁／研究頁，共 20 個組合、研究頁 19 個站內網址，0 failures。
- 檢查研究頁四個標題及網址與首頁逐一相符、兩筆 CC BY 圖源、圖片比例、無破圖、無橫向溢出、手機留白、CTA／原圖／Gallery 鍵盤焦點與連結。
- 文字對比以暫時隱藏文字、擷取實際影像背景，取文字行區域內每 3 px 的像素樣本計算。一般文字最小 **4.8:1**（門檻 4.5:1），大型文字最小 **7.85:1**（門檻 3:1）。這是本輪首圖抽樣檢查，不是全站無障礙認證。
- 首圖原檔 SHA-256 與 `gallery-sources.json` 一致。`git diff --check` 通過。
- 已人工檢視中英文桌面／手機主視覺、320 px 窄版，以及研究內頁桌面／手機圖片與段落；最後調整圖源連結整段換行及研究圖說靠左。

## 本機預覽與紀錄

預覽服務啟動後可開啟 [中文首頁](http://127.0.0.1:18766/zhuo-lab-site/zh/)、[中文研究](http://127.0.0.1:18766/zhuo-lab-site/zh/research/)、[英文首頁](http://127.0.0.1:18766/zhuo-lab-site/)、[英文研究](http://127.0.0.1:18766/zhuo-lab-site/research/)。此為本機預覽，與線上部署分開。

檔案位於 `C:\Users\ewink\.cache\zhuo-site-review\research-hero-review\`：

- `checks.json`：既有回歸檢查。
- `detail-checks.json`、`check_details.py`：本輪補充檢查結果及重跑腳本（使用本機 18767 port）。
- `zh-final-hero-1440.png`、`zh-final-hero-390.png`、`zh-final-hero-320.png`：首頁大背景；同目錄亦有英文與其他尺寸。
- `zh-research-page-1440.png`、`zh-research-page-390.png`：研究完整內頁。
- `zh-research-detail-390.png`、`en-research-detail-1440.png`：研究方向區塊細節。
- 改版前參考仍保留在同層 `square-color-review/`；本輪沒有覆寫既有截圖。

重建：

```powershell
$env:PATH = 'C:\Users\ewink\.cache\zhuo-site-tools\go\go\bin;' + $env:PATH
& 'C:\Users\ewink\.cache\zhuo-site-tools\hugo\hugo.exe' --minify --baseURL 'http://127.0.0.1:18766/zhuo-lab-site/' --destination 'C:\Users\ewink\.cache\zhuo-site-review\research-hero-public\zhuo-lab-site'
& 'C:\Users\ewink\AppData\Local\Programs\Python\Python312\python.exe' -X utf8 'C:\Users\ewink\.cache\zhuo-site-review\research-hero-review\check_details.py'
```

既有回歸腳本會自行佔用 18766 port；重跑前先確認預覽服務是否還在，不要任意停止未知程序。所有驗證結果是本機結果。

## 後續

下一 session 優先核對儀器頁未確認的能力／開放使用敘述，以及書目年份和出版狀態差異。研究進度、五位缺照片與五張缺正式圖說仍待老師／成員提供資料；詳見 [未來規劃](../FUTURE_ROADMAP.md) 與 [待確認清單](../TODO_老師確認.md)。
