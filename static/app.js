const chat=document.querySelector("#chat"), input=document.querySelector("#input"), send=document.querySelector("#send");
const key="tambot_messages"; let messages=JSON.parse(localStorage.getItem(key)||"[]");
function render(){
  chat.innerHTML="";
  if(!messages.length){chat.innerHTML=`<div class="welcome"><div class="orb">T</div><h1>Hey, I’m Thameem.</h1><p>I’m here to help with whatever you want.</p><small>Created by itzz_thammi</small></div>`;return}
  for(const m of messages){const d=document.createElement("div");d.className="msg "+m.role;d.innerHTML=`<div class="bubble"></div>`;d.querySelector(".bubble").textContent=m.content;chat.appendChild(d)}
  chat.scrollTop=chat.scrollHeight;
}
function save(){localStorage.setItem(key,JSON.stringify(messages));}
async function sendMsg(){
 const text=input.value.trim(); if(!text)return;
 messages.push({role:"user",content:text}); save(); render(); input.value="";
 const bubble=document.createElement("div"); bubble.className="msg assistant"; bubble.innerHTML='<div class="bubble">…</div>'; chat.appendChild(bubble); chat.scrollTop=chat.scrollHeight;
 try{
   const r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({messages:messages.slice(-30)})});
   if(!r.ok) throw new Error(await r.text());
   const reader=r.body.getReader(), dec=new TextDecoder(); let out="";
   while(true){const {done,value}=await reader.read();if(done)break;out+=dec.decode(value,{stream:true});bubble.querySelector(".bubble").textContent=out;chat.scrollTop=chat.scrollHeight}
   messages.push({role:"assistant",content:out});save();
 }catch(e){bubble.querySelector(".bubble").textContent="TamBOT connection error: "+e.message}
}
send.onclick=sendMsg; input.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendMsg()}});
document.querySelector("#newChat").onclick=()=>{messages=[];save();render()};
document.querySelector("#clearMemory").onclick=()=>{localStorage.removeItem(key);messages=[];render()};
document.querySelector("#attach").onclick=()=>document.querySelector("#file").click();
document.querySelector("#mic").onclick=()=>{
 if(!("webkitSpeechRecognition" in window||"SpeechRecognition" in window)){alert("Voice input is not supported in this browser.");return}
 const R=window.SpeechRecognition||window.webkitSpeechRecognition,r=new R();r.lang=navigator.language;r.onresult=e=>{input.value=e.results[0][0].transcript;sendMsg()};r.start();
};
render();
