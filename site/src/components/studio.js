import * as THREE from 'three';
/** Build-time source for the studio's prefiltered reflection map. */
export function createStudioEnvironment(renderer){
 const studio=new THREE.Scene();studio.background=new THREE.Color(0x5c6a82);
 const softbox=(w,h,p,intensity,color=0xffffff)=>{const material=new THREE.MeshBasicMaterial({color:new THREE.Color(color).multiplyScalar(intensity),side:THREE.DoubleSide});const box=new THREE.Mesh(new THREE.PlaneGeometry(w,h),material);box.position.set(...p);box.lookAt(0,0,0);studio.add(box);};
 softbox(110,170,[-85,100,100],1.5);softbox(50,160,[110,20,60],1.2);softbox(160,80,[0,120,-30],1.8);softbox(200,40,[-30,-100,40],.65,0xbacbff);softbox(150,130,[0,0,-120],.7);
 const pmrem=new THREE.PMREMGenerator(renderer);const map=pmrem.fromScene(studio,.04,.1,100,{size:128});studio.traverse(o=>{o.geometry?.dispose();o.material?.dispose();});pmrem.dispose();return map;
}
