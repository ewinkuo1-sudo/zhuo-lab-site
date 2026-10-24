---
title: Clinical Collaborations
date: 2026-09-06
type: landing

sections:
  - block: markdown
    content:
      title: Clinical collaborations
      subtitle: Real tissue, real diagnostic questions
      text: |
        Every imaging method in the lab is developed against a clinical question brought to us by
        physicians and pathologists. Each case runs along the same [research pipeline](../research/):
        see tissue with light, turn it into numbers, hand them to AI, and eventually reach inside the body.
        The badges under each case show which stages it has reached; click one to read about that direction.

        ### Oesophageal cancer: grading the stroma without stains {#esophagus}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#collagen-chirality-and-extracellular-matrix-quantification"><i></i><b>Quantify</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-assisted-label-free-pathology"><i></i><b>Classify</b></a><a class="zl-station zl-station-goal" style="--st:#009E73" href="../research/#miniaturized-nonlinear-endomicroscopy"><i></i><b>Reach</b><small>long-term</small></a></p>

        **Question.** Can the extracellular matrix around a lesion tell squamous cell carcinoma from
        high-grade dysplasia, before a pathologist has to decide on H&E?
        **What we do.** Two-photon and SHG imaging of unstained sections, texture features, and
        machine-learning classifiers.
        **With.** Gastroenterology and pathology, Kaohsiung Medical University Hospital.
        **Status.** Published (*Sci. Rep.* 2025); whole-slide scanning is a follow-on direction whose progress is to be confirmed.

        ### Cartilage disease: osteoarthritis versus rheumatoid arthritis {#cartilage}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#collagen-chirality-and-extracellular-matrix-quantification"><i></i><b>Quantify</b></a></p>

        **Question.** Do collagen fibre organisation and chirality separate normal, osteoarthritic
        and rheumatoid cartilage?
        **What we do.** Polarization-resolved SHG, χ33/χ31 and degree-of-linear-polarization maps.
        **With.** Rheumatology and orthopaedics collaborators at China Medical University Hospital.
        **Status.** Published (*APL Bioeng.* 2024).

        ### Oral cancer: worst pattern of invasion {#oral}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-assisted-label-free-pathology"><i></i><b>Classify</b></a><a class="zl-station zl-station-goal" style="--st:#009E73" href="../research/#miniaturized-nonlinear-endomicroscopy"><i></i><b>Reach</b><small>long-term</small></a></p>

        **Question.** Can a prognostic invasion pattern that is hard to score by eye be quantified
        from label-free multiphoton images?
        **What we do.** Multiphoton imaging of the tumour front combined with deep-learning
        classification.
        **With.** Head-and-neck pathology collaborators.
        **Status.** Published (*Lab. Invest.* 2026).

        ### Collagen pathology scores a pathologist can audit {#collagen-score}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#E69F00" href="../research/#collagen-chirality-and-extracellular-matrix-quantification"><i></i><b>Quantify</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-assisted-label-free-pathology"><i></i><b>Classify</b></a></p>

        **Question.** Can collagen-related pathology be turned into a reproducible number rather than
        a visual grade?
        **What we do.** Quantitative SHG metrics and machine learning, reported alongside the images
        they came from so the reasoning is inspectable.
        **Status.** Published (*J. Microsc.* 2026); ongoing.

        ## Data and ground truth
        Every study uses **adjacent 5 µm sections** from the same block: one is H&E-stained and
        annotated by a pathologist to serve as ground truth, the other is left unstained for
        label-free multiphoton imaging. Classifiers are trained and tested only against that
        annotation, so every claim traces back to a pathologist's call on the same tissue.

        ## How a collaboration works
        1. You bring a diagnostic question and access to tissue (fresh, frozen or FFPE unstained sections).
        2. We image label-free on our multiphoton platform and build the analysis pipeline with you.
        3. Results are validated against your ground truth and written up jointly.

        Clinicians and pathologists interested in a pilot study: [contact us](../contact/).

    design:
      columns: '1'
---
