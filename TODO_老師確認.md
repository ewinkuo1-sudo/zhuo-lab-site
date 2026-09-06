# 上線前要老師確認的項目（2026-09-06）

網站骨架與文字已寫好，以下是「我猜的」或「查不到的」，上線前要老師拍板。搜 `TODO(老師確認)` 可找到檔內對應位置。

## 命名與網址
- [ ] 實驗室正式名稱（中／英／縮寫）。目前暫用「Zhuo Lab」／「卓冠宇實驗室」，沒用 TBL（跟 Tulane 撞名）。改 `config/_default/hugo.yaml` 的 `title` 與 `languages.yaml` 的 zh `title`。
- [ ] 網址：`<org>.github.io` 免費，或自購網域，或 `*.nycu.edu.tw`。決定後改 `hugo.yaml` 的 `baseURL`。
- [ ] GitHub Organization 由誰建、老師要不要當 owner。

## 內容
- [ ] 首頁標語「Seeing tissue without labels／不染色，直接看見組織」是我寫的，老師可換。
- [ ] 研究頁四個方向的敘述，依所方個人頁三條研究領域 + 兩篇通訊作者論文寫成，請老師修正。
- [ ] 研究頁每個方向缺一張自己的代表影像（P-SHG 膠原蛋白／SHG-CD／CARS-FLIM），放 `assets/media/`。
- [ ] Facilities 頁目前是佈局範例，儀器清單、規格、照片、經費標示全部待補；高甫仁老師移轉的貴儀要不要列。
- [ ] 成員：目前只有老師本人。學生名單、照片、入學年、Alumni 與去向。
- [ ] 老師頭像暫時抓所方網站 2026-01 上傳的那張，要不要換。
- [ ] Join Us 的招生文字：公開 email 或改表單；具體背景要求；要不要列合作醫師。
- [ ] 聯絡頁電話、地址、房號抄自所方個人頁，請確認。

## 論文
- [ ] `publications.bib` 目前 21 篇（Google Scholar 前 15 + Academic Hub 最新 6），DOI 由 Crossref 比對。要不要改成全列或只放精選。
- [ ] 後續維護方式：老師丟 Zotero 群組 → 匯出 .bib 覆蓋 `publications.bib`。要不要建 Zotero 群組。
- [ ] ORCID 目前是空的，建議老師花 30 分鐘授權 Crossref 匯入，之後可自動同步。

## 授權
- [ ] 論文圖多數期刊要授權或只能放縮圖。
- [ ] 成員照片同意公開。

## 論文作者名
- [ ] 2010 J. Struct. Biol.（澱粉 SHG）Crossref 作者掛「Zong-Yan Zhuo」，Google Scholar 列在老師名下。是早期拼法還是不同人？確認後若是老師，把 `publications.bib` 該筆改成 `Zhuo, Guan-Yu`。
