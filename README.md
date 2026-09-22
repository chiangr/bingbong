# bingbong

The current interactive product site, engineering references, and hardware working files in one checkout. Start with [SESSION_HANDOFF.md](SESSION_HANDOFF.md) for the accepted design direction, source authority, verification results, and remaining work.

This handoff branch is `codex/assembly-handoff-2026-09-22` in [chiangr/bingbong](https://github.com/chiangr/bingbong). It preserves the earlier `master` history and mirrors the local project layout: the former repository-root firmware now lives under `firmware/`.

## Run the site

Install Node.js 24 LTS (or 22.12+) and run:

```sh
git clone --single-branch --branch codex/assembly-handoff-2026-09-22 https://github.com/chiangr/bingbong.git
cd bingbong/site
npm ci
npm run dev
```

Open http://localhost:5173/#inside for the exploded assembly study, or http://localhost:5173/ for the full fifteen-chapter experience. [The standalone HTML](site/artifact/bingbong.html) also opens directly in a browser without installing dependencies.

For a production preview:

```sh
npm run build
npm run preview
```

Open http://localhost:4173/#inside. Servers must be started on each laptop; no remote service is required.

## Project map

| Path | Contents |
| --- | --- |
| [site/](site/) | Current Three.js/Vite experience, all assets, source, scripts and documentation |
| [site/qa/](site/qa/) | Saved tests, 240 layout captures, independent reviews, Lighthouse report and videos |
| [DESIGN_MANUFACTURING_REPORT_2026-09-19.md](DESIGN_MANUFACTURING_REPORT_2026-09-19.md) | Latest engineering authority, including conflicts and open decisions |
| [REDESIGN_DECISION_2026-09-12.md](REDESIGN_DECISION_2026-09-12.md) | Earlier engineering decisions; superseded where the September 19 report conflicts |
| [firmware/](firmware/) | Existing ESP32-S2/BG95 bring-up code and current KiCad working files in `bingbong_pcb/` |
| [cad/](cad/), [cad-v2/](cad-v2/) | Existing mechanical and PCB design exports; these are not final production CAD for the illustrated reference build |
| [pcbway-fab/](pcbway-fab/), [datasheets/](datasheets/), [bom-scratch/](bom-scratch/) | Fabrication exports, component references and supporting analysis |

See [site/README.md](site/README.md) for interactions and verification commands. The website uses the engineering report's reference geometry; existing hardware files and firmware do not constitute a completed implementation of that design.
