---
title: Clinical Collaborations
summary: 'Questions brought back from the clinic: esophageal cancer, cartilage disease, oral cancer and prostate cancer, with the stations each case has reached, what was found and what is not yet known.'
date: 2026-09-06
type: landing

sections:
  - block: markdown
    content:
      title: Clinical collaborations
      subtitle: Questions brought back from the clinic
      text: |
        Most of our questions start in the clinic: a physician or pathologist meets tissue that is hard to read, and we try to give an answer that can be measured from optical images. Each case runs along the same [research path](../research/): see, measure, distinguish, and eventually reach inside the body. The badges show which stations a case has reached; click one to read about that direction. Collaborating institutions and clinicians are listed in each paper's author affiliations.

        ### Esophageal cancer: squamous cell carcinoma versus high-grade dysplasia {#esophagus}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#collagen-chirality-and-extracellular-matrix-quantification"><i></i><b>Measure</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-assisted-label-free-pathology"><i></i><b>Distinguish</b></a><a class="zl-station zl-station-goal" style="--st:#009E73" href="../research/#miniaturized-nonlinear-endomicroscopy"><i></i><b>Reach</b><small>long-term</small></a></p>

        **Question.** Squamous cell carcinoma and high-grade dysplasia can look alike on a section. Can the extracellular matrix around a lesion help tell them apart?<br>
        **Approach.** Two-photon microscopy images SHG and two-photon fluorescence from the extracellular matrix; texture features are computed and passed to a support-vector machine.<br>
        **Result.** Classifiers built on the SHG images reach 75%, 84.21%, 95% and 95.65% accuracy across four comparisons (*Sci. Rep.* 2025).<br>
        **Not yet known.** These are samples from a single study; whether the result holds for other patients remains to be validated.

        ### Cartilage disease: osteoarthritis versus rheumatoid arthritis {#cartilage}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#collagen-chirality-and-extracellular-matrix-quantification"><i></i><b>Measure</b></a></p>

        **Question.** How does the arrangement of collagen fibers differ between normal, osteoarthritic and rheumatoid-arthritis cartilage?<br>
        **Approach.** Polarization-resolved SHG, giving point-by-point maps of the susceptibility ratio χ33/χ31, the degree of linear polarization and fiber orientation.<br>
        **Result.** Normal cartilage has χ33/χ31 values distinct from both diseases; osteoarthritic cartilage shows a higher degree of linear polarization and more directional fibers; rheumatoid-arthritis cartilage is more disordered (*APL Bioeng.* 2024).<br>
        **Not yet known.** The paper presents these parameters as a reference for diagnosis; whether they can serve as clinical markers needs more samples.

        ### Oral cancer: worst pattern of invasion {#oral}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#E69F00" href="../research/#collagen-chirality-and-extracellular-matrix-quantification"><i></i><b>Measure</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-assisted-label-free-pathology"><i></i><b>Distinguish</b></a><a class="zl-station zl-station-goal" style="--st:#009E73" href="../research/#miniaturized-nonlinear-endomicroscopy"><i></i><b>Reach</b><small>long-term</small></a></p>

        **Question.** The worst pattern of invasion (WPOI-5) is a pathological sign of poor prognosis in oral cancer. What does the tissue around such tumors look like?<br>
        **Approach.** Clinical data from 263 patients are analyzed, and the tumor microenvironment is examined with multimodal nonlinear microscopy (SHG, third-harmonic generation and two-photon fluorescence) and polarization-resolved SHG.<br>
        **Result.** WPOI-5 is an independent predictor of poorer relapse-free survival. Samples with WPOI-5 show increased collagen cross-linking and remodeling, with fibers tending to align perpendicular to the tumor boundary (*Lab. Invest.* 2026). A separate pilot study applies deep learning and machine learning to two-photon images of oral lesions (*IEEE Photonics J.* 2026).<br>
        **Not yet known.** The paper presents the imaging results as preliminary, proof-of-concept evidence that calls for validation studies.

        ### Prostate cancer: normal versus tumor tissue {#prostate}

        <p class="zl-case-stations"><a class="zl-station" style="--st:#56B4E9" href="../research/#label-free-nonlinear-optical-microscopy"><i></i><b>See</b></a><a class="zl-station" style="--st:#CC79A7" href="../research/#ai-assisted-label-free-pathology"><i></i><b>Distinguish</b></a></p>

        **Question.** Are label-free two-photon fluorescence images enough to tell normal prostate tissue from tumor?<br>
        **Approach.** On 295 images from tissue microarrays (135 sample groups), a texture-feature classifier is compared with deep-learning models based on MobileNetV3.<br>
        **Result.** The texture-feature classifier reaches 71.9% accuracy; the best deep-learning model reaches 86.1%, with an AUC of about 0.91 (*Sci. Rep.* 2026).<br>
        **Not yet known.** The result comes from cross-validation within one dataset; the paper calls for larger independent cohorts and patient-level validation.

        ## What the images are checked against
        Optical images are read against the pathological diagnosis. After imaging, the result is compared with a pathologist's reading of conventionally stained sections, and classifiers are trained and tested against that answer.

        ## How a collaboration works
        1. You bring a diagnostic problem and the tissue available for it.
        2. We image it label-free and decide with you what to measure and how to analyze it.
        3. The results are checked against the pathological diagnosis and written up together.

        Clinicians and pathologists interested in a small pilot study: [contact us](../contact/).

    design:
      columns: '1'
---
