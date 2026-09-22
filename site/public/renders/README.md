# Fallback render source

These static views support unavailable WebGL and no-JavaScript browsing. The normal experience starts its animated 3D model automatically and does not use product-image swaps.

All frames come from `src/components/product-model.js`, `scene.js` and `timeline.js`. The geometry is in millimetres. `npm run assets`, with the dev server running, opens `render-lab.html`, sets complete poses and exports transparent WebP files. Desktop and phone views share geometry and materials. Projected crown coordinates in `src/render-frames.json` are retained as render metadata; live hit areas are projected each frame from the real crown.

`await createScene(container)` creates the renderer. `scene.setFrame({rx,ry,rz,cx,cy,scale,screen,halo,state,pair,otherCx,otherCy,otherScale,otherState,otherHalo,crown,pressed,reduced})` sets a complete target. `cx` and `cy` are fractions of the canvas. `crown` is radians in π/12 steps; `pressed` moves it 0.4 mm. `reduced:true` removes automatic movement for capture. The runtime uses one animation loop and pauses when the document is hidden.

The 95 × 27 × 15 mm body, Ø13 crown, 48 serrations, 1.5 mm ring, 22.5 mm cap, 34 × 16 mm lens and 25.58 × 10.96 mm active panel follow brief §12. The model is an exterior visualization, not production CAD. Final colours and finishes remain design intent. Studio reflections come from the generated lighting map in `public/lighting/`; grain textures are deterministic.
