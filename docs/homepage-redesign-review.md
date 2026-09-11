# Homepage redesign review — 2026-09-11

## Delivered

Bilingual homepage with a real lab image, a short mission, news, four research directions, three source-linked selected publications, PI, existing-profile milestones, compact member cards, research and activity previews, recruitment by role, and contact. The complete People page and all thirteen author profiles remain available.

The navbar now resolves homepage anchors through each language's actual home permalink; the PI portrait uses a Hugo page resource. Both fixes work with the GitHub Pages project prefix. Internal custom-block links resolve actual language pages rather than composing paths with relLangURL.

Two CC BY 4.0 figures were downloaded without cropping and attributed with source and licence links. The oral-cancer figure was matched byte-for-byte to the existing supplied original and reused. Gallery now has eight images: six existing originals and two newly sourced figures. The five originals without scientific captions retain appearance-only descriptions.

## Verification

- Hugo 0.135.0 extended production-style build succeeds.
- Playwright / Microsoft Edge: English and Chinese Home at 1440, 1024, 768 and 390 px.
- Additional mobile checks: English/Chinese People, Research, Gallery, News and the English publication list.
- 17 page/viewport checks; 46 unique internal URLs; no broken images, horizontal overflow, duplicate homepage IDs or invalid homepage link fragments.
- Desktop and mobile navigation clicks reach the People section; standalone pages link to the correct language homepage.
- Home shows twelve compact profiles and one PI; full People pages still show thirteen profiles.
- Desktop and mobile screenshots reviewed; scientific figure frames preserve complete panels and scale bars.
- Screenshot/check outputs: C:/Users/ewink/.cache/zhuo-site-review/redesign/.

## Content still requiring source material

Five member portraits, unresolved name/status details, five original image captions, instrument specifications/photos, and confirmation of official Chinese lab name. The probe and AI research cards remain labelled concept illustrations. Recruitment invites enquiries without promising current vacancies or funding. Milestones are drawn from the existing PI profile and remain subject to the same factual review as that profile.
