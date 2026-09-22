import * as THREE from 'three';
import {box,cylinderX,ringX,opticalWeb,capLining,capLip,tube,springContact,waveWasher,labelTexture,splitRear,springLeaf} from './assembly-geometry.js';

const clamp=v=>Math.min(1,Math.max(0,v)),smooth=v=>{v=clamp(v);return v*v*(3-2*v);};
const X=value=>value-47.5;
const crownIds=['crown','race','balls','leaves','sleeve','washer','retainer','magnet','diaphragm','sensors'];

/** Augments the SAME exterior model. Physical dimensions follow the project's
 * coaxial baseline. Exploded offsets and component artwork are explanatory. */
export function createAssembly(product){
  const rig=new THREE.Group();rig.name='assembly-rig';
  for(const child of [...product.group.children])rig.add(child);product.group.add(rig);
  const parts={},pickables=[],materials=new Set();let selected='shell',previousAngle=NaN,previousDeflection=NaN,antennaWeight=0;
  const material=(color,metalness=0,roughness=.45)=>new THREE.MeshStandardMaterial({color,metalness,roughness});
  const silver=material(0xa4b4ca,.92,.31),gold=material(0xcda975,.78,.3),black=material(0x0a1220,.1,.5),pom=material(0xc8ccd2,0,.33),ceramic=material(0x161b29,.2,.12),rubber=material(0x404657,0,.9),boardMat=material(0x173638,.25,.46);
  const standard=product.group.getObjectByName('PC-ABS-shell').material;
  function part(id,originals=[]){
    const group=new THREE.Group();group.name='part-'+id;group.userData.partId=id;rig.add(group);
    for(const name of originals){const object=rig.getObjectByName(name);if(object)group.add(object);}
    return parts[id]={group,meshes:[],opacity:1};
  }
  function add(id,geometry,mat,position=[0,0,0],name=''){
    const mesh=new THREE.Mesh(geometry,mat);mesh.position.set(...position);mesh.name=name||id;parts[id].group.add(mesh);return mesh;
  }
  function label(id,text,width,height,position){const m=new THREE.MeshBasicMaterial({map:labelTexture(text),transparent:true,depthWrite:false,toneMapped:false});return add(id,new THREE.PlaneGeometry(width,height),m,position);}
  function moveOriginal(id,names){return part(id,names);}

  moveOriginal('shell',['PC-ABS-shell','flank-lug','cord-loop-illustration','13.8-mm-shoulder']);
  moveOriginal('display',['16x34-glass-lens','11.6x26.2-clear-window','10.96x25.58-AMOLED','lens-specular']);
  moveOriginal('crown',['48-serration-crown']);
  moveOriginal('cap',['6061-T6-antenna-cap','cap-edge-chamfer']);
  moveOriginal('halo',['1.5-mm-optical-PC-halo','halo-emission','halo-local-bloom']);
  moveOriginal('lid',['rear-parting-line',...Array.from({length:4},(_,i)=>'gold-dock-pad-'+(i+1))]);
  for(const id of ['board','cell','haptic','race','balls','leaves','sleeve','washer','retainer','magnet','diaphragm','sensors','feed','contact'])part(id);

  // Split the approved exterior at its rear seam. Assembled, these surfaces
  // occupy their original coordinates; opening the door reveals actual volume.
  const shell=parts.shell.group.getObjectByName('PC-ABS-shell');
  const [front,rear]=splitRear(shell.geometry);shell.geometry=front;
  add('lid',rear,standard,[0,0,0],'moulded-rear-door');
  add('lid',box(55,19,.8,.4),standard,[X(38.5),0,-5.4],'door-inner-web');
  const gasket=[];for(let i=0;i<=80;i++){const a=i/80*Math.PI*2;gasket.push([X(38.5)+27.6*Math.sign(Math.cos(a))*Math.abs(Math.cos(a))**.25,9.5*Math.sign(Math.sin(a))*Math.abs(Math.sin(a))**.35,-5]);}
  add('lid',tube(gasket,.24),rubber,[0,0,0],'perimeter-gasket');
  for(const y of [-8.5,8.5]){
    add('shell',box(51,1.2,1.8,.2),standard,[X(40),y,3.9],'board-support-rib');
    const screw=add('lid',new THREE.CylinderGeometry(.85,.85,3,16),silver,[X(11),y,-5.3],'M1.4-lid-screw');screw.rotation.x=Math.PI/2;
    add('shell',new THREE.TorusGeometry(1,.35,8,24),gold,[X(11),y,-3.7],'threaded-insert');
  }
  add('display',box(31,13.5,.78,.15),black,[X(35),0,6.84],'AMOLED-module');
  add('display',box(34,16,.45,.15),black,[X(35),0,7.16],'laminated-lens-edge');
  add('display',box(6,5,.1,.01),gold,[X(49),0,5.95],'display-flex-tail');
  add('display',tube([[X(49),0,6.5],[X(50),0,4],[X(47),0,2.6]],.32),gold,[0,0,0],'folded-panel-flex');

  add('board',box(44,23,.8,.08),boardMat,[X(38),0,1.4],'six-layer-PCB');
  add('board',box(8,23,.8,.08),boardMat,[X(64),0,1.4],'RF-board-edge');
  add('board',box(12,11,1.28,.25),silver,[X(26),0,2.44],'LTE-M-radio-SiP');
  label('board','LTE–M',10,2.5,[X(26),0,3.09]);
  // Representative package placements follow the report's clearances. There is
  // no decorative copper beyond X=63 except the specified antenna feed.
  for(const [x,y,w,h]of[[39,8.3,5,3],[46,-8.5,4,3],[55,8.3,4,3],[33,-8.5,3,2.5],[19,8.5,2.5,2.5],[49,0,3.3,5]]){
    add('board',box(w,h,.75,.1),black,[X(x),y,2.16]);
    for(const side of [-1,1])for(let k=0;k<4;k++)add('board',box(.3,.65,.12,.02),silver,[X(x-w*.36+k*w*.24),y+side*(h/2+.22),1.94]);
  }
  for(let i=0;i<16;i++){
    const x=20+i*2.55,y=i%2?10.25:-10.25;
    add('board',box(1.1,.65,.45,.04),i%3?rubber:gold,[X(x),y,2.03]);
    add('board',box(1.9,.16,.035,.01),gold,[X(x),y-1.1,1.82]);
  }
  const rfLabel=label('board','RF',3,2,[X(65),-7,1.83]);rfLabel.name='RF-edge-label';
  add('board',box(6.5,.22,.07,.02),gold,[X(63.3),0,1.84],'antenna-feed-trace');
  const motor=add('haptic',new THREE.CylinderGeometry(4,4,4.05,64),silver,[X(56),0,3.85],'170Hz-LRA');motor.rotation.x=Math.PI/2;
  add('haptic',box(10,9,.3,.2),gold,[X(56),0,1.95],'LRA-board-bracket');
  label('haptic','170',5,1.8,[X(56),0,5.90]);

  const cellMat=material(0x84939b,.68,.47);
  add('cell',box(43,23,6,.65),cellMat,[X(40.5),0,-2.15],'connectorised-pouch-cell');
  add('cell',box(2.3,21,6.1,.2),gold,[X(20.15),0,-2.15],'cell-insulated-head');
  add('cell',box(39,19,.15,.1),rubber,[X(41),0,.94],'PET-insulator');
  label('cell','Li–ion  /  3.7 V',30,6,[X(41),0,-5.18]).rotation.y=Math.PI;
  add('cell',tube([[X(20),6,0],[X(18),5,-.2],[X(17.5),1,1]],.22),gold,[0,0,0],'cell-connector-tail');
  add('cell',box(4,4,.12,.01),new THREE.MeshStandardMaterial({color:0xdab080,roughness:.6}),[X(59),-8,-5.2],'stretch-release-tab');

  // Hollow crown cup and its integral hub. The earlier exterior is retained
  // in place, replacing its solid hidden rear face with the real cup opening.
  const crownMesh=product.crown.children.find(o=>o.isMesh&&o.geometry.type==='CylinderGeometry');
  crownMesh.geometry=ringX(6.5,5.5,6.7,{teeth:48});crownMesh.position.x=X(4.65);
  const frontWall=new THREE.Mesh(ringX(6.5,0,1.3,{teeth:48}),crownMesh.material);frontWall.position.x=X(.65);product.crown.add(frontWall);
  for(const [start,end,r]of[[1.3,2.6,3.5],[2.6,3.7,3.1],[3.7,4.15,3.5],[4.15,5,3.1],[5,6.2,3.5]]){const hub=new THREE.Mesh(cylinderX(r,end-start),silver);hub.position.x=X((start+end)/2);product.crown.add(hub);}
  const pocket=new THREE.Mesh(ringX(3.5,3.025,2.6),silver);pocket.position.x=X(7.5);product.crown.add(pocket);
  const race=add('race',ringX(5.305,4.6,2.6,{grooves:24}),silver,[X(3.1),0,0],'24-groove-race');
  race.userData.grooves=24;
  for(const sign of [-1,1])add('balls',new THREE.SphereGeometry(.4,32,20),ceramic,[X(3.1),sign*4.32,0],'Si3N4-ball-'+(sign===1?'A':'B'));
  const springs=[];for(const sign of [-1,1]){const leaf=add('leaves',springLeaf(),gold,[X(3.1),0,0],'BeCu-leaf-'+sign);leaf.rotation.x=sign===1?0:Math.PI;springs.push(leaf);}
  // A small cutaway through the pocket region keeps the real balls visible.
  for(const start of [.22,Math.PI+.22])add('sleeve',ringX(4.5,3.53,2.45,{arc:Math.PI-.44,start}),pom,[X(3.175),0,0],'sleeve-pocket-cutaway');
  add('sleeve',ringX(5.45,3.55,4),pom,[X(6.4),0,0],'POM-journal');
  add('sleeve',ringX(6.6,3.8,.5),pom,[X(8.65),0,0],'sleeve-flange');
  for(const y of [-7.5,7.5]){add('sleeve',box(1.5,6,3,.3),pom,[X(8.3),y,0],'cartridge-ear');add('sleeve',cylinderX(.5,1.6),pom,[X(9.5),y*.8,0],'PCB-locating-pin');}
  const washer=add('washer',waveWasher(),gold,[X(1.625),0,0],'three-wave-washer');washer.material=washer.material.clone();washer.material.side=THREE.DoubleSide;
  const retain=new THREE.TorusGeometry(3.64,.2,12,80,Math.PI*1.9);retain.rotateY(Math.PI/2);add('retainer',retain,gold,[X(4.78),0,0],'BeCu-retaining-C-ring');
  add('magnet',cylinderX(3,2.5),silver,[X(7.5),0,0],'diametric-sensing-magnet');
  const stripe=add('magnet',box(.04,5,.1,.01),new THREE.MeshBasicMaterial({color:0xb7adff}),[X(8.77),0,0]);stripe.rotation.y=Math.PI/2;
  add('diaphragm',cylinderX(4.7,.30),rubber,[X(9),0,0],'LSR-diaphragm-skin');
  add('diaphragm',ringX(6.25,4.7,.8),rubber,[X(9),0,0],'diaphragm-rim-bead');
  add('diaphragm',cylinderX(.7,.75),pom,[X(9.525),2.33,2.33],'off-axis-PEEK-pip');
  add('sensors',box(.6,22,10,.15),boardMat,[X(10.78),0,0],'satellite-board');
  add('sensors',box(.75,3,3,.15),black,[X(10.105),0,0],'angle-sensor');
  for(const [y,z]of[[4,0],[0,4]])add('sensors',box(.5,1.4,1.1,.08),black,[X(10.2),y,z],'Hall-wake-latch');
  add('sensors',box(.53,2.6,1.6,.1),silver,[X(10.215),2.33,2.33],'off-axis-press-switch');
  add('sensors',tube([[X(11.1),7,0],[X(13),7,1],[X(16.5),6,1.5]],.28),gold,[0,0,0],'satellite-flex');

  // Optical web with a real feed aperture. The tab is integral to the cap;
  // its plated land is a finish, not an extra loose block in the assembly.
  const web=parts.halo.group.getObjectByName('1.5-mm-optical-PC-halo');web.geometry=opticalWeb();
  for(const id of ['halo-emission','halo-local-bloom'])parts.halo.group.getObjectByName(id).geometry=web.geometry;
  add('halo',box(8,1.4,1.4,.2),web.material,[X(67),10,2.5],'light-injection-guide');
  // PCB top is z=1.8; the plated contact face is z=3.2 (+1.4 mm).
  add('cap',box(9,5,1.5,.15),silver,[X(70),0,4.0],'integral-L-feed-tab');
  add('cap',box(1.5,5,4.8,.2),silver,[X(74),0,2.0],'tab-root');
  add('feed',box(3,4,.05,.015),gold,[X(67),0,3.225],'gold-plated-underside-land');
  const contact=add('contact',springContact(),gold,[0,0,0],'vertical-deflection-contact');
  add('contact',box(2.2,2,.15,.06),gold,[X(66),0,1.88],'SMT-contact-foot');
  // Internal cap cavity: remove the hidden solid front fan, add a dark inner
  // wall. The assembled outer surface remains the approved cap geometry.
  const cap=parts.cap.group.getObjectByName('6061-T6-antenna-cap'),p=cap.geometry.attributes.position,idx=cap.geometry.index.array,kept=[];
  for(let i=0;i<idx.length;i+=3)if(![idx[i],idx[i+1],idx[i+2]].every(k=>Math.abs(p.getX(k)-25)<.001))kept.push(idx[i],idx[i+1],idx[i+2]);
  cap.geometry=cap.geometry.clone();cap.geometry.setIndex(kept);
  const lining=silver.clone();lining.side=THREE.BackSide;lining.roughness=.46;
  add('cap',capLining(),lining,[0,0,0],'machined-cap-cavity');
  parts.cap.group.getObjectByName('cap-edge-chamfer').geometry=capLip();

  // Light construction axes, attached to the object and visible only exploded.
  const guides=new THREE.Group();rig.add(guides);
  const guideMat=new THREE.LineDashedMaterial({color:0x8793ae,transparent:true,opacity:0,dashSize:1.2,gapSize:1.4,depthWrite:false});
  for(const points of [[[X(-30),0,0],[X(115),0,0]],[[X(35),0,-48],[X(35),0,51]]]){const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p))),guideMat);line.computeLineDistances();guides.add(line);}

  for(const [id,part]of Object.entries(parts))part.group.traverse(object=>{
    if(!object.isMesh&&!object.isLine)return;object.userData.partId=id;
    const dynamic=['10.96x25.58-AMOLED','halo-emission','halo-local-bloom'].includes(object.name);
    object.userData.sourceMaterial=dynamic?object.material:null;object.material=object.material.clone();object.userData.dynamicMaterial=dynamic&&object.name!=='10.96x25.58-AMOLED';object.userData.baseOpacity=object.material.opacity;
    // One transparent shader variant allows every part to fade continuously.
    // Changing transparent without recompiling leaves Three's OPAQUE define on.
    object.material.transparent=true;object.material.needsUpdate=true;
    if(object.material.color)object.userData.baseColor=object.material.color.clone();
    part.meshes.push(object);materials.add(object.material);if(object.isMesh)pickables.push(object);
  });
  const internal=new Set(['board','cell','haptic',...crownIds.filter(x=>x!=='crown'),'feed','contact']);
  const exploded={shell:[0,0,0],display:[0,8,37],board:[0,1,14],cell:[0,-2,-15],haptic:[3,15,27],lid:[0,-5,-36],cap:[29,0,0],halo:[12,0,0],feed:[29,0,0],contact:[0,1,14]};
  const spread={crown:-23,washer:-15,race:-8,balls:0,leaves:3,sleeve:10,retainer:17,magnet:25,diaphragm:33,sensors:40};
  const partStage={crown:1,race:1,balls:1,leaves:1,sleeve:1,washer:1,retainer:1,magnet:1,diaphragm:1,sensors:1,board:2,haptic:2,contact:2,display:3,cell:4,lid:5};
  function update(f){
    const e=f.explode??0,c=f.crownStudy??0,d=f.detentStudy??0,a=f.antennaStudy??0,building=f.buildStudy??0,b=f.buildProgress??0;
    antennaWeight=a;
    rig.position.set(-(f.focusX??0),0,0);
    const angle=f.detentAngle??0,radius=4.26+.06*Math.cos(angle*24);
    const station=b*6,staged=smooth(station),boardEntry=smooth((station-2)/.35),boardSeat=smooth((station-2.35)/.45);
    const boardPosition=station<2?new THREE.Vector3(0,1+34*staged,14-30*staged):new THREE.Vector3(0,35*(1-boardEntry),-16*(1-boardSeat));
    for(const [id,part]of Object.entries(parts)){
      let reveal=internal.has(id)?smooth(e*3):1;
      if(crownIds.includes(id))reveal*=1-a;else reveal*=1-c-d;
      if(d&&!['race','balls','leaves','sleeve'].includes(id))reveal*=1-d;
      if(a&&['display','cell','haptic','lid','shell'].includes(id))reveal*=1-a;
      if(id==='contact'||id==='feed')reveal=Math.max(reveal,a);
      part.opacity=reveal;part.group.visible=reveal>.003;
      let offset=exploded[id]??[-19,0,0];
      let amount=e;
      if(building){const stage=partStage[id]??0;const fitted=smooth((b*6-stage)/.8);amount*=1-building*fitted;}
      const crown=crownIds.includes(id);
      part.group.position.set(offset[0]*amount,offset[1]*amount,offset[2]*amount);
      part.group.rotation.x=(id==='cap'||id==='feed')?a*Math.PI*.85:0;
      if(crown){part.group.position.x=THREE.MathUtils.lerp(-19*amount,spread[id]??0,c);part.group.position.x=THREE.MathUtils.lerp(part.group.position.x,0,d);}
      if(crown&&building){
        // The cartridge enters from the open rear of the tray and advances
        // crown-first toward the nose. It is not pushed in from outside.
        const station=b*6,stage=smooth(station),enter=smooth((station-1)/.4),seat=smooth((station-1.4)/.4);
        const staging=new THREE.Vector3(-19+28*stage,-17*stage,-23*stage);
        if(station>=1)staging.set(9*(1-seat),-17*(1-enter),-23*(1-enter));
        part.group.position.lerp(staging,building);
      }
      if(building&&['board','contact','haptic'].includes(id)){
        const position=boardPosition.clone();if(id==='haptic'){const prepared=smooth(station/.8);position.x+=3*(1-prepared);position.y+=14*(1-prepared);position.z+=13*(1-prepared);}
        part.group.position.lerp(position,building);
      }
      if(building&&id==='cell'){
        const enter=smooth((station-4)/.35),seat=smooth((station-4.35)/.45);
        const position=station<4?new THREE.Vector3(0,-2-33*staged,-15-3*staged):new THREE.Vector3(0,-35*(1-enter),-18*(1-seat));part.group.position.lerp(position,building);
      }
      if(a){
        const positions={cap:[17,4,0],halo:[5,0,0],feed:[17,4,0],contact:[-5,-2,-5],board:[-5,-2,-5]};
        if(positions[id])part.group.position.lerp(new THREE.Vector3(...positions[id]),a);
      }
      for(const mesh of part.meshes){
        const m=mesh.material;
        if(mesh.userData.sourceMaterial)m.color.copy(mesh.userData.sourceMaterial.color);
        let local=1;
        if(id==='sleeve')local*=1-d*(mesh.name==='sleeve-pocket-cutaway'?.88:1);
        if(id==='board'&&!['RF-board-edge','RF-edge-label','antenna-feed-trace'].includes(mesh.name))local*=1-a;
        const opacity=(mesh.userData.dynamicMaterial?mesh.userData.sourceMaterial.opacity:mesh.userData.baseOpacity)*reveal*local;
        mesh.visible=opacity>.003; // Product.update owns screen visibility too.
        if(mesh.name==='10.96x25.58-AMOLED')mesh.visible&&=(f.screenLevel??1)>.001;
        mesh.userData.pickOpacity=opacity;
        m.opacity=opacity;m.depthWrite=opacity>.96;
        const highlight=(id===selected?.045:0)*(f.study??0)*(1-building*b);
        if(m.emissive){m.emissive.set(id===selected?0x57409c:0);m.emissiveIntensity=highlight;}
        if(['board','contact','feed','cap'].includes(id)&&m.emissive){
          const stage={board:0,contact:1,feed:2,cap:3}[id],p=f.feedProgress??-1;
          const pulse=p<0?0:Math.max(0,1-Math.abs(p*4-stage-.5)/.8);
          if(pulse>0){m.emissive.set(0xa6efd2);m.emissiveIntensity=pulse*.65;}
        }
      }
    }
    race.rotation.x=angle;product.crown.rotation.x+=(angle*d);
    parts.balls.meshes.forEach((ball,i)=>ball.position.y=(i===0?-1:1)*radius);
    if(!Number.isFinite(previousAngle)||Math.abs(angle-previousAngle)>.0001){for(const leaf of springs){leaf.geometry.dispose();leaf.geometry=springLeaf(radius-.4);}previousAngle=angle;}
    const deflection=e*.6*(1-building)+building*(station<2?.6:Math.min(.6,Math.max(0,-boardPosition.z)));
    if(!Number.isFinite(previousDeflection)||Math.abs(deflection-previousDeflection)>.0001){
      const geometry=contact.geometry,positions=geometry.attributes.position,rest=geometry.userData.restPositions,weights=geometry.userData.flexWeights;
      for(let i=0;i<positions.count;i++)positions.setZ(i,rest[i*3+2]+deflection*weights[i]);positions.needsUpdate=true;geometry.computeVertexNormals();geometry.computeBoundingBox();geometry.computeBoundingSphere();previousDeflection=deflection;
    }
    guideMat.opacity=.11*e*(1-d)*(1-a)*(1-c*.5);guides.visible=guideMat.opacity>.002;
    if(building&&b>.99)guideMat.opacity=0;
  }
  function select(id){if(parts[id])selected=id;}
  const bounds=new THREE.Box3();
  function anchor(id){
    const part=parts[id];if(!part)return null;part.group.updateWorldMatrix(true,true);
    if(id==='board')return new THREE.Vector3(X(42+22*antennaWeight),0,2).applyMatrix4(part.group.matrixWorld);
    bounds.setFromObject(['balls','leaves'].includes(id)?part.meshes[0]:part.group);return bounds.getCenter(new THREE.Vector3());
  }
  update({});
  return{rig,parts,materials,pickables,update,select,anchor,get selected(){return selected;}};
}
