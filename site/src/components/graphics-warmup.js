/** Start the graphics driver without blocking text, navigation or scrolling.
 * The visible renderer still owns the real canvas; this worker only prepares
 * a 1-pixel context while its module downloads. Unsupported browsers fall back. */
export function warmGraphics(){
  if(!('Worker'in window)||!('OffscreenCanvas'in window))return{ready:Promise.resolve(),release(){}};
  let worker,url,timer,finish;
  const ready=new Promise(resolve=>{finish=resolve;});
  function release(){clearTimeout(timer);worker?.terminate();if(url){URL.revokeObjectURL(url);url=null;}finish();}
  try{
    url=URL.createObjectURL(new Blob([`try{const canvas=new OffscreenCanvas(1,1);self.context=canvas.getContext('webgl2',{powerPreference:'default'});self.context?.clear(self.context.COLOR_BUFFER_BIT);}catch{}postMessage('ready');`],{type:'text/javascript'}));
    worker=new Worker(url);worker.onmessage=()=>{clearTimeout(timer);finish();};worker.onerror=()=>release();timer=setTimeout(finish,1000);
  }catch{release();}
  return{ready,release};
}
