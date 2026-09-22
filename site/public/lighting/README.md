# Studio environment

A prefiltered CubeUV lighting map from the softbox scene in src/components/studio.js. Not a product image: the model is rendered live using these reflection samples.

384 × 512; linear RGB; radiance divided by 4 for PNG storage; flipY false. The renderer restores the scale through material environment intensity. Rebuild with npm run dev followed by node scripts/bake-lighting.mjs.
