# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    overflow:hidden;
    font-family:Arial;
    background:#0b1020;
}

/* =========================================================
   ARCADE WINDOW (1/4 SCREEN + LANDSCAPE FIX)
========================================================= */

.game-wrapper{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);

    width:1100px;
    height:620px;

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
   MENU
========================================================= */

#menu{
    position:absolute;
    width:100%;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:rgba(0,0,0,0.7);
    z-index:10;
}

.box{
    width:420px;
    background:#111c33;
    padding:25px;
    border-radius:15px;
    color:white;
    text-align:center;
}

select,input{
    width:100%;
    padding:10px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    background:#24324d;
    color:white;
}

/* =========================================================
   END SCREEN
========================================================= */

#end{
    position:absolute;
    width:100%;
    height:100%;
    display:none;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    background:rgba(0,0,0,0.85);
    color:white;
    z-index:100;
}

#end h1{
    font-size:60px;
}

#end button{
    margin-top:20px;
    padding:12px;
    border:none;
    border-radius:10px;
    background:#2563eb;
    color:white;
    cursor:pointer;
}

</style>
</head>

<body>

<div id="menu">
    <div class="box">

        <h2>CHARACTER</h2>

        <input id="p1name" placeholder="P1 Name">
        <select id="p1color">
            <option value="red">Rot</option>
            <option value="blue">Blau</option>
            <option value="green">Grün</option>
            <option value="yellow">Gelb</option>
            <option value="pink">Pink</option>
        </select>

        <input id="p2name" placeholder="P2 Name">
        <select id="p2color">
            <option value="blue">Blau</option>
            <option value="red">Rot</option>
            <option value="green">Grün</option>
            <option value="yellow">Gelb</option>
            <option value="pink">Pink</option>
        </select>

        <button onclick="start()">START</button>

    </div>
</div>

<div id="end">
    <h1 id="winnerText">WINNER</h1>
    <div>🏆 CEREMONY 🏆</div>
    <button onclick="location.reload()">Zurück zum Menü</button>
</div>

<div class="game-wrapper">
<canvas id="c"></canvas>
</div>

<script>

const c=document.getElementById("c");
const ctx=c.getContext("2d");

c.width=1100;
c.height=620;

let game=false;
let winner=null;

const g=0.8;

/* ================= PLATFORMS (FIXED HEIGHT) ================= */

function plat(){
return[
{x:0,y:580,w:1100,h:40},
{x:150,y:450,w:300,h:25},
{x:700,y:450,w:300,h:25},
{x:420,y:320,w:260,h:25}
];
}

/* ================= PLAYER ================= */

class P{
constructor(x,y,color){
this.x=x;
this.y=y;
this.w=50;
this.h=80;
this.dx=0;
this.dy=0;
this.c=color;
this.score=0;
this.g=false;
}

draw(){

ctx.fillStyle=this.c;
ctx.fillRect(this.x,this.y,this.w,this.h);

// face
ctx.fillStyle="white";
ctx.fillRect(this.x+10,this.y+20,6,6);
ctx.fillRect(this.x+30,this.y+20,6,6);
}

upd(){

this.dy+=g;
this.x+=this.dx;
this.y+=this.dy;

this.g=false;

for(let p of plat()){

let hit=
this.x<p.x+p.w&&
this.x+this.w>p.x&&
this.y<p.y+p.h&&
this.y+this.h>p.y;

if(hit){

if(this.dy>0 && this.y+this.h-this.dy<=p.y){
this.y=p.y-this.h;
this.dy=0;
this.g=true;
}
}
}

if(this.x<0)this.x=0;
if(this.x>1050)this.x=1050;
}
}

/* ================= PLAYERS ================= */

const p1=new P(200,100,"red");
const p2=new P(800,100,"blue");

/* ================= INPUT ================= */

const k={};

window.addEventListener("keydown",e=>k[e.code]=true);
window.addEventListener("keyup",e=>k[e.code]=false);

/* ================= CONTROL ================= */

function ctrl(p,l,r,j){

p.dx=0;

if(k[l])p.dx=-6;
if(k[r])p.dx=6;

if(k[j]&&p.g)p.dy=-15;
}

/* ================= START ================= */

function start(){

p1.c=document.getElementById("p1color").value;
p2.c=document.getElementById("p2color").value;

document.getElementById("menu").style.display="none";

game=true;
}

/* ================= RESET ================= */

function reset(){
p1.x=200;p2.x=800;
p1.y=100;p2.y=100;
}

/* ================= COLLISION ================= */

function col(a,b){
return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
}

/* ================= END SCREEN ================= */

function endGame(w){

winner=w;

document.getElementById("end").style.display="flex";

document.getElementById("winnerText").innerText=w+" gewinnt!";
}

/* ================= LOOP ================= */

function loop(){

ctx.fillStyle="#0b1020";
ctx.fillRect(0,0,1100,620);

for(let p of plat()){
ctx.fillStyle="#334155";
ctx.fillRect(p.x,p.y,p.w,p.h);
}

if(game && !winner){

ctrl(p1,"KeyA","KeyD","KeyW");
ctrl(p2,"ArrowLeft","ArrowRight","ArrowUp");

p1.upd();
p2.upd();

if(col(p1,p2)){
if(p1.dy>0 && p1.y<p2.y){
p1.score++;
reset();
}
if(p2.dy>0 && p2.y<p1.y){
p2.score++;
reset();
}
}

if(p1.score>=5)endGame("P1");
if(p2.score>=5)endGame("P2");
}

p1.draw();
p2.draw();

requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=1000)
