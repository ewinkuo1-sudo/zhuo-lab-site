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


        [Explore microscopy images from the lab](../gallery/)

        ## Label-free nonlinear optical microscopy

        <div class="zl-split">
        <div>

        Second-harmonic generation (SHG), two-photon excited fluorescence (TPEF), coherent anti-Stokes
        Raman scattering (CARS) and fluorescence-lifetime imaging (FLIM) are combined on a single
        multimodal platform. Each contrast reports a different molecular property, so one scan of an
        unstained section yields collagen architecture, cellular autofluorescence, lipid distribution
        and metabolic state at once. Recent work couples these images with machine learning and deep
        learning to classify tissue automatically.

        </div>
        <div>

        ![Simulated multimodal micrograph: SHG collagen in green, two-photon autofluorescence of cells in amber, CARS lipid droplets in orange](gen/thumb-multimodal.webp "Illustration (simulated, not data): SHG collagen, two-photon autofluorescence and CARS lipid contrast from one scan of an unstained section.")

        </div>
        </div>

        ## Collagen chirality and extracellular-matrix quantification

        <div class="zl-split">
        <div>

        Collagen is the dominant SHG source in tissue. Polarization-resolved SHG (P-SHG) and SHG
        circular dichroism (SHG-CD) measure fibre orientation, the χ33/χ31 susceptibility ratio and
        the chiral response of collagen, which change with disease. We have applied this to
        distinguish normal, osteoarthritic and rheumatoid cartilage, and to quantify the stroma of
        oesophageal squamous cell carcinoma and high-grade dysplasia in collaboration with
        gastroenterologists and pathologists.

        </div>
        <div>

        ![Simulated polarization-resolved SHG map in which each collagen fibre is coloured by its local orientation](gen/thumb-pshg.webp "Illustration (simulated, not data): a P-SHG orientation map, hue encoding local fibre angle and brightness encoding SHG intensity, with the two-lobed polarisation response in the inset.")

        </div>
        </div>

        ## AI-assisted label-free pathology

        <div class="zl-split">
        <div>

        A label-free image is only useful in the clinic if it can be read reliably and quickly.
        We therefore treat the analysis pipeline as part of the instrument. Published work extracts
        texture (GLCM) features from SHG and two-photon images and classifies oesophageal carcinoma
        against high-grade dysplasia with support-vector machines, and integrates deep learning
        with classical machine learning to classify label-free two-photon images end to end.
        Current efforts extend this to whole-slide multiphoton scans, to the worst pattern of
        invasion in oral cancer, and to quantitative collagen pathology scores that a pathologist
        can audit.

        </div>
        <div>

        ![Simulated label-free tissue image with a tile-wise classifier probability overlay](gen/thumb-ai.webp "Illustration (simulated, not data): tile-wise classifier output overlaid on a label-free multiphoton image, warm tiles flagging the tumour-like region.")

        </div>
        </div>

        <div class="zl-steps">
          <div><small>01</small><b>Image</b><p>Unstained section on the multiphoton platform: SHG, TPEF, P-SHG channels in one scan.</p></div>
          <div><small>02</small><b>Quantify</b><p>Fibre orientation, χ33/χ31, texture features and whole-slide tiles extracted automatically.</p></div>
          <div><small>03</small><b>Classify</b><p>SVM or deep network returns a call per region, with the source image beside it.</p></div>
          <div><small>04</small><b>Validate</b><p>Checked against the pathologist's ground truth before anything is reported.</p></div>
        </div>

        Beyond the models themselves, the lab uses AI tooling throughout its day-to-day work.
        We use Claude to accelerate image-analysis pipeline development (image registration,
        fibre-orientation quantification, lifetime fitting), for literature synthesis, and for
        manuscript preparation, and we build automated pipelines that take a raw image stack to a
        figure without manual steps. For a small lab this is how a translational programme keeps moving.

        <!-- TODO(老師確認): AI 段落是依 Sci Rep 2025、IEEE Photonics J 2026、Lab Invest 2026、J Microsc 2026 的題目寫的草稿，請老師修正細節與正在進行的項目。 -->

        ## Miniaturized nonlinear endomicroscopy

        <div class="zl-split">
        <div>

        To bring label-free imaging to patients, we are shrinking the nonlinear microscope into
        fibre-based probes suitable for endoscopy, targeting non-invasive diagnosis and short-pulse
        laser treatment of collagen-rich tissue.

        </div>
        <div>

        ![Schematic of a fibre-based nonlinear endomicroscopy probe focusing femtosecond pulses into tissue and collecting SHG from collagen](gen/thumb-endoscope.webp "Illustration: a fibre-based nonlinear endomicroscopy probe delivering femtosecond pulses through a miniature objective and collecting the SHG signal from collagen in tissue. Schematic, not to scale.")

        </div>
        </div>

        ## Molecular structure of starch and biomaterials

        The same SHG physics that reports on collagen also reports on the crystalline order of
        starch granules. We use it, with spectroscopy, to characterise rice and corn starch,
        starch-based bioplastics and engineered biomaterials.

        ## Other lines of work
        - **Chiral imaging of collagen** by SHG circular dichroism, the method behind much of the lab's tissue work.
        - **Single-particle tracking and coherent brightfield microscopy** for label-free, ultrahigh-speed observation of nanoparticles, viruses and intracellular transport in live cells.
        - **Tumour-microenvironment heterogeneity**, mapping how stromal collagen varies across a lesion rather than reporting one average number.

        ## External resources we build on
        - [PSHG-TISS](https://doi.org/10.1038/s41597-022-01477-1): a public collection of polarization-resolved SHG images of tissue (Hristu et al., *Sci. Data* 2022). Not produced by this lab.
        - [Open-source one- and two-photon light-sheet microscope](https://doi.org/10.1038/s41598-025-03107-3) (Hubert et al., *Sci. Rep.* 2025). Not produced by this lab.

        <!-- TODO(老師確認): 每個方向補一張自己的代表影像 (P-SHG 膠原蛋白 / SHG-CD / CARS-FLIM)，放 assets/media/ -->
    design:
      columns: '1'
---
