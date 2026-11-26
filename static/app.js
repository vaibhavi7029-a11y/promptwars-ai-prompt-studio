const $ = id => document.getElementById(id);
let latestPrompt = "";
function requestBody(){return {prompt:$("prompt").value,goal:$("goal").value,audience:$("audience").value,tone:$("tone").value};}
function escapeHtml(s){return s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function renderAnalysis(a){
 $("score").innerHTML = `${a.score}<small>/100</small>`;
 $("meter-fill").style.width = `${a.score}%`;
 $("checks").innerHTML = Object.entries(a.checks).map(([name,ok])=>`<div class="check"><b>${ok?"✓":"○"}</b>${escapeHtml(name)}</div>`).join("");
 $("suggestions").innerHTML = a.suggestions.length ? a.suggestions.map(s=>`<li>${escapeHtml(s)}</li>`).join("") : "<li>Great structure. Keep testing and refining with real tasks.</li>";
}
async function post(path){
 const body=requestBody(); if(body.prompt.trim().length<8){$("status").textContent="Please enter a prompt with at least 8 characters.";return null;}
 $("status").textContent="Working…";
 try{const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});if(!r.ok)throw new Error("Request failed");const data=await r.json();$("status").textContent="Complete.";return data;}
 catch(e){$("status").textContent="Could not reach the server. Check your connection and try again.";return null;}
}
$("analyze").addEventListener("click",async()=>{const d=await post("/api/analyze");if(d)renderAnalysis(d);});
$("optimize").addEventListener("click",async()=>{const d=await post("/api/optimize");if(!d)return;renderAnalysis(d.analysis);latestPrompt=d.optimized_prompt;$("output").textContent=latestPrompt;$("mode").textContent=`Optimization mode: ${d.mode}`;$("copy").disabled=false;});
$("copy").addEventListener("click",async()=>{if(!latestPrompt)return;try{await navigator.clipboard.writeText(latestPrompt);$("status").textContent="Optimized prompt copied.";}catch(e){$("status").textContent="Clipboard unavailable in this browser.";}});