import { writeFile } from 'node:fs/promises';
import hero from '../src/sections/01-promise.js';
import pet from '../src/sections/02-pet.js';
import boop from '../src/sections/03-boop.js';
import hold from '../src/sections/04-hold.js';
import creature from '../src/sections/05-creature.js';
import halo from '../src/sections/06-halo.js';
import object from '../src/sections/07-object.js';
import quiet from '../src/sections/08-quiet.js';
import size from '../src/sections/09-scale.js';
import details from '../src/sections/10-specifications.js';
import inside from '../src/sections/11-inside.js';
import crown from '../src/sections/12-crown.js';
import detents from '../src/sections/13-detents.js';
import antenna from '../src/sections/14-antenna.js';
import assembly from '../src/sections/15-assembly.js';
import rfLab from '../src/sections/rf-lab.js';
const sections=[hero,pet,boop,hold,creature,halo,object,quiet,size,details,inside,crown,detents,antenna,assembly];
const escape=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;');
const brand='<span class="brand-symbol" aria-hidden="true"></span>bingbong';
const html=`<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080b13"><meta name="color-scheme" content="dark"><title>bingbong — You turn it. They feel it.</title><meta name="description" content="A small cellular keychain, made for two. Turn to pet. Press to boop. Hold to be there. No phone, no app, nothing to set up."><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/albert-sans.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/src/experience.css"><link rel="stylesheet" href="/src/assembly.css"></head>
<body class="is-hello"><script>document.body.classList.add('enhanced')</script>
<a class="skip-link" href="#main">Skip to the story</a>
<header class="site-header"><a class="wordmark" href="#hello" aria-label="bingbong home">${brand}</a><nav aria-label="Main navigation"><a href="#pet">The feeling</a><a href="#object">The object</a><a href="#inside">Inside</a><a href="#details">The details</a><a href="#rf-lab" data-rf-open>RF lab</a></nav><a class="nav-try" href="#pet">Try it <span aria-hidden="true">↗</span></a></header>
<aside aria-label="Interactive product"><div class="scene-stage" id="scene-stage" role="group" aria-label="${escape(hero.alt)}"><div class="scene-aura" aria-hidden="true"></div><div class="scene-grid" aria-hidden="true"></div><img class="hero-still" src="/renders/hello.webp" width="1200" height="1100" alt="" loading="lazy"><div class="scene-loading" aria-hidden="true"></div><div class="scene-canvas" id="scene-canvas"></div><div class="scene-note"><span class="tiny-spark" aria-hidden="true">✳</span><span id="scene-note">${hero.annotation}</span></div><div class="pair-label yours"><span></span>YOU</div><div class="pair-label theirs"><span></span>YOUR PERSON</div><div class="travel-line" aria-hidden="true"><i></i></div><div class="part-pin" aria-hidden="true"><i></i><span></span></div><div class="size-rule"><span>95 mm</span></div><button id="crown-target" class="crown-target" aria-label="Crown: drag or use arrow keys to turn; Enter to boop; hold Space for presence" aria-describedby="crown-help"></button></div><p class="sr-only" id="crown-help">Left and right arrows turn by one detent. Enter sends one boop. Hold Space to share presence, then release. Drag the body of the product to inspect it from any angle.</p></aside>
<div class="scene-toolbar interactive" role="region" aria-label="Product view controls"><span><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 8c-3 4 2 7 7 7s10-3 7-7M3 8l0 4M3 8l4 1M10 3v9m-3-6 3-3 3 3"/></svg>Drag to rotate</span><button data-orbit="-1" aria-label="Rotate product left">‹</button><button data-orbit="1" aria-label="Rotate product right">›</button><button class="view-reset" data-reset-view aria-label="Reset product view">↺</button></div>
<nav class="chapter-progress" aria-label="Story chapters">${sections.map((s,i)=>`<a href="#${s.id}" aria-label="${escape(s.label)}" ${i===0?'aria-current="true"':''}></a>`).join('')}</nav>
<main id="main">${sections.map((s,i)=>`<section id="${s.id}" class="story-section ${i===0?'hero':''} ${s.study?'assembly-section':''}" data-index="${i}" data-label="${escape(s.label)}" data-alt="${escape(s.alt)}" data-note="${escape(s.annotation)}" aria-labelledby="title-${s.id}"><div class="section-inner"><div class="section-copy"><p class="eyebrow"><span aria-hidden="true"></span>${s.eyebrow}</p><${i===0?'h1':'h2'} id="title-${s.id}">${s.title}</${i===0?'h1':'h2'}><p class="description">${s.description}</p>${s.extra}</div><img class="section-still" src="/renders/${s.id}.webp" width="1200" height="1100" alt="${escape(s.alt)}" loading="lazy"></div>${i===0?'<div class="hero-bottom"><a href="#pet"><span class="scroll-line" aria-hidden="true">↓</span>A LITTLE SCROLL. A LITTLE CLOSER.</a></div>':''}</section>`).join('')}</main>
<footer><a class="wordmark" href="#hello" aria-label="bingbong home">${brand}</a><p>A little way to say, I’m here.</p><span>Target specifications. Nothing measured yet.</span></footer>
<div class="utility-bar interactive" role="region" aria-label="Experience controls"><button id="sound-toggle" aria-pressed="false" aria-label="Sound off. Turn click sound on."><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4zM17 9l5 6m0-6-5 6"/></svg><span>Sound off</span></button><span id="chapter-name">THE PROMISE</span></div><div id="gesture-announcement" class="sr-only" role="status" aria-live="polite"></div>
${rfLab()}
<script type="module" src="/src/main.js"></script></body></html>`;
await writeFile('index.html',html);
console.log('Live product experience generated; fifteen chapters plus the RF lab and a static RF primer.');
