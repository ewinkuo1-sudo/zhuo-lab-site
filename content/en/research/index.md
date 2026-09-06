---
title: Research
date: 2026-09-06
type: landing

sections:
  - block: markdown
    content:
      title: Research
      subtitle: Translational biophotonics
      text: |
        The lab's goal is to move optical imaging techniques from the bench into the hospital.
        We build nonlinear optical microscopes and endoscopes that read the molecular structure of
        tissue directly, without staining, and we turn those images into quantitative markers that
        pathologists and clinicians can use.

        ## Label-free nonlinear optical microscopy

        Second-harmonic generation (SHG), two-photon excited fluorescence (TPEF), coherent anti-Stokes
        Raman scattering (CARS) and fluorescence-lifetime imaging (FLIM) are combined on a single
        multimodal platform. Each contrast reports a different molecular property, so one scan of an
        unstained section yields collagen architecture, cellular autofluorescence, lipid distribution
        and metabolic state at once. Recent work couples these images with machine learning and deep
        learning to classify tissue automatically.

        ## Collagen chirality and extracellular-matrix quantification

        Collagen is the dominant SHG source in tissue. Polarization-resolved SHG (P-SHG) and SHG
        circular dichroism (SHG-CD) measure fibre orientation, the χ33/χ31 susceptibility ratio and
        the chiral response of collagen, which change with disease. We have applied this to
        distinguish normal, osteoarthritic and rheumatoid cartilage, and to quantify the stroma of
        oesophageal squamous cell carcinoma and high-grade dysplasia in collaboration with
        gastroenterologists and pathologists.

        ## AI-assisted label-free pathology

        A label-free image is only useful in the clinic if it can be read reliably and quickly.
        We therefore treat the analysis pipeline as part of the instrument. Published work extracts
        texture (GLCM) features from SHG and two-photon images and classifies oesophageal carcinoma
        against high-grade dysplasia with support-vector machines, and integrates deep learning
        with classical machine learning to classify label-free two-photon images end to end.
        Current efforts extend this to whole-slide multiphoton scans, to the worst pattern of
        invasion in oral cancer, and to quantitative collagen pathology scores that a pathologist
        can audit.

        Beyond the models themselves, the lab uses AI tooling throughout its day-to-day work:
        coding agents to write and refactor image-analysis and instrument-control code, large
        language models for literature triage and first drafts of analysis reports, and
        automated pipelines that take a raw image stack to a figure without manual steps.
        We see these tools as the way a small lab keeps a translational programme moving.

        <!-- TODO(老師確認): AI 段落是依 Sci Rep 2025、IEEE Photonics J 2026、Lab Invest 2026、J Microsc 2026 的題目寫的草稿，請老師修正細節與正在進行的項目。 -->

        ## Miniaturized nonlinear endomicroscopy

        To bring label-free imaging to patients, we are shrinking the nonlinear microscope into
        fibre-based probes suitable for endoscopy, targeting non-invasive diagnosis and short-pulse
        laser treatment of collagen-rich tissue.

        ## Molecular structure of starch and biomaterials

        The same SHG physics that reports on collagen also reports on the crystalline order of
        starch granules. We use it, with spectroscopy, to characterise rice and corn starch,
        starch-based bioplastics and engineered biomaterials.

        <!-- TODO(老師確認): 每個方向補一張自己的代表影像 (P-SHG 膠原蛋白 / SHG-CD / CARS-FLIM)，放 assets/media/ -->
    design:
      columns: '1'
---
