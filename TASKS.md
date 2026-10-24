# 官網結構整合（2026-10-24）

圖解：https://claude.ai/artifact/SzRj9xc5BRMabNY61tWSiR
主軸：四個方向排成一條流程「看得到→讀得懂→判得準→到得了」，顏色沿用成員島四條光路（藍／橘／粉／綠），疾病案例當橫線貫穿研究頁與合作頁。
上線：commit 81ebc7f（主改）＋ dfa02ab（首頁流程列跨欄修正），Actions 皆成功。

## 研究結構
- [x] R1 首頁四卡加流程列＋動詞色標，AI 與內視鏡順序對調（features.html、_index.md ×2、data/stations.json）
- [x] R2 疾病案例橫線：研究頁每方向列「用在哪些案例」、合作頁每案例標走到哪幾站（data/cases.json、lab_research.html、collaborations ×2）
- [x] R3 精選論文改四篇、一方向一篇、帶動詞色標（highlights.json、lab_publication_brief.html）
- [x] R4 研究頁底部三個孤立小節收成「延伸閱讀」（research/index.md ×2）
- [x] R5 全片掃描進度說法統一為保守版（collaborations ×2）；J. Microsc.／Lab. Invest. 2026 補進研究頁代表論文

## 成員頁
- [x] M1 成員島搬到成員頁頂端當總覽（people/index.md ×2）
- [x] M2 每人卡片加光路色標（authors 前置資料 station 欄 ×12×2、lab_people.html）
- [x] M3 雙向連結：島上「成員頁介紹」→跳卡片（target=_top）；卡片「在成員島看他」→postMessage 讓島選中他
- [x] M4 老師段落縮為兩段＋連結（authors/guan-yu-zhuo `<!--more-->`、lab_people.html 用 .Summary）
- [x] M5 校友區：涴鈞、Wei-Hsun Wang 前置資料 alumni: true，分組進「校友」
- [x] M6 缺頭像改灰色人形剪影（components/zl_silhouette.html）

## 其他
- [x] 成員島四條光路名稱加動詞；主檔 projects\member-island 與 static 已同步
- [x] 研究地圖頂端路線膠囊加對應色點
- [x] 首頁「認識團隊」加成員島連結
- [x] commit + push，Actions 成功，Edge 截線上頁驗證（首頁、研究、合作、成員、英文首頁）
- [x] 第二次部署後再截首頁確認流程列跨欄（OK）
- [x] 手機寬度：10/24 用 Chrome 把線上 9 頁放進 390 px 框實測，全部沒有橫向溢出；首頁流程列自動換行、四卡疊成一欄，沒被切。先前 Edge 無頭截圖被切是無頭模式假象（實體手機未看）
- [x] 研究地圖頁、成員島 postMessage 實際點擊：10/24 Chrome 線上實點。卡片「在成員島看他」→島選中黃柏翰；島「成員頁介紹」→跳到 #member-po-han-huang 卡片；研究地圖點站別，3D 與右側卡片會換

## 網址與鏡像（10/24 決定）
- [x] 正式網址先維持 GitHub Pages（ewinkuo1-sudo.github.io/zhuo-lab-site/），baseURL 不動
- [x] Cloudflare 鏡像保留：使用者 10/24 加好 CLOUDFLARE_API_TOKEN；第一次部署因 wrangler-action 預設 3.90 不支援純靜態設定而失敗，publish.yaml 指定 wranglerVersion "4" 後成功。workers.dev 首頁、中英成員頁、研究地圖、成員島都 200 且是新版

## 第二輪改善（10/24 使用者同意做）
- [x] I1 成員島日間模式：嵌在成員頁固定淺色；單獨開時跟系統＋切換鈕；成員頁 iframe 黑底改掉（people ×2）
- [x] I2 成員島手機寬度兩個 .lab 區塊超出 4–32 px（其實是 3D 畫布邊緣的名字標籤被切，整頁沒溢出；改成標籤夾在畫布內）
- [x] I3 成員島英文版（英文成員頁嵌英文）
- [x] I4 研究地圖英文版（英文選單「Research Map (中文)」改指英文版）
- [x] I5 主檔與官網 static 同步、push、線上驗證（英文成員頁嵌英文淺色島、卡片→島選中 Po-Han Huang；英文研究地圖 /research-map/en/；中英選單連結正確；GitHub Pages＋Cloudflare 都部署成功）
- [x] 研究地圖路線色點原本只改在官網副本，被英文版覆蓋掉 → 已搬回 research-map 原始檔重建（以後改研究地圖只改原始檔）
- [ ] 手機上成員島標籤仍很擠（桌子縮太小，原本就有），之後可考慮手機預設關標籤或拉近鏡頭
- [ ] 研究地圖英文段落用官網 research.json 英文原文，比中文版改寫保守；起點／終點卡、介面字、教材說明的英文是 Claude 寫的，待老師看
- [x] 手機選單地球圖示旁的下拉箭頭黏在一起像破圖 → lg 以下隱藏箭頭（template.scss）
- [x] Cloudflare 鏡像成員島 iframe 破圖：主題產生的 _headers 是 X-Frame-Options: DENY → layouts/index.headers 覆寫成 SAMEORIGIN

## 下一步：全面找問題（10/24 使用者說下次做）
兩個網址都要測：GitHub Pages 與 Cloudflare 鏡像（鏡像有 _headers，行為可能不同，10/24 就是鏡像才出 iframe 破圖）。
- [x] Q1 全站連結（10/24 兩網址各爬全站）：唯一 404 是研究地圖英文版切換鈕原始 href（en/en/），已修；21 個 DOI 用 doi.org handle API 全部有效（直接 curl 出版社會 403，是擋爬蟲）；中文錨點與 #article-journal 是爬蟲誤報
- [x] Q2 版面：25 頁 × 4 寬度用 iframe 量，無橫向溢出、無破圖；修了語言選單箭頭被滑過底線拉成橫槓（使用者抓到）、手機展開選單底部加分界
- [x] Q3 嵌入頁：卡片→島（選中＋捲動）、島→卡片（target=_top）都正常；研究地圖中英手機寬度正常；成員島嵌入時隱藏自己的標題說明（成員頁上方已有同一段）
- [x] Q4 主控台：11 個主要頁面零錯誤、無 4xx 資源；拿掉沒用的 Decap CMS 外掛（首頁少載 234 KB netlify-identity）
- [x] Q5 內容：中英成員職稱／光路一致；中文頁 meta description 原本是英文，已修；頁面原始碼裡的 TODO(老師確認) 註解移到 TODO_老師確認.md
- [ ] Q7 待使用者決定：中文首頁大標仍是英文「Translational Biophotonics Laboratory」與 NYCU 眉標（正式中文名稱待老師）（成員島手機標籤重疊：10/24 已改成 ≤480 px 預設關標籤、只顯示點到的人）
- [ ] Q6 手機實機：請使用者用手機看一輪（或 USB 偵錯接 chrome://inspect）

## 要老師確認
- 全片掃描到底是「進行中」還是「待確認」（兩頁現在都寫保守版）
- 老師成員頁段落縮短是否同意（完整版在個人頁）
- 光片顯微鏡要不要公開列為發展中方向（目前只放延伸閱讀；國科會計畫未送）
- 每人屬哪條光路（目前照成員島填；添至無標籤）
- Lab. Invest. 2026 口腔癌是否算 AI 方向代表作（已放 AI 代表論文與精選論文「判得準」）

- [x] 成員島說明欄可收合、桌子放大（10/24 使用者回饋，已上線）
