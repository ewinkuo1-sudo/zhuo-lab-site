// 由 build_data.py 產生，勿手改
window.SITE_DATA={
 "zh": {
  "lang": "zh",
  "statement": "用光學看見組織，推進無標記診斷。",
  "description": "結合非線性光學、定量影像與人工智慧，研究癌症和組織結構，開發走向臨床的成像工具。",
  "official": "https://ewinkuo1-sudo.github.io/zhuo-lab-site/",
  "owl": "https://ewinkuo1-sudo.github.io/owl-toys/",
  "stations": [
   {
    "key": "microscopy",
    "verb": "看得到",
    "name": "無標記非線性光學顯微",
    "developing": false,
    "question": "不同的光學對比，如何呈現組織結構與分子特性？",
    "method": "已發表工作以多模態顯微方法結合 SHG、雙光子螢光、螢光生命期成像與 CARS；實際使用的通道與取像順序依實驗而定。",
    "finding": "2021 年論文介紹多模態平台；2025 年食道組織研究以 SHG、雙光子螢光與影像分析比較不同診斷組別的組織。",
    "status": "方法與組織應用已有論文支持；走向臨床使用是長期目標。",
    "papers_label": "代表論文",
    "finding_label": "已發表發現",
    "papers": [
     {
      "title": "Label-free multimodal nonlinear optical microscopy for biomedical applications",
      "authors": "Zhuo 等",
      "journal": "Journal of Applied Physics",
      "year": 2021,
      "doi": "10.1063/5.0036341"
     },
     {
      "title": "Quantitative image analysis of the extracellular matrix of esophageal squamous cell carcinoma and high grade dysplasia via two-photon microscopy",
      "authors": "Makkithaya 等",
      "journal": "Scientific Reports",
      "year": 2025,
      "doi": "10.1038/s41598-025-13910-7"
     }
    ],
    "figure": {
     "src": "assets/esophagus-2025.webp",
     "w": 1200,
     "h": 1766,
     "alt": "論文圖包含 H&E 組織切片，以及食道組織的 SHG、雙光子螢光與合併影像。",
     "caption": "2025 年食道組織研究圖 2：H&E 組織切片，以及 SHG、雙光子螢光與合併影像。這項研究用的是病理切片、含 H&E 染色，所以這張圖不能當成「完全未染色」的示範。",
     "credit": "Makkithaya et al. · Scientific Reports · Fig. 2",
     "source": "https://doi.org/10.1038/s41598-025-13910-7",
     "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    "toys": [
     {
      "title": "FLIM Phasor 遊樂場",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/flim-phasor-playground.html",
      "desc": "螢光壽命怎麼變成一張 phasor 圖。"
     },
     {
      "title": "CARS 拍頻遊樂場",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/cars-beat-playground.html",
      "desc": "兩道雷射拍頻，怎麼讀出分子振動。"
     }
    ]
   },
   {
    "key": "collagen",
    "verb": "讀得懂",
    "name": "膠原蛋白手性與細胞外基質定量",
    "developing": false,
    "question": "如何量化不同組織狀態下的膠原蛋白排列？",
    "method": "偏振解析 SHG 量測訊號隨偏振的變化，取得感受率比值、線偏振程度與纖維方向等參數，描述膠原蛋白的組織特徵。",
    "finding": "2024 年軟骨研究比較正常、骨關節炎與類風濕性關節炎組織，報告各組在偏振衍生參數與膠原排列上的差異。",
    "status": "軟骨研究已發表；把同一套偏振量測用到其他組織與細胞外基質，是實驗室持續發展的方向。",
    "papers_label": "代表論文",
    "finding_label": "已發表發現",
    "papers": [
     {
      "title": "Investigating cartilage-related diseases by polarization-resolved second harmonic generation (P-SHG) imaging",
      "authors": "Makkithaya 等",
      "journal": "APL Bioengineering",
      "year": 2024,
      "doi": "10.1063/5.0196676"
     },
     {
      "title": "Advancing collagen-related pathology assessment through second-harmonic generation imaging",
      "authors": "Rodrigues 等",
      "journal": "Journal of Microscopy",
      "year": 2026,
      "doi": "10.1111/jmi.70098"
     },
     {
      "title": "Polarization resolved second harmonic microscopy",
      "authors": "Mazumder 等",
      "journal": "Methods",
      "year": 2017,
      "doi": "10.1016/j.ymeth.2017.06.012"
     }
    ],
    "figure": {
     "src": "assets/cartilage-2024.webp",
     "w": 757,
     "h": 719,
     "alt": "骨關節炎軟骨的 H&E、SHG 強度、感受率比值、偏振與方向分布圖。",
     "caption": "2024 年研究中的骨關節炎軟骨：組織切片、SHG 強度及偏振衍生參數圖，保留完整圖 3。",
     "credit": "Makkithaya et al. · APL Bioengineering · Fig. 3",
     "source": "https://doi.org/10.1063/5.0196676",
     "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    "toys": [
     {
      "title": "SHG 互動教室",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/shg-academy.html",
      "desc": "倍頻訊號從哪來、為什麼膠原特別亮。"
     },
     {
      "title": "P-SHG 偏振遊樂場",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/pshg-polar-playground.html",
      "desc": "轉偏振、看花瓣圖，讀出纖維方向。"
     }
    ]
   },
   {
    "key": "ai",
    "verb": "判得準",
    "name": "AI 輔助無標記病理",
    "developing": false,
    "question": "哪些影像特徵有助於區分不同組織組別？",
    "method": "2025 年食道研究以灰階共現矩陣（GLCM）抽取紋理特徵，使用支持向量機（SVM）分類。2026 年前導研究則探討深度學習與機器學習用於雙光子口腔病灶影像分類。",
    "finding": "2025 年食道研究用 SHG 影像的紋理特徵訓練 SVM，分辨不同診斷組別；2026 年口腔病灶研究則是深度學習與機器學習結合的前導研究。兩者都在各自的資料集內評估，樣本數有限。",
    "status": "影像分類已有論文支持；要成為臨床可用的工具，還需要更大的資料集與獨立驗證。",
    "papers_label": "代表論文",
    "finding_label": "已發表發現",
    "papers": [
     {
      "title": "Deciphering the Worst Pattern of Invasion in Oral Cancer: Integrative Clinical, Pathological, and Multimodal Nonlinear Optical Imaging Insights",
      "authors": "Huang 等",
      "journal": "Laboratory Investigation",
      "year": 2026,
      "doi": "10.1016/j.labinv.2025.104257"
     },
     {
      "title": "Quantitative image analysis of the extracellular matrix of esophageal squamous cell carcinoma and high grade dysplasia via two-photon microscopy",
      "authors": "Makkithaya 等",
      "journal": "Scientific Reports",
      "year": 2025,
      "doi": "10.1038/s41598-025-13910-7"
     },
     {
      "title": "Integration of Deep Learning and Machine Learning for Label-Free Two-Photon Imaging-Based Classification of Oral Lesions: A Pilot Study",
      "authors": "Karnati 等",
      "journal": "IEEE Photonics Journal",
      "year": 2026,
      "doi": "10.1109/jphot.2026.3701723"
     }
    ],
    "figure": {
     "src": "assets/esophagus-2025-fig8.webp",
     "w": 1200,
     "h": 860,
     "alt": "四張 ROC 曲線圖，各自比較兩個食道組織診斷組別的 SVM 分類結果。",
     "caption": "2025 年食道研究圖 8：以 SHG 影像紋理特徵訓練的 SVM 分類器，在四組兩兩比較下的 ROC 曲線，保留完整圖。",
     "credit": "Makkithaya et al. · Scientific Reports · Fig. 8",
     "source": "https://doi.org/10.1038/s41598-025-13910-7",
     "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    "toys": []
   },
   {
    "key": "endomicroscopy",
    "verb": "到得了",
    "name": "微型化非線性內視顯微術",
    "developing": true,
    "question": "如何把非線性顯微成像帶入更小的探測空間？",
    "method": "把激發光經光纖送到微型探頭、再把訊號收回來，讓非線性顯微離開光學桌。探頭的設計與效能依目標應用而定。",
    "finding": "2021 年的多模態顯微論文是這個方向的技術基礎；微型探頭本身還沒有發表成果。",
    "status": "微型化是長期方向，目前仍在發展中；探頭的尺寸與成像效能還沒有可公開的數據。",
    "papers_label": "相關技術背景",
    "finding_label": "已有技術基礎",
    "papers": [
     {
      "title": "Label-free multimodal nonlinear optical microscopy for biomedical applications",
      "authors": "Zhuo 等",
      "journal": "Journal of Applied Physics",
      "year": 2021,
      "doi": "10.1063/5.0036341"
     }
    ],
    "figure": {
     "src": "assets/probe-concept.webp",
     "w": 683,
     "h": 649,
     "alt": "3D 示意圖：橘色光纖接到一支手持探頭，探頭指向培養皿裡的組織樣品。",
     "caption": "概念示意：光纖把激發光送到手持探頭。這是本頁 3D 場景的渲染圖，不是實驗室的實機照片。",
     "credit": "本頁 3D 場景渲染",
     "source": null,
     "license": null
    },
    "toys": []
   }
  ]
 },
 "en": {
  "lang": "en",
  "statement": "See tissue through light. Advance label-free diagnosis.",
  "description": "We combine nonlinear optics, quantitative imaging and AI to study cancer and tissue structure, and develop imaging tools for clinical translation.",
  "official": "https://ewinkuo1-sudo.github.io/zhuo-lab-site/",
  "owl": "https://ewinkuo1-sudo.github.io/owl-toys/",
  "stations": [
   {
    "key": "microscopy",
    "verb": "See",
    "name": "Label-free nonlinear optical microscopy",
    "developing": false,
    "question": "How can optical contrasts reveal tissue architecture and molecular properties?",
    "method": "Published work combines SHG, two-photon fluorescence, fluorescence-lifetime imaging and CARS within a multimodal microscopy approach. The contrast channels and acquisition sequence depend on the experiment.",
    "finding": "The 2021 paper presents a multimodal platform. A 2025 esophageal tissue study combines SHG and two-photon fluorescence with image analysis to compare tissue groups. That study includes H&E-stained sections; its figure should not be read as a demonstration that all samples were unstained.",
    "status": "Published studies establish the methods and tissue applications. Extending them toward clinical use is a long-term goal; current system configurations and new projects should be discussed with the lab.",
    "papers_label": "Representative papers",
    "finding_label": "Published findings",
    "papers": [
     {
      "title": "Label-free multimodal nonlinear optical microscopy for biomedical applications",
      "authors": "Zhuo et al.",
      "journal": "Journal of Applied Physics",
      "year": 2021,
      "doi": "10.1063/5.0036341"
     },
     {
      "title": "Quantitative image analysis of the extracellular matrix of esophageal squamous cell carcinoma and high grade dysplasia via two-photon microscopy",
      "authors": "Makkithaya et al.",
      "journal": "Scientific Reports",
      "year": 2025,
      "doi": "10.1038/s41598-025-13910-7"
     }
    ],
    "figure": {
     "src": "assets/esophagus-2025.webp",
     "w": 1200,
     "h": 1766,
     "alt": "Published figure with H&E histology and SHG, two-photon fluorescence and merged esophageal tissue images.",
     "caption": "Esophageal tissue in the 2025 study: H&E histology alongside SHG, two-photon fluorescence and merged images. Full Fig. 2 is retained.",
     "credit": "Makkithaya et al. · Scientific Reports · Fig. 2",
     "source": "https://doi.org/10.1038/s41598-025-13910-7",
     "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    "toys": [
     {
      "title": "FLIM phasor playground",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/flim-phasor-playground.html",
      "desc": "How fluorescence lifetimes become a phasor plot."
     },
     {
      "title": "CARS beat playground",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/cars-beat-playground.html",
      "desc": "How two beating lasers read out molecular vibrations."
     }
    ]
   },
   {
    "key": "collagen",
    "verb": "Quantify",
    "name": "Collagen chirality and extracellular-matrix quantification",
    "developing": false,
    "question": "How can collagen organization be quantified across different tissue conditions?",
    "method": "Polarization-resolved SHG measures polarization-dependent signals to derive susceptibility ratios, linear polarization and fibre orientation. These measurements describe aspects of collagen organization.",
    "finding": "The 2024 cartilage study compares normal, osteoarthritic and rheumatoid-arthritis tissues. It reports differences in polarization-derived parameters and collagen organization between these tissue groups.",
    "status": "Cartilage findings are published. Broader applications to collagen chirality and extracellular-matrix assessment remain research directions; the current scope of ongoing studies needs confirmation.",
    "papers_label": "Representative papers",
    "finding_label": "Published findings",
    "papers": [
     {
      "title": "Investigating cartilage-related diseases by polarization-resolved second harmonic generation (P-SHG) imaging",
      "authors": "Makkithaya et al.",
      "journal": "APL Bioengineering",
      "year": 2024,
      "doi": "10.1063/5.0196676"
     },
     {
      "title": "Advancing collagen-related pathology assessment through second-harmonic generation imaging",
      "authors": "Rodrigues et al.",
      "journal": "Journal of Microscopy",
      "year": 2026,
      "doi": "10.1111/jmi.70098"
     },
     {
      "title": "Polarization resolved second harmonic microscopy",
      "authors": "Mazumder et al.",
      "journal": "Methods",
      "year": 2017,
      "doi": "10.1016/j.ymeth.2017.06.012"
     }
    ],
    "figure": {
     "src": "assets/cartilage-2024.webp",
     "w": 757,
     "h": 719,
     "alt": "Osteoarthritis cartilage: H&E images, SHG intensity, susceptibility ratio, polarization and orientation maps.",
     "caption": "Osteoarthritis cartilage from the 2024 study: histology, SHG intensity and polarization-derived maps. Full Fig. 3 is retained.",
     "credit": "Makkithaya et al. · APL Bioengineering · Fig. 3",
     "source": "https://doi.org/10.1063/5.0196676",
     "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    "toys": [
     {
      "title": "SHG academy",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/shg-academy.html",
      "desc": "Where the frequency-doubled signal comes from, and why collagen is bright."
     },
     {
      "title": "P-SHG polarization playground",
      "url": "https://ewinkuo1-sudo.github.io/owl-toys/pshg-polar-playground.html",
      "desc": "Rotate the polarization and read fibre orientation from the polar plot."
     }
    ]
   },
   {
    "key": "ai",
    "verb": "Classify",
    "name": "AI-assisted label-free pathology",
    "developing": false,
    "question": "Which image features can help distinguish tissue groups?",
    "method": "The 2025 esophageal study extracts gray-level co-occurrence matrix (GLCM) texture features and uses support-vector machines (SVM) for classification. A 2026 pilot study investigates deep learning and machine learning for two-photon imaging-based oral-lesion classification.",
    "finding": "Published studies evaluate tissue classification in their respective datasets. The oral-lesion work is a pilot study; these results do not establish a general clinical diagnostic system.",
    "status": "Image classification has published support. New whole-slide workflows, pathology scores and deployment plans require separate confirmation and validation.",
    "papers_label": "Representative papers",
    "finding_label": "Published findings",
    "papers": [
     {
      "title": "Deciphering the Worst Pattern of Invasion in Oral Cancer: Integrative Clinical, Pathological, and Multimodal Nonlinear Optical Imaging Insights",
      "authors": "Huang et al.",
      "journal": "Laboratory Investigation",
      "year": 2026,
      "doi": "10.1016/j.labinv.2025.104257"
     },
     {
      "title": "Quantitative image analysis of the extracellular matrix of esophageal squamous cell carcinoma and high grade dysplasia via two-photon microscopy",
      "authors": "Makkithaya et al.",
      "journal": "Scientific Reports",
      "year": 2025,
      "doi": "10.1038/s41598-025-13910-7"
     },
     {
      "title": "Integration of Deep Learning and Machine Learning for Label-Free Two-Photon Imaging-Based Classification of Oral Lesions: A Pilot Study",
      "authors": "Karnati et al.",
      "journal": "IEEE Photonics Journal",
      "year": 2026,
      "doi": "10.1109/jphot.2026.3701723"
     }
    ],
    "figure": {
     "src": "assets/esophagus-2025-fig8.webp",
     "w": 1200,
     "h": 860,
     "alt": "Four ROC curves, each comparing SVM classification of two diagnostic groups of esophageal tissue.",
     "caption": "Fig. 8 of the 2025 esophageal study: ROC curves of an SVM classifier trained on SHG image texture features, for four pairwise comparisons. Full figure retained.",
     "credit": "Makkithaya et al. · Scientific Reports · Fig. 8",
     "source": "https://doi.org/10.1038/s41598-025-13910-7",
     "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    "toys": []
   },
   {
    "key": "endomicroscopy",
    "verb": "Reach",
    "name": "Miniaturized nonlinear endomicroscopy",
    "developing": true,
    "question": "How could nonlinear microscopy be brought into a smaller probing space?",
    "method": "The concept is to combine optical fibres and miniature optics for excitation delivery and signal collection. Probe design and performance depend on the intended application.",
    "finding": "The related 2021 paper describes multimodal microscopy as a technical foundation. It is not evidence of a completed endoscopic probe or clinical deployment.",
    "status": "Miniaturization is a long-term direction. Prototype status, dimensions, imaging performance and representative experimental images await confirmation from the lab.",
    "papers_label": "Related technical background",
    "finding_label": "Technical foundation",
    "papers": [
     {
      "title": "Label-free multimodal nonlinear optical microscopy for biomedical applications",
      "authors": "Zhuo et al.",
      "journal": "Journal of Applied Physics",
      "year": 2021,
      "doi": "10.1063/5.0036341"
     }
    ],
    "figure": {
     "src": "assets/probe-concept.webp",
     "w": 683,
     "h": 649,
     "alt": "3D illustration: an orange optical fibre leads to a handheld probe pointed at tissue in a Petri dish.",
     "caption": "Concept illustration: an optical fibre delivers excitation light to a handheld probe. Rendered from this page's 3D scene; not a photograph of a lab instrument.",
     "credit": "Rendered from this page's 3D scene",
     "source": null,
     "license": null
    },
    "toys": []
   }
  ]
 }
};
