import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
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
    background:#050814;
    overflow:hidden;
    font-family:Arial;
}

/* =========================================================
   GAME WINDOW (RECTANGLE)
========================================================= */

.game-container{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);

    width:1200px;
    height:650px;

    border-radius:16px;
    overflow:hidden;

    border:2px solid rgba(255,255,255,0.08);
}

canvas{
    width:100%;
    height:100%;
}

/* =========================================================
   CHARACTER EDITOR (IMPORTANT NEW SYSTEM)
========================================================= */

#editor{
    position:absolute;
    width:100%;
    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    background:radial-gradient(circle,#0b1225,#050814);

    z-index:100;
}

.panel{
    width:500px;
    background:#111c33;
    padding:25px;
    border-radius:18px;
    color:white;
}

.panel h1{
    margin-bottom:10px;
}

.row{
    margin-top:10px;
}

select,input{
    width:100%;
    padding:10px;
    margin-top:5px;
    border-radius:10px;
    border:none;
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
    padding:0 30px;
    color:white;
    font-weight:bold;
    z-index:5;
}

/* =========================================================
   SCORE ANIMATION
========================================================= */

#scoreAnim{
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

.pauseBox{
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

<div id="editor">

    <div class="panel">

        <h1>CHARACTER EDIT</h1>

        <div class="row">Name P1</div>
        <input id="p1name">

        <div class="row">Color</div>
        <select id="p1color">
            <option value="#ef4444">Red</option>
            <option value="#3b82f6">Blue</option>
            <option value="#22c55e">Green</option>
        </select>

        <div class="row">Hat</div>
        <select id="p1hat">
            <option value="none">None</option>
            <option value="hat">Hat</option>
            <option value="cap">Cap</option>
        </select>

        <div class="row">Glasses</div>
        <select id="p1glass">
            <option value="none">None</option>
            <option value="sunglasses">Sunglasses</option>
        </select>

        <hr style="margin:10px 0">

        <div class="row">Name P2</div>
        <input id="p2name">

        <div class="row">Color</div>
        <select id="p2color">
            <option value="#3b82f6">Blue</option>
            <option value="#ef4444">Red</option>
            <option value="#22c55e">Green</option>
        </select>

        <div class="row">Hat</div>
        <select id="p2hat">
            <option value="none">None</option>
            <option value="hat">Hat</option>
            <option value="cap">Cap</option>
        </select>

        <div class="row">Glasses</div>
        <select id="p2glass">
            <option value="none">None</option>
            <option value="sunglasses">Sunglasses</option>
        </select>

        <button onclick="startGame()" style="margin-top:15px;width:100%;padding:12px;background:#2563eb;color:white;border:none;border-radius:10px;">
        START
        </button>

    </div>

</div>

<!-- =======================================================
   HUD + SCORE
======================================================= -->

<div id="hud"></div>
<div id="scoreAnim"></div>

<!-- =======================================================
   PAUSE
======================================================= -->

<div id="pause">
    <div class="pauseBox">
        PAUSED
        <br><br>
        <button onclick="resume()">Resume</button>
        <button onclick="location.reload()">Menu</button>
    </div>
</div>

<!-- =======================================================
   GAME
======================================================= -->

<div class="game-container">
<canvas id="c"></canvas>
</div>

<script>

/* ================= CANVAS ================= */

const c=document.getElementById("c");
const ctx=c.getContext("2d");

c.width=1200;
c.height=650;

/* ================= STATE ================= */

let game=false;
let pause=false;
let winner=null;

/* ================= SCORE SYSTEM ================= */

function showScore(text){
    const s=document.getElementById("scoreAnim");
    s.innerText=text;
    s.style.display="block";

    setTimeout(()=>{
        s.style.display="none";
    },2500);
}

/* ================= PLATFORMS ================= */

function platforms(){
return[
{ x:0,y:600,w:1200,h:50},
{ x:150,y:450,w:300,h:20},
{ x:750,y:450,w:300,h:20},
{ x:450,y:320,w:300,h:20},
];
}

/* ================= PLAYER ================= */

class Player{
constructor(x,y,color){
this.x=x;
this.y=y;
this.w=50;
this.h=80;
this.dx=0;
this.dy=0;
this.color=color;
this.score=0;
this.onGround=false;
}

draw(){
ctx.fillStyle=this.color;
ctx.fillRect(this.x,this.y,this.w,this.h);

// face
ctx.fillStyle="white";
ctx.fillRect(this.x+10,this.y+20,8,8);
ctx.fillRect(this.x+30,this.y+20,8,8);
}

update(){

this.dy+=0.8;
this.x+=this.dx;
this.y+=this.dy;

this.onGround=false;

for(let p of platforms()){
if(this.x<p.x+p.w&&this.x+this.w>p.x&&this.y<p.y+p.h&&this.y+this.h>p.y){

if(this.dy>0){
this.y=p.y-this.h;
this.dy=0;
this.onGround=true;
}
}
}

if(this.x<0)this.x=0;
if(this.x>1150)this.x=1150;
}
}

/* ================= PLAYERS ================= */

const p1=new Player(200,100,"red");
const p2=new Player(800,100,"blue");

/* ================= INPUT ================= */

const keys={};

window.addEventListener("keydown",e=>{
keys[e.code]=true;
if(e.code==="Escape")pause=!pause;
});

window.addEventListener("keyup",e=>{
keys[e.code]=false;
});

/* ================= CONTROL ================= */

function control(p,l,r,j){

p.dx=0;

if(keys[l])p.dx=-6;
if(keys[r])p.dx=6;

if(keys[j]&&p.onGround){
p.dy=-14;
}
}

/* ================= START ================= */

function startGame(){

p1.color=document.getElementById("p1color").value;
p2.color=document.getElementById("p2color").value;

document.getElementById("editor").style.display="none";

game=true;
}

/* ================= LOOP ================= */

function loop(){

ctx.fillStyle="#050814";
ctx.fillRect(0,0,1200,650);

for(let p of platforms()){
ctx.fillStyle="#334155";
ctx.fillRect(p.x,p.y,p.w,p.h);
}

if(game && !pause && !winner){

control(p1,"KeyA","KeyD","KeyW");
control(p2,"ArrowLeft","ArrowRight","ArrowUp");

p1.update();
p2.update();

if(p1.x<p2.x+50&&p1.x+50>p2.x&&p1.y<p2.y+80&&p1.y+80>p2.y){

if(p1.dy>0){
p1.score++;
showScore(p1.score);
p1.x=200;p2.x=800;
p1.y=100;p2.y=100;
}

if(p2.dy>0){
p2.score++;
showScore(p2.score);
p1.x=200;p2.x=800;
p1.y=100;p2.y=100;
}
}

if(p1.score>=5)winner="P1";
if(p2.score>=5)winner="P2";
}

p1.draw();
p2.draw();

document.getElementById("hud").innerHTML=
"Player1: "+p1.score+" | Player2: "+p2.score;

if(winner){
ctx.fillStyle="white";
ctx.font="60px Arial";
ctx.fillText(winner+" WINS!",400,300);
}

requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=900)
