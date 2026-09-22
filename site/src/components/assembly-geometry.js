import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';

const yzToX=new THREE.Matrix4().set(0,0,1,0, 1,0,0,0, 0,1,0,0, 0,0,0,1);
export const box=(x,y,z,r=.15)=>new RoundedBoxGeometry(x,y,z,2,Math.min(r,x/3,y/3,z/3));
export function cylinderX(radius,length){const geometry=new THREE.CylinderGeometry(radius,radius,length,64);geometry.rotateZ(Math.PI/2);return geometry;}

/** An axial ring, with optional internal race grooves or external serrations.
 * The 24 grooves are geometry, not a texture or a row of decorative balls. */
export function ringX(outer,inner,length,{grooves=0,teeth=0,arc=Math.PI*2,start=0}={}){
  const steps=Math.max(64,grooves*16,teeth*8),positions=[],normals=[],uv=[],indices=[];
  const radial=(theta,hole)=>hole?inner+(grooves?.12*(.5+.5*Math.cos(theta*grooves)):0):outer-(teeth?.19*(.5+.5*Math.cos(theta*teeth)):0);
  const vertex=(x,y,z,nx,ny,nz,u,v)=>{const id=positions.length/3;positions.push(x,y,z);normals.push(nx,ny,nz);uv.push(u,v);return id;};
  // The topology is known: explicit annular strips avoid an expensive polygon
  // triangulation when the detailed module joins a scene that is already live.
  for(const sign of [-1,1]){
    const base=positions.length/3;
    for(let i=0;i<=steps;i++){const a=start+i/steps*arc;for(const hole of [false,true]){const r=radial(a,hole);vertex(sign*length/2,Math.cos(a)*r,Math.sin(a)*r,sign,0,0,i/steps,Number(hole));}}
    for(let i=0;i<steps;i++){const a=base+i*2,b=a+1,c=a+2,d=a+3;sign<0?indices.push(a,b,c,b,d,c):indices.push(a,c,b,b,c,d);}
  }
  for(const hole of [false,true]){
    if(hole&&!inner)continue;const base=positions.length/3;
    for(let i=0;i<=steps;i++){
      const a=start+i/steps*arc,r=radial(a,hole),dr=hole?(grooves?-.06*grooves*Math.sin(a*grooves):0):(teeth?.095*teeth*Math.sin(a*teeth):0);
      const n=new THREE.Vector3(0,dr*Math.sin(a)+r*Math.cos(a),-dr*Math.cos(a)+r*Math.sin(a)).normalize().multiplyScalar(hole?-1:1);
      for(const side of [-1,1])vertex(side*length/2,Math.cos(a)*r,Math.sin(a)*r,n.x,n.y,n.z,i/steps,(side+1)/2);
    }
    for(let i=0;i<steps;i++){const a=base+i*2,b=a+1,c=a+2,d=a+3;hole?indices.push(a,b,c,b,d,c):indices.push(a,c,b,b,c,d);}
  }
  if(arc<Math.PI*2)for(const [a,sign]of[[start,-1],[start+arc,1]]){
    const base=positions.length/3,ny=-Math.sin(a)*sign,nz=Math.cos(a)*sign;
    for(const side of [-1,1])for(const hole of [false,true]){const r=radial(a,hole);vertex(side*length/2,Math.cos(a)*r,Math.sin(a)*r,0,ny,nz,(side+1)/2,Number(hole));}
    sign<0?indices.push(base,base+2,base+1,base+1,base+2,base+3):indices.push(base,base+1,base+2,base+1,base+3,base+2);
  }
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('normal',new THREE.Float32BufferAttribute(normals,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);return g;
}

export function stadiumShape(inset=0){
  const r=7.5-inset,s=new THREE.Shape();
  s.moveTo(-6,-r);s.lineTo(6,-r);s.absarc(6,0,r,-Math.PI/2,Math.PI/2,false);s.lineTo(-6,r);s.absarc(-6,0,r,Math.PI/2,Math.PI*1.5,false);return s;
}
export function opticalWeb(){
  const s=stadiumShape(),hole=new THREE.Path();hole.moveTo(-2.8,2.95);hole.lineTo(-2.8,5.05);hole.lineTo(2.8,5.05);hole.lineTo(2.8,2.95);hole.closePath();s.holes.push(hole);
  const g=new THREE.ExtrudeGeometry(s,{depth:1.5,bevelEnabled:false,curveSegments:48});g.applyMatrix4(yzToX);g.translate(23.5,0,0);return g;
}
export function capLining(){
  const g=new THREE.ExtrudeGeometry(stadiumShape(1.25),{depth:19.8,bevelEnabled:false,curveSegments:48});
  // The opening has no front face. Reverse-side rendering shows the machined
  // cavity, including its closed inner end, through the open cap mouth.
  const p=g.attributes.position,keep=[];
  for(let i=0;i<p.count;i+=3)if(![i,i+1,i+2].every(k=>Math.abs(p.getZ(k))<.001))keep.push(i,i+1,i+2);
  g.setIndex(keep);g.applyMatrix4(yzToX);g.translate(25,0,0);return g;
}
export function capLip(){
  const s=stadiumShape(),hole=stadiumShape(1.25);s.holes.push(hole);
  const g=new THREE.ExtrudeGeometry(s,{depth:.18,bevelEnabled:false,curveSegments:48});g.applyMatrix4(yzToX);g.translate(25,0,0);return g;
}
export function tube(points,radius=.12){return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),32,radius,8,false);}
export function springContact(){
  // 0.09 mm formed strip, with a flat wiping tip. Local z at the top of
  // the compressed tip is 3.2 mm; the PCB top datum is 1.8 mm.
  const path=new THREE.CurvePath();
  path.add(new THREE.LineCurve3(new THREE.Vector3(18,0,1.94),new THREE.Vector3(19.4,0,1.94)));
  path.add(new THREE.CubicBezierCurve3(new THREE.Vector3(19.4,0,1.94),new THREE.Vector3(20.25,0,1.94),new THREE.Vector3(20.1,0,3.155),new THREE.Vector3(18.6,0,3.155)));
  const positions=[],indices=[],weights=[];
  for(let i=0;i<=64;i++){
    const t=i/64,p=path.getPoint(t),tangent=path.getTangent(t),nx=-tangent.z,nz=tangent.x;
    for(const [side,face]of[[-1,-1],[1,-1],[1,1],[-1,1]]){positions.push(p.x+face*.045*nx,side*.65,p.z+face*.045*nz);weights.push(t*t*(3-2*t));}
    if(i<64)for(let j=0;j<4;j++){const a=i*4+j,b=i*4+(j+1)%4;indices.push(a,b,a+4,b,b+4,a+4);}
  }
  indices.push(0,2,1,0,3,2,256,257,258,256,258,259);
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();
  g.userData.restPositions=new Float32Array(positions);g.userData.flexWeights=weights;return g;
}
export function waveWasher(){
  const points=[];for(let i=0;i<=144;i++){const a=i/144*Math.PI*2;points.push(new THREE.Vector3(Math.sin(a*3)*.24,Math.cos(a)*4.2,Math.sin(a)*4.2));}
  const g=new THREE.BufferGeometry(),positions=[],indices=[];
  points.forEach((p,i)=>{const a=i/144*Math.PI*2;for(const r of [3.6,4.8])positions.push(p.x,Math.cos(a)*r,Math.sin(a)*r);if(i<144){const n=i*2;indices.push(n,n+1,n+2,n+1,n+3,n+2);}});
  g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();return g;
}
export function labelTexture(text,{color='#b7adff',background='transparent',width=512,height=128}={}){
  const canvas=document.createElement('canvas');canvas.width=width;canvas.height=height;const ctx=canvas.getContext('2d');
  ctx.fillStyle=background;ctx.fillRect(0,0,width,height);ctx.fillStyle=color;ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='500 42px monospace';ctx.fillText(text,width/2,height/2);
  const t=new THREE.CanvasTexture(canvas);t.colorSpace=THREE.SRGBColorSpace;return t;
}

export function splitRear(geometry){
  const position=geometry.attributes.position,index=geometry.index.array,front=[],back=[];
  for(let i=0;i<index.length;i+=3){const tri=[index[i],index[i+1],index[i+2]],x=tri.reduce((n,k)=>n+position.getX(k),0)/3,z=tri.reduce((n,k)=>n+position.getZ(k),0)/3;(z< -4.3&&x> -38.5&&x<21?back:front).push(...tri);}
  const a=geometry.clone(),b=geometry.clone();a.setIndex(front);b.setIndex(back);return [a,b];
}

export function springLeaf(radius=3.92){
  // Tangential cantilever: clamped root, curved strip and a tip under the ball.
  const s=new THREE.Shape();s.moveTo(1.8,-3.8);s.bezierCurveTo(2.7,-2.9,radius,-1.5,radius,0);s.lineTo(radius-.12,0);s.bezierCurveTo(radius-.12,-1.5,2.58,-2.9,1.68,-3.8);s.closePath();
  const g=new THREE.ExtrudeGeometry(s,{depth:1.5,bevelEnabled:false,curveSegments:12});g.applyMatrix4(yzToX);g.translate(-.75,0,0);return g;
}
