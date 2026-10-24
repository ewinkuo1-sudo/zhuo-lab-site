---
title: 臨床合作
date: 2026-09-06
type: landing

sections:
  - block: markdown
    content:
      title: 臨床合作
      subtitle: 真實組織、真實診斷問題
      text: |
        實驗室每一項影像方法都是對著臨床醫師與病理科醫師帶來的問題發展的。每個案例都走在同一條[研究流程](../research/)上：先用光看到組織、再變成數字、交給 AI 判讀、最後往體內送。下面每個案例標出它目前走到哪幾站，點色標可回到該方向的說明。

        ### 食道癌：不染色也能評估基質 {#esophagus}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#無標記非線性光學顯微"><i></i><b>看得到</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#膠原蛋白手性與細胞外基質定量"><i></i><b>讀得懂</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-輔助無標記病理"><i></i><b>判得準</b></a><a class="zl-station zl-station-goal" style="--st:#009E73" href="../research/#微型化非線性內視顯微術"><i></i><b>到得了</b><small>長期目標</small></a></p>

        **問題。** 病灶周圍的細胞外基質，能否在病理醫師看 H&E 之前，就區分鱗狀細胞癌與高度分化不良？
        **我們做的。** 對未染色切片做雙光子與 SHG 取像，抽取紋理特徵，訓練機器學習分類器。
        **合作。** 高雄醫學大學附設醫院腸胃科與病理科。
        **狀態。** 已發表（*Sci. Rep.* 2025）；全片掃描為後續方向，進度待確認。

        ### 軟骨疾病：退化性關節炎與類風濕性關節炎 {#cartilage}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#無標記非線性光學顯微"><i></i><b>看得到</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#膠原蛋白手性與細胞外基質定量"><i></i><b>讀得懂</b></a></p>

        **問題。** 膠原纖維的排列與手性，能否區分正常、退化性與類風濕性軟骨？
        **我們做的。** 極化解析 SHG、χ33/χ31 與線偏振度圖。
        **合作。** 中國醫藥大學附設醫院風濕免疫科與骨科。
        **狀態。** 已發表（*APL Bioeng.* 2024）。

        ### 口腔癌：最差侵犯型態 {#oral}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#無標記非線性光學顯微"><i></i><b>看得到</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-輔助無標記病理"><i></i><b>判得準</b></a><a class="zl-station zl-station-goal" style="--st:#009E73" href="../research/#微型化非線性內視顯微術"><i></i><b>到得了</b><small>長期目標</small></a></p>

        **問題。** 一個肉眼難以評分的預後指標，能否從無標記多光子影像量化？
        **我們做的。** 對腫瘤前緣做多光子取像，結合深度學習分類。
        **合作。** 頭頸部病理科合作者。
        **狀態。** 已發表（*Lab. Invest.* 2026）。

        ### 病理醫師可以稽核的膠原蛋白病理分數 {#collagen-score}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#E69F00" href="../research/#膠原蛋白手性與細胞外基質定量"><i></i><b>讀得懂</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-輔助無標記病理"><i></i><b>判得準</b></a></p>

        **問題。** 膠原蛋白相關病理能否變成可重複的數字，而不是目測分級？
        **我們做的。** 定量 SHG 指標與機器學習，並把結果與來源影像並列，讓推論可被檢視。
        **狀態。** 已發表（*J. Microsc.* 2026）；持續進行。

        ## 資料與 ground truth
        每項研究都使用同一蠟塊的**相鄰 5 µm 切片**：一片做 H&E 染色並由病理醫師標註作為 ground truth，另一片不染色供無標記多光子成像。分類器只對照這份標註訓練與測試，因此每個結論都能追溯到病理醫師對同一塊組織的判讀。

        ## 合作怎麼進行
        1. 你帶來診斷問題與組織來源（新鮮、冷凍或 FFPE 未染色切片）。
        2. 我們在多光子平台上做無標記取像，並與你一起建立分析流程。
        3. 結果對照你的 ground truth 驗證，共同撰寫發表。

        有興趣做先導研究的臨床與病理醫師，請[與我們聯絡](../contact/)。

        <!-- TODO(老師確認): 各合作案的醫院、科別、醫師姓名與可否公開；進行中未發表案子要不要列；食道癌全片掃描目前是「進行中」還是「規劃中」（2026-10-24 統一改成保守寫法，與研究頁一致）。 -->
    design:
      columns: '1'
---
