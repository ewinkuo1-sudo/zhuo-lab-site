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
        label: Our research
        url: '#research'
      cta_alt:
        label: Join the lab
        url: '#join'
      cta_note:
        label: Institute of Biophotonics · National Yang Ming Chiao Tung University · Taipei
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
          <div><b>21+</b><span>journal papers</span></div>
          <div><b>5</b><span>imaging modalities</span></div>
          <div><b>4</b><span>clinical programmes</span></div>
          <div><b>3</b><span>hospital collaborations</span></div>
        </div>
        <p class="zl-stats-note">SHG · THG · TPEF · CARS/SRS · FLIM</p>
    design:
      columns: '1'
      spacing:
        padding: ['0', '0', '1.5rem', '0']

  - block: markdown
    id: about
    content:
      title: About Us
      text: |
        **See tissue without labels.** We build nonlinear optical microscopes — SHG, TPEF, CARS, FLIM — that image cancer and collagen at the cellular scale, with no stain and no fixation. Then we bring those tools into the clinic: fibre-based endomicroscopy probes, polarization-resolved collagen mapping, and deep learning that turns raw photon signals into diagnostic calls.

        Led by Prof. Guan-Yu Zhuo at the Institute of Biophotonics, NYCU, the lab sits at the intersection of ultrafast optics, tissue biology, and translational medicine.
    design:
      columns: '1'

  - block: markdown
    id: pi
    content:
      title: Principal Investigator
      text: |
        <div class="zl-pi">
          <div class="zl-pi-photo">
            <img src="media/pi/zhuo.jpg" alt="Prof. Guan-Yu Zhuo" loading="lazy">
          </div>
          <div class="zl-pi-text">
            <h3>Guan-Yu Zhuo, Ph.D.</h3>
            <p>Associate Professor, <a href="https://bioph.nycu.edu.tw/">Institute of Biophotonics</a>, National Yang Ming Chiao Tung University.</p>
            <p>Ph.D. in Physics, National Taiwan University (2012). Postdoctoral research at Caltech, Academia Sinica, and Max Planck Institute for Polymer Research. NSTC Excellent Young Scholar (2024–2027). Co-editor, <em>Advanced Biophysical Techniques in Biosciences</em> (Springer, 2025).</p>
            <p><a href="https://scholar.google.com/citations?user=nF1TaA8AAAAJ">Google Scholar</a> · <a href="https://orcid.org/0000-0002-9813-2989">ORCID</a></p>
          </div>
        </div>
    design:
      columns: '1'

  - block: features
    id: research
    content:
      title: Research
      items:
        - name: Label-free nonlinear optical microscopy
          image: gen/thumb-multimodal.webp
          image_alt: Simulated multimodal micrograph with SHG collagen, two-photon autofluorescence and CARS lipid contrast (illustration)
          icon: microscope
          icon_pack: fas
          description: SHG, two-photon fluorescence, CARS and FLIM on one platform, with no stain and no fixation.
        - name: Collagen chirality and ECM quantification
          image: gen/thumb-pshg.webp
          image_alt: Simulated polarization-resolved SHG orientation map of collagen fibres (illustration)
          icon: dna
          icon_pack: fas
          description: Polarization-resolved SHG and SHG circular dichroism to read fibre orientation and pathology in cancer and cartilage.
        - name: Miniaturized nonlinear endomicroscopy
          image: gen/thumb-endoscope.webp
          image_alt: Schematic of a fibre-based nonlinear endomicroscopy probe imaging collagen in tissue (illustration)
          icon: stethoscope
          icon_pack: fas
          description: Fibre-based nonlinear imaging probes designed for in vivo diagnosis.
        - name: AI-assisted label-free pathology
          image: gen/thumb-ai.webp
          image_alt: Simulated label-free tissue image with a tile-wise classifier probability overlay (illustration)
          icon: brain
          icon_pack: fas
          description: Machine learning and deep learning that turn unstained multiphoton images into diagnostic calls, from texture features and SVMs to end-to-end neural networks.

  - block: markdown
    id: research-detail
    content:
      title:
      text: |
        <div class="zl-steps">
          <div><small>01</small><b>Image</b><p>Unstained section on the multiphoton platform: SHG, TPEF, P-SHG channels in one scan.</p></div>
          <div><small>02</small><b>Quantify</b><p>Fibre orientation, χ33/χ31, texture features and whole-slide tiles extracted automatically.</p></div>
          <div><small>03</small><b>Classify</b><p>SVM or deep network returns a call per region, with the source image beside it.</p></div>
          <div><small>04</small><b>Validate</b><p>Checked against the pathologist's ground truth before anything is reported.</p></div>
        </div>
    design:
      columns: '1'
      spacing:
        padding: ['0', '0', '2rem', '0']

  - block: lab_people
    id: people
    content:
      title: People

  - block: lab_gallery
    id: gallery
    content:
      title: Gallery
      text: Explore microscopy images from the lab. Select an image to view the full original.
      count: 6

  - block: lab_events
    id: activities
    content:
      count: 3
      title: Events & lab life

  - block: lab_news
    id: news
    content:
      title: News

  - block: collection
    id: publications
    content:
      title: Publications
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
    id: join
    content:
      title: Join Us
      subtitle: Graduate students, undergraduates and postdocs
      text: |
        We are an interdisciplinary lab. Our work sits between optics, tissue biology and clinical
        medicine, so we welcome students from **physics, electrical and optical engineering,
        biomedical engineering, life sciences and medicine**.

        **What you would work on** — building nonlinear optical microscopes and fibre probes; imaging clinical tissue and biomaterials; quantitative image analysis with ML/DL; AI-assisted pipelines (Python, PyTorch, Claude Code); working directly with clinicians.

        **How to apply** — send one e-mail to <zhuo0929@nycu.edu.tw> with a short CV, which research direction interests you, and your earliest start date. Master's and Ph.D. students apply through the [Institute of Biophotonics](https://bioph.nycu.edu.tw/) admission programmes.
    design:
      columns: '1'

  - block: contact
    id: contact
    content:
      title: Contact
      text: |-
        Institute of Biophotonics, National Yang Ming Chiao Tung University (Yangming campus, Taipei).
      email: zhuo0929@nycu.edu.tw
      phone: +886-2-2826-7962
      address:
        street: 'No. 155, Sec. 2, Linong St., Beitou District'
        city: Taipei
        region: ''
        postcode: '11221'
        country: Taiwan
        country_code: TW
      directions: 'Traditional Medicine Building A, 6th floor, Room 604-E (office). Institute office: Room 608, +886-2-2826-7000 ext. 65707.'
      coordinates:
        latitude: '25.1227'
        longitude: '121.5164'
      autolink: true
    design:
      columns: '1'
---
