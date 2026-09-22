import * as THREE from 'three';
import { drawMascot } from './mascot.js';

/** All dimensions are millimetres in the brief's X frame. Exterior model, no invented internals.
 * Reuse: createProduct(); add .group to a Three scene; update({screen, halo, state, crown,
 * pressed, time, reduced}). Crown is radians quantised by caller to 15 degrees.
 */
export const dimensions = Object.freeze({ length:95, width:27, thickness:15, crownDiameter:13, crownLength:8, crownProtrusion:6, serrations:48, detents:24, shoulderDiameter:13.8, lensLength:34, lensWidth:16, activeLength:25.58, activeWidth:10.96, ringStart:71, ringLength:1.5, capStart:72.5, capLength:22.5, pressTravel:.4 });

// 27 x 15 stadium: two 7.5 mm semicircles separated by a 12 mm straight.
function section(theta, inset = 0) {
  const radius = 7.5 - inset;
  return [(Math.cos(theta) >= 0 ? 6 : -6) + radius * Math.cos(theta), radius * Math.sin(theta)];
}
function shellGeometry(start, end, roundedStart = false, roundedEnd = false) {
  const positions=[],normals=[],uv=[],indices=[],profile=[];
  // Sample the straight faces as well as the semicircular sides. Analytical
  // normals keep the machined end flat instead of averaging it into a pillow.
  for(let i=0;i<=48;i++){const a=-Math.PI/2+i/48*Math.PI;profile.push([6,Math.cos(a),Math.sin(a)]);}
  for(let i=1;i<=12;i++)profile.push([6-i,0,1]);
  for(let i=1;i<=48;i++){const a=Math.PI/2+i/48*Math.PI;profile.push([-6,Math.cos(a),Math.sin(a)]);}
  for(let i=1;i<=12;i++)profile.push([-6+i,0,-1]);
  const n=profile.length-1,r=roundedStart||roundedEnd?2.4:0;
  const xs=[];
  if(roundedStart)for(let i=0;i<=16;i++)xs.push(start+r*(1-Math.cos(i/16*Math.PI/2)));
  else xs.push(start);
  // Straight axial faces need only their endpoints. Extra rings here multiply
  // vertices without changing the silhouette, surface normals or texture UVs.
  // Rounded ends and the exact display-opening datums retain their samples.
  if(roundedEnd)for(let i=0;i<=16;i++)xs.push(end-r+r*Math.sin(i/16*Math.PI/2));
  else xs.push(end);
  if(start===6)xs.push(18,52);
  xs.sort((a,b)=>a-b);const rows=xs.length-1;
  for (let j=0; j<=rows; j++) {
    const x = xs[j];
    const distance = Math.min(roundedStart ? x-start : 999, roundedEnd ? end-x : 999);
    const inset = distance < r ? r-Math.sqrt(Math.max(0,r*r-(r-distance)**2)) : 0;
    const side=(roundedStart&&x-start<r)?-1:1;
    const nx=distance<r?side*(r-distance)/r:0,radial=Math.sqrt(Math.max(0,1-nx*nx));
    for(let i=0;i<=n;i++){const[center,ny,nz]=profile[i];positions.push(x-47.5,center+(7.5-inset)*ny,(7.5-inset)*nz);normals.push(nx,ny*radial,nz*radial);uv.push((x-start)/(end-start),i/n);}
  }
  for(let j=0;j<rows;j++) for(let i=0;i<n;i++) {
    const a=j*(n+1)+i,b=a+n+1;
    const x=(xs[j]+xs[j+1])/2;
    const [c,ny,nz]=profile[i];const y=c+7.5*ny,z=7.5*nz;
    if(start===6&&x>18&&x<52&&Math.abs(y)<8&&z>6.8)continue;
    indices.push(a,a+1,b,b,a+1,b+1);
  }
  // End fans close the sealed shell; the join at the ring is covered by the next part.
  for (const j of [0,rows]) {
    const center=positions.length/3; positions.push((j===0?start:end)-47.5,0,0);normals.push(j===0?-1:1,0,0);uv.push(.5,.5);
    const capStart=positions.length/3;
    for(let i=0;i<=n;i++){const k=(j*(n+1)+i)*3;positions.push(...positions.slice(k,k+3));normals.push(j===0?-1:1,0,0);uv.push(i/n,0);}
    for(let i=0;i<n;i++)j===0?indices.push(center,capStart+i+1,capStart+i):indices.push(center,capStart+i,capStart+i+1);
  }
  const geometry=new THREE.BufferGeometry();
  geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geometry.setAttribute('normal',new THREE.Float32BufferAttribute(normals,3));geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geometry.setIndex(indices);
  return geometry;
}

function grainTexture(metal = false) {
  const c=document.createElement('canvas');c.width=c.height=128;const ctx=c.getContext('2d');const d=ctx.createImageData(128,128);let seed=4201;
  for(let y=0;y<128;y++) for(let x=0;x<128;x++) {seed=(seed*16807)%2147483647;const v=metal?145+Math.sin(x*1.7)*8+(seed%9):140+seed%45;const k=(y*128+x)*4;d.data[k]=d.data[k+1]=d.data[k+2]=v;d.data[k+3]=255;}
  ctx.putImageData(d,0,0);const tex=new THREE.CanvasTexture(c);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.repeat.set(metal?9:5,metal?1:3);return tex;
}

export function createProduct() {
  const group=new THREE.Group();group.name='bingbong-95x27x15';
  const polymer=new THREE.MeshPhysicalMaterial({color:0x161e2b,metalness:0,roughness:.61,clearcoat:0,specularIntensity:.32,envMapIntensity:.45,bumpMap:grainTexture(),bumpScale:.004});
  const metal=new THREE.MeshPhysicalMaterial({color:0xbcc7d7,metalness:1,roughness:.43,envMapIntensity:.5,anisotropy:.3,bumpMap:grainTexture(true),bumpScale:.002});
  const collarMat=new THREE.MeshStandardMaterial({color:0x252c37,metalness:.65,roughness:.28});
  const ringMat=new THREE.MeshPhysicalMaterial({color:0xbfc8dc,roughness:.27,metalness:.1,transparent:true,opacity:.88});
  const litRingMat=new THREE.MeshBasicMaterial({color:0xff9e76,toneMapped:false,transparent:true,opacity:0,depthWrite:false});
  const add=(geometry,material,name)=>{const mesh=new THREE.Mesh(geometry,material);mesh.name=name;group.add(mesh);return mesh;};
  add(shellGeometry(6,71,true,false),polymer,'PC-ABS-shell');
  const ring=add(shellGeometry(71,72.5),ringMat,'1.5-mm-optical-PC-halo');
  const emission=add(ring.geometry,litRingMat,'halo-emission');emission.scale.setScalar(1.0002);
  const glowMat=new THREE.MeshBasicMaterial({color:0xff9e76,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending,toneMapped:false});
  const glow=add(shellGeometry(70.85,72.65),glowMat,'halo-local-bloom');glow.scale.y=1.05;glow.scale.z=1.05;
  add(shellGeometry(72.5,95,false,true),metal,'6061-T6-antenna-cap');
  add(shellGeometry(72.5,72.68),new THREE.MeshStandardMaterial({color:0xe1e9f4,metalness:1,roughness:.18}),'cap-edge-chamfer');
  // Lens border and plane are sub-flush relative to the 7.5 mm front datum.
  const lensShape=new THREE.Shape();lensShape.moveTo(-15.5,-8);lensShape.lineTo(15.5,-8);lensShape.quadraticCurveTo(17,-8,17,-6.5);lensShape.lineTo(17,6.5);lensShape.quadraticCurveTo(17,8,15.5,8);lensShape.lineTo(-15.5,8);lensShape.quadraticCurveTo(-17,8,-17,6.5);lensShape.lineTo(-17,-6.5);lensShape.quadraticCurveTo(-17,-8,-15.5,-8);
  const lens=add(new THREE.ShapeGeometry(lensShape),new THREE.MeshBasicMaterial({color:0x010205}),'16x34-glass-lens');
  lens.position.set(35-47.5,0,7.43);
  const art=document.createElement('canvas');art.width=294;art.height=126;const ctx=art.getContext('2d');drawMascot(ctx);
  const texture=new THREE.CanvasTexture(art);texture.colorSpace=THREE.SRGBColorSpace;texture.minFilter=THREE.LinearFilter;
  const screenMaterial=new THREE.MeshBasicMaterial({map:texture,toneMapped:false});
  const clearWindow=add(new THREE.PlaneGeometry(26.2,11.6),new THREE.MeshBasicMaterial({color:0x000000}),'11.6x26.2-clear-window');clearWindow.position.set(34.8-47.5,0,7.432);
  const screen=add(new THREE.PlaneGeometry(25.58,10.96),screenMaterial,'10.96x25.58-AMOLED');screen.position.set(34.8-47.5,0,7.435);
  // A fine, dim optical streak over the ink border, never whitening the AMOLED black.
  const streak=add(new THREE.PlaneGeometry(28,.09),new THREE.MeshBasicMaterial({color:0xc6d9f2,transparent:true,opacity:.16}),'lens-specular');streak.position.set(35-47.5,7.45,7.44);
  const crown=new THREE.Group();crown.name='48-serration-crown';group.add(crown);
  const crownGeometry=new THREE.CylinderGeometry(6.5,6.5,8,192,1,false);const pos=crownGeometry.attributes.position;
  for(let i=0;i<pos.count;i++) {const x=pos.getX(i),z=pos.getZ(i),angle=Math.atan2(z,x),radius=Math.hypot(x,z);if(radius>6){const factor=(6.5-.19*(.5+.5*Math.cos(angle*48)))/radius;pos.setX(i,x*factor);pos.setZ(i,z*factor);}}
  crownGeometry.computeVertexNormals();crownGeometry.rotateZ(Math.PI/2);const crownMesh=new THREE.Mesh(crownGeometry,metal);crownMesh.position.x=4-47.5;crown.add(crownMesh);
  const disk=new THREE.Mesh(new THREE.CylinderGeometry(5.9,5.9,.18,96),new THREE.MeshStandardMaterial({color:0xb0bfd1,metalness:1,roughness:.32}));disk.rotation.z=Math.PI/2;disk.position.x=.15-47.5;crown.add(disk);
  const collar=add(new THREE.CylinderGeometry(6.9,6.9,2.2,96),collarMat,'13.8-mm-shoulder');collar.rotation.z=Math.PI/2;collar.position.x=7.1-47.5;
  // Lug on crown flank. It adds no axial length and never approaches the antenna.
  const lug=add(new THREE.TorusGeometry(1.8,.65,12,36),metal,'flank-lug');lug.rotation.x=Math.PI/2;lug.position.set(11-47.5,-13.1,0);
  const cordCurve=new THREE.CatmullRomCurve3([new THREE.Vector3(-36.5,-14,0),new THREE.Vector3(-40,-21,-1),new THREE.Vector3(-31,-24,-1),new THREE.Vector3(-31,-19,0),new THREE.Vector3(-36.5,-14,0)]);
  add(new THREE.TubeGeometry(cordCurve,48,.38,8,false),new THREE.MeshStandardMaterial({color:0x343e51,roughness:.9}),'cord-loop-illustration');
  // The full-width rear lid's visible parting line.
  const seamPoints=[];
  const rearZ=y=>-Math.sqrt(Math.max(0,7.5**2-Math.max(0,Math.abs(y)-6)**2))-.04;
  // Follow the rear surface, including its stadium flanks, instead of burying an ellipse.
  const outline=new THREE.Shape();outline.moveTo(11,-11.6);outline.lineTo(65,-11.6);outline.quadraticCurveTo(68,-11.6,68,-8.6);outline.lineTo(68,8.6);outline.quadraticCurveTo(68,11.6,65,11.6);outline.lineTo(11,11.6);outline.quadraticCurveTo(8,11.6,8,8.6);outline.lineTo(8,-8.6);outline.quadraticCurveTo(8,-11.6,11,-11.6);
  for(const point of outline.getSpacedPoints(240))seamPoints.push(new THREE.Vector3(point.x-47.5,point.y,rearZ(point.y)));
  const seam=new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(seamPoints),new THREE.LineBasicMaterial({color:0x13100d}));seam.name='rear-parting-line';group.add(seam);
  for(let i=0;i<4;i++){const pad=add(new THREE.CylinderGeometry(1,1,.12,36),new THREE.MeshStandardMaterial({color:0xb8872d,metalness:.85,roughness:.4,envMapIntensity:.55}),`gold-dock-pad-${i+1}`);pad.rotation.x=Math.PI/2;pad.position.set(35.19+i*2.54-47.5,0,-7.5);}
  const haloLights=[-8,8].map(y=>{const light=new THREE.PointLight(0xff986f,0,32,2);light.position.set(71.75-47.5,y,9);group.add(light);return light;});
  let lastState='',lastFrame=-1,stateStart=0,lastReaction=0;
  return {group,crown,dimensions,screen,haloLights,update({screen:lit=true,screenLevel=Number(lit),halo=0,state='resting',crown:angle=0,pressed=false,time=0,reduced=false,clickRate=1,reaction=0}={}) {
    screen.visible=screenLevel>.001;screenMaterial.color.setScalar(screenLevel);crown.rotation.x=angle;crown.position.x=pressed?.4:0;
    litRingMat.opacity=halo;litRingMat.color.set(0xff9e76).multiplyScalar(.65+.35*halo);glowMat.opacity=halo*.24;
    haloLights.forEach(light=>light.intensity=halo*110);
    const frame=reduced?0:Math.floor(time*24);
    if(lastState!==state||lastReaction!==reaction){stateStart=time;lastReaction=reaction;}
    if(screen.visible&&(lastState!==state||lastFrame!==frame)){drawMascot(ctx,state,time,reduced,time-stateStart,clickRate);texture.needsUpdate=true;lastState=state;lastFrame=frame;}
  }};
}
