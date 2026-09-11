---
title:
date: 2026-09-06
type: landing

sections:
  - block: hero
    content:
      title: |
        Translational<br>
        Biophotonics<br>
        Laboratory
      cta:
        label: 研究方向
        url: research/
      cta_alt:
        label: 加入我們
        url: join/
      cta_note:
        label: 國立陽明交通大學 生醫光電研究所 · 台北陽明校區
    design:
      background:
        color: '#04201c'
        text_color_light: true

  - block: markdown
    id: lab-stats
    content:
      title:
      text: |
        <div class="zl-stats">
          <div><b>1,490</b><span>總引用數</span></div>
          <div><b>18</b><span>h-index</span></div>
          <div><b>4</b><span>臨床合作案</span></div>
          <div><b>3</b><span>合作醫院</span></div>
        </div>
        <p class="zl-stats-note">資料來源：Google Scholar，2026 年 9 月。</p>
    design:
      columns: '1'
      spacing:
        padding: ['0', '0', '1.5rem', '0']

  - block: markdown
    id: about
    content:
      title: 關於我們
      text: |
        Translational Biophotonics Lab 是由卓冠宇教授領導的前沿研究團隊，隸屬國立陽明交通大學生醫光電研究所。我們致力於開創先進光學影像技術，並將其轉化為癌症診斷與生物醫學探索中具有實質影響力的臨床應用。

        我們專精於波編碼非線性內視顯微術、多模態非線性光學成像，以及無標記成像技術，包括二次諧波產生（SHG）、三次諧波產生（THG）、雙光子激發螢光（TPEF）、拉曼與受激拉曼散射（SRS）。透過整合多光子激發、二次與三次諧波產生，以及偏振解析對比機制，我們以前所未有的精確度，呈現細胞與分子尺度的光與組織交互作用。

        我們的研究串聯基礎光子學與轉譯醫學，實現不需染劑或標記的即時活體組織病理分析。我們聚焦於癌症生物學中的臨床挑戰，包括早期偵測、腫瘤邊界評估，以及透過高解析度、多模態成像理解腫瘤侵犯型態。

        在創新與合作的推動下，實驗室結合光學物理、生物醫學工程與臨床洞見，開發兼具小型化、智慧化與臨床應用能力的下一代診斷工具。
    design:
      columns: '1'

  - block: features
    content:
      title: 研究方向
      items:
        - name: 無標記非線性光學顯微
          image: gen/thumb-multimodal.webp
          image_alt: 模擬多模態顯微影像：SHG 膠原蛋白、雙光子自體螢光與 CARS 脂質對比（示意圖）
          url: research/#無標記非線性光學顯微
          icon: microscope
          icon_pack: fas
          description: SHG、雙光子螢光、CARS 與 FLIM 整合於同一平台，不需染色、不需固定。
        - name: 膠原蛋白手性與細胞外基質定量
          image: gen/thumb-pshg.webp
          image_alt: 模擬極化解析 SHG 膠原纖維方向圖（示意圖）
          url: research/#膠原蛋白手性與細胞外基質定量
          icon: dna
          icon_pack: fas
          description: 以極化解析 SHG 與 SHG 圓二色性讀出纖維方向與病理變化，應用於癌症與軟骨疾病。
        - name: 微型化非線性內視顯微術
          image: gen/thumb-endoscope.webp
          image_alt: 光纖式非線性內視顯微探頭對組織中膠原蛋白取像的示意圖
          url: research/#微型化非線性內視顯微術
          icon: stethoscope
          icon_pack: fas
          description: 光纖式非線性影像探頭，目標是活體內的即時診斷。
        - name: AI 輔助無標記病理
          image: gen/thumb-ai.webp
          image_alt: 模擬無標記組織影像疊加分類器逐格機率圖（示意圖）
          url: research/#ai-輔助無標記病理
          icon: brain
          icon_pack: fas
          description: 用機器學習與深度學習把未染色的多光子影像變成診斷判讀，從紋理特徵加 SVM 到端到端神經網路。

  - block: lab_gallery
    id: gallery
    content:
      title: 研究影像
      text: 探索實驗室的顯微影像；點選圖片可查看完整原圖。
      count: 3
      link_label: 瀏覽全部研究影像

  - block: lab_events
    id: activities
    content:
      count: 3
      title: 活動與實驗室日常
      link_label: 所有活動與照片

  - block: lab_news
    id: news
    content:
      title: 最新消息
      link_label: 所有消息與活動

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
    id: closing
    content:
      title:
      subtitle:
      text: |
        <div class="zl-close">
          <h2>帶著你的診斷問題來找我們。</h2>
          <p>有組織樣本的臨床醫師、有好奇心的學生，都從一封信開始。</p>
          <p class="zl-close-btns"><a class="btn btn-primary" href="collaborations/">臨床合作</a><a class="btn btn-outline-light" href="join/">加入我們</a></p>
        </div>
    design:
      columns: '1'
      background:
        color: '#04201c'
        text_color_light: true
---
