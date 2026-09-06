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
        <br>

        We develop **label-free nonlinear optical microscopy** and bring it to the clinic.
        Our group at the Institute of Biophotonics, National Yang Ming Chiao Tung University (Taipei),
        images collagen, cartilage and tumour stroma with second-harmonic generation, two-photon
        fluorescence and Raman contrast, pairs those images with machine learning for automated
        diagnosis, and is miniaturising the whole pipeline into endoscopes for early disease detection.
      cta:
        label: Our research
        url: research/
      cta_alt:
        label: Join the lab
        url: join/
    design:
      background:
        gradient_end: '#1e3a5f'
        gradient_start: '#0b1f33'
        text_color_light: true

  - block: features
    content:
      title: Research directions
      items:
        - name: Label-free nonlinear optical microscopy
          icon: microscope
          icon_pack: fas
          description: SHG, two-photon fluorescence, CARS and FLIM on one platform, with no stain and no fixation.
        - name: Collagen chirality and ECM quantification
          icon: dna
          icon_pack: fas
          description: Polarization-resolved SHG and SHG circular dichroism to read fibre orientation and pathology in cancer and cartilage.
        - name: Miniaturized nonlinear endomicroscopy
          icon: stethoscope
          icon_pack: fas
          description: Fibre-based nonlinear imaging probes designed for in vivo diagnosis.
        - name: AI-assisted label-free pathology
          icon: brain
          icon_pack: fas
          description: Machine learning and deep learning that turn unstained multiphoton images into diagnostic calls, from texture features and SVMs to end-to-end neural networks.

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
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
