import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

/* =========================================================
   BASE
========================================================= */

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    overflow:hidden;
    background:#050814;
    font-family:Arial;
}

/* =========================================================
   GAME FRAME (RECTANGLE ARCADE STYLE)
========================================================= */

.frame{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);

    width:1200px;
    height:650px;

    border-radius:18px;
    overflow:hidden;

    border:2px solid rgba(255,255,255,0.08);
}

canvas{
    width:100%;
    height:100%;
    display:block;
}

/* =========================================================
   SCREENS SYSTEM
========================================================= */

.screen{
    position:absolute;
    width:100%;
    height:100vh;
}

/* ================= EDITOR ================= */

#editor{
    display:flex;
    justify-content:center;
    align-items:center;
    background:radial-gradient(circle,#0b1225,#050814);
    z-index:100;
}

.panel{
    width:520px;
    background:#111c33;
    padding:25px;
    border-radius:16px;
    color:white;
}

.panel h1{
    text-align:center;
    margin-bottom:10px;
}

.panel input, .panel select{
    width:100%;
    padding:10px;
    margin-top:8px;
    border:none;
    border-radius:8px;
    background:#24324d;
    color:white;
}

/* =========================================================
   HUD
========================================================= */

#hud{
    position:absolute;
    top:10px;
    width:100%;
    display:flex;
    justify-content:space-between;
    padding:0 25px;
    color:white;
    font-weight:bold;
    z-index:10;
}

/* =========================================================
   SCORE ANIMATION
========================================================= */

#anim{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:80px;
    color:white;
    display:none;
    z-index:200;
}

/* =========================================================
   PAUSE
========================================================= */

#pause{
    position:absolute;
    width:100%;
    height:100%;
    display:none;
    justify-content:center;
    align-items:center;
    background:rgba(0,0,0,0.6);
    z-index:150;
}

.box{
    background:#1e293b;
    padding:20px;
    color:white;
    border-radius:10px;
}

</style>

</head>

<body>

<!-- =======================================================
   CHARACTER EDITOR
======================================================= -->

<div id="editor" class="screen">

<div class="panel">

<h1>CHARACTER CREATOR</h1>

<h3>P1</h3>
<input id="p1name" placeholder="Name">
<select id="p1color">
<option value="red">Red</option>
<option value="blue">Blue</option>
<option value="green">Green</option>
</select>

<select id="p1hat">
<option value="none">No Hat</option>
<option value="hat">Hat</option>
<option value="cap">Cap</option>
</select>

<select id="p1glass">
<option value="none">No Glasses</option>
<option value="sun">Sunglasses</option>
</select>

<hr>

<h3>P2</h3>
<input id="p2name" placeholder="Name">
<select id="p2color">
<option value="blue">Blue</option>
<option value="red">Red</option>
<option value="green">Green</option>
</select>

<select id="p2hat">
<option value="none">No Hat</option>
<option value="hat">Hat</option>
<option value="cap">Cap</option>
</select>

<select id="p2glass">
<option value="none">No Glasses</option>
<option value="sun">Sunglasses</option>
</select>

<button onclick="start()" style="margin-top:15px;width:100%;padding:12px;background:#2563eb;color:white;border:none;border-radius:8px;">
START GAME
</button>

</div>

</div>

<!-- =======================================================
   HUD + ANIMATION + PAUSE
======================================================= -->

<div id="hud"></div>
<div id="anim"></div>

<div id="pause">
<div class="box">
PAUSE
<br><br>
<button onclick="resume()">Resume</button>
<button onclick="location.reload()">Exit</button>
</div>
</div>

<!-- =======================================================
   GAME FRAME
======================================================= -->

<div class="frame">
<canvas id="c"></canvas>
</div>

<script>

/* =========================================================
   SETUP
========================================================= */

const c=document.getElementById("c");
const ctx=c.getContext("2d");

c.width=1200;
c.height=650;

/* =========================================================
   STATE
========================================================= */

let game=false;
let pause=false;
let winner=null;

/* =========================================================
   ANIMATION
========================================================= */

function anim(text){
const a=document.getElementById("anim");
a.innerText=text;
a.style.display="block";
setTimeout(()=>a.style.display="none",2500);
}

/* =========================================================
   PLATFORM
========================================================= */

function plat(){
return[
{x:0,y:600,w:1200,h:50},
{x:200,y:450,w:300,h:20},
{x:700,y:450,w:300,h:20},
{x:450,y:320,w:300,h:20}
];
}

/* =========================================================
   PLAYER
========================================================= */

class P{
constructor(x,y,c){
this.x=x;
this.y=y;
this.w=50;
this.h=80;
this.dx=0;
this.dy=0;
this.c=c;
this.s=0;
this.g=false;
}

draw(){

ctx.fillStyle=this.c;
ctx.fillRect(this.x,this.y,this.w,this.h);

// face
ctx.fillStyle="white";
ctx.fillRect(this.x+10,this.y+20,6,6);
ctx.fillRect(this.x+30,this.y+20,6,6);

ctx.fillRect(this.x+20,this.y+35,8,3);
}

upd(){

this.dy+=0.8;
this.x+=this.dx;
this.y+=this.dy;

this.g=false;

for(let p of plat()){
if(this.x<p.x+p.w&&this.x+this.w>p.x&&this.y<p.y+p.h&&this.y+this.h>p.y){
if(this.dy>0){
this.y=p.y-this.h;
this.dy=0;
this.g=true;
}
}
}

if(this.x<0)this.x=0;
if(this.x>1150)this.x=1150;
}
}

/* =========================================================
   PLAYERS
========================================================= */

const p1=new P(200,100,"red");
const p2=new P(800,100,"blue");

/* =========================================================
   INPUT
========================================================= */

const k={};

window.addEventListener("keydown",e=>{
k[e.code]=true;
if(e.code==="Escape")pause=!pause;
});
window.addEventListener("keyup",e=>k[e.code]=false);

/* =========================================================
   CONTROL
========================================================= */

function ctrl(p,l,r,j){

p.dx=0;

if(k[l])p.dx=-6;
if(k[r])p.dx=6;

if(k[j]&&p.g)p.dy=-14;
}

/* =========================================================
   START
========================================================= */

function start(){

p1.c=document.getElementById("p1color").value;
p2.c=document.getElementById("p2color").value;

document.getElementById("editor").style.display="none";

game=true;
}

/* =========================================================
   RESET
========================================================= */

function reset(){
p1.x=200;p2.x=800;
p1.y=100;p2.y=100;
}

/* =========================================================
   LOOP
========================================================= */

function loop(){

ctx.fillStyle="#050814";
ctx.fillRect(0,0,1200,650);

for(let p of plat()){
ctx.fillStyle="#334155";
ctx.fillRect(p.x,p.y,p.w,p.h);
}

if(game && !pause && !winner){

ctrl(p1,"KeyA","KeyD","KeyW");
ctrl(p2,"ArrowLeft","ArrowRight","ArrowUp");

p1.upd();
p2.upd();

if(p1.x<p2.x+50&&p1.x+50>p2.x&&p1.y<p2.y+80&&p1.y+80>p2.y){

if(p1.dy>0){
p1.s++;
anim(p1.s);
reset();
}

if(p2.dy>0){
p2.s++;
anim(p2.s);
reset();
}
}

if(p1.s>=5)winner="P1";
if(p2.s>=5)winner="P2";
}

p1.draw();
p2.draw();

document.getElementById("hud").innerHTML=
"P1: "+p1.s+" | P2: "+p2.s;

if(winner){
ctx.fillStyle="white";
ctx.font="50px Arial";
ctx.fillText(winner+" WIN!",450,300);
}

requestAnimationFrame(loop);
}

loop();

function resume(){
pause=false;
document.getElementById("pause").style.display="none";
}

</script>

</body>
</html>
"""

components.html(html, height=900)
