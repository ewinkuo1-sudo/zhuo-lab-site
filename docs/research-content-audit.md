# 研究內容與待確認資料核對

日期：2026-09-11。起始版本：`1cfd4fa2024ceae8433fc8df7e24f69572fb8b41`。
範圍：首頁、四個研究方向、既有圖片與代表論文；不把文獻報告視為目前實驗室設備清單。

## 已核對來源與採用範圍

| 來源 | 本輪採用 | 限制／處理 |
|---|---|---|
| [Zhuo et al., 2021；NYCU 作者機構摘要](https://scholar.nycu.edu.tw/en/publications/label-free-multimodal-nonlinear-optical-microscopy-for-biomedical/)；[DOI](https://doi.org/10.1063/5.0036341) | 多模態平台結合 SHG、TPF、FLIM、CARS 的技術背景。 | 摘要不足以支持所有通道一次同步取像或目前設備能力；不能當作內視探頭完成證據。 |
| [Makkithaya et al., 2025；期刊全文](https://www.nature.com/articles/s41598-025-13910-7) | 食道組織 SHG／TPF、GLCM 特徵、SVM 分類；圖 2。 | Methods 與圖說包含 H&E 染色切片；不稱此圖為全數未染色樣本。只描述研究資料集結果，不擴大成臨床診斷能力。 |
| [Makkithaya et al., 2024；全文／作者稿](https://pmc.ncbi.nlm.nih.gov/articles/PMC11062753/)；[DOI](https://doi.org/10.1063/5.0196676) | 正常、OA、RA 軟骨的 P-SHG 與定量參數差異；圖 3。 | 代表圖為 OA 軟骨，沒有把整篇結果當作全部在同一張圖裡。 |
| [Karnati et al., 2026；NYCU 作者機構摘要](https://scholar.nycu.edu.tw/en/publications/integration-of-deep-learning-and-machine-learning-for-label-free-/)；[DOI](https://doi.org/10.1109/JPHOT.2026.3701723) | 雙光子口腔病灶影像的深度學習與機器學習分類；明示前導研究。 | 已核對摘要與出版狀態，未取得期刊全文；不加入泛化效能、臨床部署或全片自動化宣稱。 |
| `content/en/publication/mazumder-2017-polarization/`、`chakraborty-2022-synthesis/` | 偏振方法與澱粉基生物塑膠的延伸閱讀。 | 沿用既有書目和題名層次，不新增細部結果。 |

圖片來源與 SHA-256 沿用 `homepage-figure-sources.json`、`gallery-sources.json`。前兩張論文圖保留完整比例、標記、來源與 CC BY 4.0；探頭、AI 保留明示概念圖。首圖 `lab-04.png` 原檔與色彩資料未改，深藍漸層只屬首頁呈現，完整原圖可直接開啟。

## 舊草稿處理

- 「一次掃描同時取得所有通道」改為已發表平台的方法描述，取像配置需依實驗確認。
- 微型探頭、非侵入式診斷與雷射治療原被寫成正在執行的工作；改為微型化長期方向，移除未核實治療承諾。
- 全片掃描、病理量化分數、AI 全面使用、Claude 日常工作及完全無人工步驟的流程缺少足夠來源，移至待確認問題，不在研究頁陳述為事實。
- 單顆粒／病毒超高速觀察與其他未附來源的研究線，改以完整論文清單與洽詢入口引導。原草稿可從起始版本的研究頁追溯。
- 既有四個方向及附加段落的網址片段保留。首頁英文 ECM 名稱展開成與內頁相同的全名，原網址片段不變。
- 各段以「已發表」和「長期／待確認進度」區分；尚未收到老師的研究狀態核可。

## 下一輪最需確認的事實

1. **儀器頁**：目前仍寫有「受訓即可使用」、SHG/THG/TPF 同步、偏振偵測、FV300 反射能力、頻域 FLIM 與相干拉曼、冷凍切片及 GPU；這些都未由本輪來源證實為現在的配置。下輪先核對，未有來源時改為洽詢式描述。
2. **人物與聯絡**：正式中文名稱、職稱／履歷、姓名拼法、電話與房號、成員分類與照片同意待本人確認。
3. **影像**：lab-01、03、04、05、06 的正式圖說，以及五位成員缺照，皆尚待資料。
4. **書目**：2010 作者身分及收錄範圍待核對。另本次 NYCU 頁面將 `wu-2026-mechanically` 對應成果列為 2027、`rodrigues-2026-advancing` 列 accepted/in press；只列為下一輪出版年／狀態核對項，不在本輪批次改動書目或消息。

完整可回覆問題見根目錄 `TODO_老師確認.md`。未有來源不勾選「事實已確認」。

## 維護方式

首頁 `content/en/_index.md`、`content/zh/_index.md` 的 research items 是主題名稱、排序、圖片、圖源與網址的來源；`research_key` 對應 `data/research.json` 中的雙語說明與論文 slug。`lab_research.html` 讀取它們產生內頁，論文題名／年份／DOI 直接沿用既有英文書目，中文頁明示此去向。新增或改動方向時需一起維護兩語 key，並保留已公開網址。
