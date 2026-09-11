---
title:
date: 2026-09-06
type: landing

sections:
  - block: hero
    content:
      title: |
        Seeing tissue
        without labels
      text: |
        We build **label-free nonlinear optical microscopes** that read collagen and tissue structure
        with no stain, and turn those images into diagnoses clinicians can act on.
      cta:
        label: Our research
        url: research/
      cta_alt:
        label: Join the lab
        url: join/
      cta_note:
        label: Institute of Biophotonics · National Yang Ming Chiao Tung University · Taipei
    design:
      background:
        color: '#04201c'
        text_color_light: true

  - block: markdown
    content:
      title:
      text: |
        <div class="zl-stats">
          <div><b>1,490</b><span>citations</span></div>
          <div><b>18</b><span>h-index</span></div>
          <div><b>4</b><span>clinical programmes</span></div>
          <div><b>3</b><span>hospital collaborations</span></div>
        </div>
        <p class="zl-stats-note">Google Scholar, September 2026.</p>
    design:
      columns: '1'
      spacing:
        padding: ['0', '0', '1.5rem', '0']

  - block: markdown
    id: about
    content:
      title: About the lab
      text: |
        **Translational Biophotonics Laboratory (TBL)** at the Institute of Biophotonics, National Yang Ming Chiao Tung University bridges optical innovation and clinical translation, advancing multimodal nonlinear optics for cancer biology and diagnosis.
    design:
      columns: '1'

  - block: features
    content:
      title: Research directions
      items:
        - name: Label-free nonlinear optical microscopy
          image: gen/thumb-multimodal.webp
          image_alt: Simulated multimodal micrograph with SHG collagen, two-photon autofluorescence and CARS lipid contrast (illustration)
          url: research/#label-free-nonlinear-optical-microscopy
          icon: microscope
          icon_pack: fas
          description: SHG, two-photon fluorescence, CARS and FLIM on one platform, with no stain and no fixation.
        - name: Collagen chirality and ECM quantification
          image: gen/thumb-pshg.webp
          image_alt: Simulated polarization-resolved SHG orientation map of collagen fibres (illustration)
          url: research/#collagen-chirality-and-extracellular-matrix-quantification
          icon: dna
          icon_pack: fas
          description: Polarization-resolved SHG and SHG circular dichroism to read fibre orientation and pathology in cancer and cartilage.
        - name: Miniaturized nonlinear endomicroscopy
          image: gen/thumb-endoscope.webp
          image_alt: Schematic of a fibre-based nonlinear endomicroscopy probe imaging collagen in tissue (illustration)
          url: research/#miniaturized-nonlinear-endomicroscopy
          icon: stethoscope
          icon_pack: fas
          description: Fibre-based nonlinear imaging probes designed for in vivo diagnosis.
        - name: AI-assisted label-free pathology
          image: gen/thumb-ai.webp
          image_alt: Simulated label-free tissue image with a tile-wise classifier probability overlay (illustration)
          url: research/#ai-assisted-label-free-pathology
          icon: brain
          icon_pack: fas
          description: Machine learning and deep learning that turn unstained multiphoton images into diagnostic calls, from texture features and SVMs to end-to-end neural networks.

  - block: lab_gallery
    id: gallery
    content:
      title: Gallery
      text: Explore microscopy images from the lab. Select an image to view the full original.
      count: 3
      link_label: Explore the gallery

  - block: lab_news
    id: news
    content:
      title: News
      link_label: All news

  - block: collection
    content:
      title: Recent publications
      text: |
        Complete list on [Google Scholar](https://scholar.google.com/citations?user=nF1TaA8AAAAJ).
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
        <div class="zl-close">
          <h2>Bring us a diagnostic question.</h2>
          <p>Clinicians with tissue, students with curiosity: both start with one e-mail.</p>
          <p class="zl-close-btns"><a class="btn btn-primary" href="collaborations/">Clinical collaborations</a><a class="btn btn-outline-light" href="join/">Join the lab</a></p>
        </div>
    design:
      columns: '1'
      background:
        color: '#04201c'
        text_color_light: true
---
