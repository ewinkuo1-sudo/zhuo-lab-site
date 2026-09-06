---
title:
date: 2026-09-06
type: landing

sections:
  - block: hero
    content:
      title: |
        不染色，
        直接看見組織
      text: |
        <br>

        我們發展**無標記非線性光學顯微技術**，並把它帶進醫院。
        實驗室位於國立陽明交通大學生醫光電研究所（台北陽明校區），
        以二倍頻（SHG）、雙光子螢光與拉曼對比觀察膠原蛋白、軟骨與腫瘤基質，
        結合機器學習做自動判讀，並將整套流程微型化成內視鏡探頭，用於疾病早期診斷。
      cta:
        label: 研究方向
        url: research/
      cta_alt:
        label: 加入我們
        url: join/
    design:
      background:
        gradient_end: '#1e3a5f'
        gradient_start: '#0b1f33'
        text_color_light: true

  - block: features
    content:
      title: 研究方向
      items:
        - name: 無標記非線性光學顯微
          icon: microscope
          icon_pack: fas
          description: SHG、雙光子螢光、CARS 與 FLIM 整合於同一平台，不需染色、不需固定。
        - name: 膠原蛋白手性與細胞外基質定量
          icon: dna
          icon_pack: fas
          description: 以極化解析 SHG 與 SHG 圓二色性讀出纖維方向與病理變化，應用於癌症與軟骨疾病。
        - name: 微型化非線性內視顯微術
          icon: stethoscope
          icon_pack: fas
          description: 光纖式非線性影像探頭，目標是活體內的即時診斷。
        - name: AI 輔助無標記病理
          icon: brain
          icon_pack: fas
          description: 用機器學習與深度學習把未染色的多光子影像變成診斷判讀，從紋理特徵加 SVM 到端到端神經網路。

  - block: collection
    content:
      title: 近期論文
      text: |
        完整清單請見 [Google Scholar](https://scholar.google.com/citations?user=nF1TaA8AAAAJ)。
      count: 5
      filters:
        folders:
          - publication
    design:
      view: citation
      columns: '1'

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./people/" cta_text="認識成員 →" %}}
    design:
      columns: '1'
---
