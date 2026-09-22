# What changed in the redesign

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
