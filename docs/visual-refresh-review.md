# 配色、直角與留白改版 — 2026-09-11

依 `NEXT_SESSION_PLAN.md` 與使用者追加的全站直角、避免擁擠要求完成。

## 已完成

- 統一深藍、青綠與暖白；研究區淡藍灰、活動區淡杏、招生區深藍。
- 暖橘實際採 `#AA4430`、琥珀採 `#955C12`，比計畫起始色略深，以確保小字對比。
- 語意色集中於 SCSS，與 Hugo 主題同步；連結、按鈕、選單與焦點狀態統一。
- 全站直角，包含卡片、按鈕、照片框、選單、地圖控制及個人頁頭像。保留原 logo 圖案。
- 內容最大寬度 1040 px；1440 px 螢幕兩側各 200 px 留白；手機至少 24 px。長文容器上限 760 px。
- 研究卡桌面兩欄、手機一欄；成員桌面三欄，窄手機使用照片在左、文字在右的單欄摘要卡。
- 加大卡片間距與標題留白；來源小字提高至 .76rem，科學圖仍完整顯示。
- 修正 Bootstrap 按鈕焦點樣式蓋掉鍵盤外框的問題，深色區使用淺色外框。
- 截圖前等待圖片解碼；完整頁面截圖另先捲動以觸發載入，區塊截圖暫藏固定導覽避免遮擋。

## 驗證

- Hugo 0.135.0 extended 建置成功。
- `check_home_redesign.py`：17 組頁面／尺寸、46 個站內網址，零失敗；首頁 12 位成員摘要與主持人、People 13 位完整介紹均保留。
- `check_visual_refresh.py`：52 組頁面／尺寸，零失敗。
- 首頁涵蓋 1920、1440、1024、768、390、320 px，中英文皆檢查。
- People、Research、Gallery、News、Publications、主持人／Jackson 個人頁、Join、Contact、Facilities 另檢查 1440／320 px。
- 全部受測頁面無橫向溢出、圖片失效或殘留圓角，主要內容容器符合寬度與留白限制。
- 桌面與窄手機共 4 組雙語互動檢查：語言切換、搜尋輸入與結果、Escape 關閉、Tab 焦點；窄手機另驗證選單捲動。
- 20 組實際渲染前景／背景對比（含主要按鈕 hover／focus），最低 4.95:1。這是代表性檢查，非整站無障礙認證。
- 人工檢視桌面／手機的首頁主視覺、研究、論文、成員、活動及招生截圖；未修改科學影像原檔、圖中文字與比例尺。
- `git diff --check` 通過。

## 證據與重跑

- 視覺報告與前後截圖：`C:/Users/ewink/.cache/zhuo-site-review/square-color-review/`
- 回歸檢查：`C:/Users/ewink/.cache/zhuo-site-review/square-color-regression/checks.json`
- 中英文各保存 1440／390 px 的 before／after 全頁截圖，以及各重點區塊截圖。
- `en-comparison-overview.png`、`zh-comparison-overview.png` 為桌面前後總覽。
- 本機建置目的地：`C:/Users/ewink/.cache/zhuo-site-review/square-color-public/zhuo-lab-site/`，baseURL 為 `http://127.0.0.1:18766/zhuo-lab-site/`。
- 使用 `scripts/check_visual_refresh.py --root BUILD_PARENT --output REVIEW_DIR --before PREVIOUS_BUILD_PARENT` 重跑；程式會啟動並結束本機伺服器。

## 尚待來源確認

仍缺 5 位成員照片、5 張原有影像的科學圖說、部分姓名／身分確認、正式中文實驗室名稱、儀器資料。探頭與 AI 研究卡保留概念示意標記。本輪沒有新增研究成果或人物事實。
