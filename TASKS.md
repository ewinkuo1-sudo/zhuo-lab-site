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
- [ ] Cloudflare 鏡像保留：等使用者在 GitHub repo 加 CLOUDFLARE_API_TOKEN 密鑰（10/24 查 gh secret list 為空），加完推一次 commit 觸發部署，再驗 workers.dev 研究地圖不再 404

## 要老師確認
- 全片掃描到底是「進行中」還是「待確認」（兩頁現在都寫保守版）
- 老師成員頁段落縮短是否同意（完整版在個人頁）
- 光片顯微鏡要不要公開列為發展中方向（目前只放延伸閱讀；國科會計畫未送）
- 每人屬哪條光路（目前照成員島填；添至無標籤）
- Lab. Invest. 2026 口腔癌是否算 AI 方向代表作（已放 AI 代表論文與精選論文「判得準」）
