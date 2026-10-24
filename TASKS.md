# 官網結構整合（2026-10-24）

圖解：https://claude.ai/artifact/SzRj9xc5BRMabNY61tWSiR
主軸：四個方向排成一條流程「看得到→讀得懂→判得準→到得了」，顏色沿用成員島四條光路（藍／橘／粉／綠），疾病案例當橫線貫穿研究頁與合作頁。

## 研究結構
- [ ] R1 首頁四卡加流程列＋動詞色標，AI 與內視鏡順序對調（features.html、_index.md ×2、data/stations.json）
- [ ] R2 疾病案例橫線：研究頁每方向列「用在哪些案例」、合作頁每案例標走到哪幾站（data/cases.json、lab_research.html、collaborations ×2）
- [ ] R3 精選論文改四篇、一方向一篇、帶動詞色標（highlights.json、lab_publication_brief.html）
- [ ] R4 研究頁底部三個孤立小節收成「延伸閱讀」（research/index.md ×2）
- [ ] R5 全片掃描進度說法統一為保守版（collaborations ×2）；合作頁提到的 J. Microsc.／Lab. Invest. 2026 補進研究頁代表論文

## 成員頁
- [ ] M1 成員島搬到成員頁頂端當總覽（people/index.md ×2）
- [ ] M2 每人卡片加光路色標（authors 前置資料 station 欄 ×12×2、lab_people.html）
- [ ] M3 雙向連結：島上點人→跳卡片；卡片「在成員島看他」→島選中他（island index.html、lab_people.html）
- [ ] M4 老師段落縮為兩段＋連結（authors/guan-yu-zhuo `<!--more-->`、lab_people.html）
- [ ] M5 校友區：涴鈞、Wei-Hsun Wang 標 alumni（authors 前置資料、lab_people.html）
- [ ] M6 缺頭像改灰色人形剪影（lab_people.html、SCSS）

## 其他
- [ ] 成員島四條光路名稱加動詞，與官網一致；主檔與 static 同步
- [ ] 研究地圖頂端路線膠囊加對應色點
- [ ] 首頁「認識團隊」加成員島連結
- [ ] commit + push，看 Actions 成功，Edge 截線上頁驗證
- [ ] 最後一輪細節檢查（沒考慮到的事）

## 要老師確認
- 全片掃描到底是「進行中」還是「待確認」
- 老師段落縮短是否同意
- 光片顯微鏡要不要公開列為發展中方向（目前只放延伸閱讀）
- 每人屬哪條光路（目前照成員島填）
