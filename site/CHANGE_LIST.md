# What changed in the assembly revision

- Added five scroll-linked studies after the original story, using the same live object.
- Modeled the internal stack and ten crown component groups, including a hollow crown/hub, 24-groove race, two ceramic balls, deforming BeCu leaves, washer, retainer, sealed sensing stack and satellite board.
- Added the hollow antenna cap, optical web aperture, integral tab, plated land and compliant SMT contact, plus an animated electrical trace.
- Added twenty component descriptions covering material, manufacture and fitting against the latest engineering report.
- Added a reversible six-stage build with a scrubber, playback, pause, smooth reset and a mobile controller that stays below the object.
- Preserved the pet, boop, hold and scroll demonstrations; kept the assembly code out of the initial view and warmed its shaders before display.
- Reduced cold-start blocking with optional worker graphics initialization and fewer redundant exterior vertices; enlarged mobile chapter targets and increased component-index contrast.
- Added static illustrations/component notes, assembly-specific tests, a source register and an independent accuracy/visual review. Earlier delivery archives are preserved in `revisions/scroll-edition/`.

## Earlier visual redesign

| Area | New version |
| --- | --- |
| Visual direction | Midnight blue, cool silver, violet; a fixed dark presentation in either system theme |
| Typography | Cleaner Albert Sans display/body type; restrained mono labels |
| Opening | Centered headline and a large live object, with a compact demo invitation |
| Product display | Immediate live 3D; no chapter still-image swaps in the normal experience |
| Materials | Rebuilt surface normals, smoother cap edges, matte graphite and controlled studio reflections |
| Movement | One continuous scroll track; curved movement between compositions, reversible progress, restrained ambient motion and animated rear view |
| Inspection | Drag the body, use keyboard view controls, or reset the composition |
| Mobile | Native vertical scrolling; the object, stage clipping, background and controls travel together from the hero into the story |
| Demonstrations | Pet, boop, hold, halo acknowledgment and creature previews preserved |
| State reliability | Leaving a chapter clears pending demonstrations; inspection and halo overrides blend back into the path without a pose reset |
| Accessibility | Reduced motion stops ambient movement and catch-up; scroll still interpolates continuously; keyboard demos retained |
| Cold loading | Baked lighting samples and asynchronous shader compilation remove expensive setup from the visitor's main thread |
| Resilience | Offline reload, standalone file, no-JavaScript content, unavailable-WebGL fallback and context recovery |
| Product facts | Dimensions, semantics and estimate qualifications retained; no new commercial claims |

The first version's source and static archives are in `revisions/first-build/`. Current metrics and evidence are in `DESIGN_NOTES.md`; the first build's scores should not be reused for this revision.
