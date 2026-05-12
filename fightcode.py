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
    GLOBAL
========================================================= */

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    overflow:hidden;
    font-family:Arial;
    background:#050814;
}

/* =========================================================
    GAME WINDOW (ONLY 1/4 SCREEN EFFECT)
========================================================= */

.game-wrapper{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);

    width:1100px;
    height:650px;

    border-radius:18px;

    overflow:hidden;

    border:2px solid rgba(255,255,255,0.08);
}

/* =========================================================
    CANVAS
========================================================= */

canvas{
    width:100%;
    height:100%;
    display:block;
}

/* =========================================================
    MENU SYSTEM
========================================================= */

.menu{
    position:absolute;
    width:100%;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;

    background:radial-gradient(circle,#0b1225,#050814);
    z-index:100;
}

.box{
    width:420px;
    background:#111c33;
    padding:30px;
    border-radius:18px;
    color:white;
    text-align:center;
}

.box h1{
    font-size:46px;
    margin-bottom:10px;
}

.box input, select{
    width:100%;
    padding:12px;
    margin-top:10px;
    border-radius:10px;
    border:none;
    background:#24324d;
    color:white;
}

.box button{
    width:100%;
    margin-top:18px;
    padding:14px;
    border:none;
    border-radius:12px;
    font-weight:bold;
    background:linear-gradient(to right,#2563eb,#38bdf8);
    color:white;
    cursor:pointer;
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
    z-index:10;
}

/* =========================================================
    POPUP
========================================================= */

#popup{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    color:white;
    font-size:50px;
    display:none;
    z-index:200;
}

/* =========================================================
    PAUSE MENU
========================================================= */

#pauseMenu{
    position:absolute;
    width:100%;
    height:100%;
    display:none;

    justify-content:center;
    align-items:center;

    background:rgba(0,0,0,0.7);
    z-index:150;
}

.pauseBox{
    background:#1e293b;
    padding:30px;
    border-radius:15px;
    color:white;
    text-align:center;
}

.pauseBox button{
    width:100%;
    margin-top:10px;
    padding:12px;
}

/* =========================================================
    CHARACTER PREVIEW
========================================================= */

.char{
    width:40px;
    height:60px;
    display:inline-block;
    margin:5px;
}

/* =========================================================
    BACKGROUND DECOR
========================================================= */

</style>

</head>

<body>

<!-- =======================================================
    MENU
======================================================= -->

<div class="menu" id="menu">

    <div class="box">

        <h1>⚔ Jump Battle</h1>

        <input id="p1name" placeholder="Spieler 1 Name">
        <input id="p2name" placeholder="Spieler 2 Name">

        <select id="p1color">
            <option value="#ef4444">Rot</option>
            <option value="#22c55e">Grün</option>
            <option value="#3b82f6">Blau</option>
        </select>

        <select id="p2color">
            <option value="#3b82f6">Blau</option>
            <option value="#ef4444">Rot</option>
            <option value="#22c55e">Grün</option>
        </select>

        <button onclick="startGame()">START GAME</button>

    </div>

</div>

<!-- =======================================================
    PAUSE MENU
======================================================= -->

<div id="pauseMenu">

    <div class="pauseBox">

        <h2>PAUSE</h2>

        <button onclick="resume()">Weiter</button>
        <button onclick="backToMenu()">Menü</button>

    </div>

</div>

<!-- =======================================================
    POPUP + HUD
======================================================= -->

<div id="popup"></div>
<div id="hud"></div>

<!-- =======================================================
    GAME WRAPPER (SMALL VIEW)
======================================================= -->

<div class="game-wrapper">

    <canvas id="game"></canvas>

</div>

<script>

/* =========================================================
    CANVAS
========================================================= */

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

function resize(){
    canvas.width=1100;
    canvas.height=650;
}
resize();

/* =========================================================
    STATE
========================================================= */

let gameStarted=false;
let paused=false;
let winner=null;

/* =========================================================
    BACKGROUND
========================================================= */

const stars=[];

for(let i=0;i<200;i++){
    stars.push({
        x:Math.random()*1100,
        y:Math.random()*650,
        r:Math.random()*2
    });
}

/* =========================================================
    BOOST + COINS
========================================================= */

let boost={p1:0,p2:0};
let coins=[];

setInterval(()=>{
    if(gameStarted && !winner){
        if(Math.random()<0.5){
            coins.push({
                x:Math.random()*1000,
                y:Math.random()*300
            });
        }
    }
},4000);

/* =========================================================
    PLATFORM FIXED
========================================================= */

function platforms(){
    return[
        {x:0,y:600,w:1100,h:50},
        {x:150,y:470,w:300,h:20},
        {x:650,y:470,w:300,h:20},
        {x:400,y:340,w:300,h:20},
        {x:200,y:210,w:250,h:20},
        {x:650,y:210,w:250,h:20}
    ];
}

/* =========================================================
    PLAYER
========================================================= */

class Player{
    constructor(x,y,color,controls){
        this.x=x;
        this.y=y;
        this.w=50;
        this.h=80;
        this.color=color;
        this.dx=0;
        this.dy=0;
        this.score=0;
        this.controls=controls;
        this.onGround=false;
        this.name="";
    }

    draw(){
        ctx.fillStyle=this.color;
        ctx.fillRect(this.x,this.y,this.w,this.h);

        ctx.fillStyle="#f1c27d";
        ctx.beginPath();
        ctx.arc(this.x+25,this.y-10,10,0,Math.PI*2);
        ctx.fill();
    }

    update(){

        this.dy+=0.8;

        this.x+=this.dx;
        this.y+=this.dy;

        this.onGround=false;

        for(let p of platforms()){

            let hit=
                this.x<p.x+p.w&&
                this.x+this.w>p.x&&
                this.y<p.y+p.h&&
                this.y+this.h>p.y;

            if(hit){

                if(this.dy>0 && this.y+this.h-this.dy<=p.y){
                    this.y=p.y-this.h;
                    this.dy=0;
                    this.onGround=true;
                }
            }
        }

        if(this.x<0)this.x=0;
        if(this.x+this.w>1100)this.x=1100-this.w;
    }
}

/* =========================================================
    PLAYERS
========================================================= */

const p1=new Player(200,100,"#ef4444",{l:"KeyA",r:"KeyD",j:"KeyW"});
const p2=new Player(800,100,"#3b82f6",{l:"ArrowLeft",r:"ArrowRight",j:"ArrowUp"});

p1.id="p1";
p2.id="p2";

/* =========================================================
    INPUT
========================================================= */

const keys={};

window.addEventListener("keydown",e=>{
    keys[e.code]=true;

    if(e.code==="Escape"){
        togglePause();
    }
});

window.addEventListener("keyup",e=>{
    keys[e.code]=false;
});

/* =========================================================
    CONTROLS
========================================================= */

function controls(p){

    p.dx=0;

    let sp=(boost[p.id]>0)?11:7;

    if(keys[p.controls.l])p.dx=-sp;
    if(keys[p.controls.r])p.dx=sp;

    if(keys[p.controls.j] && p.onGround){
        p.dy=-15;
    }
}

/* =========================================================
    MENU START
========================================================= */

function startGame(){

    p1.name=document.getElementById("p1name").value||"P1";
    p2.name=document.getElementById("p2name").value||"P2";

    p1.color=document.getElementById("p1color").value;
    p2.color=document.getElementById("p2color").value;

    document.getElementById("menu").style.display="none";

    gameStarted=true;
}

/* =========================================================
    PAUSE
========================================================= */

function togglePause(){
    if(!gameStarted)return;

    paused=!paused;

    document.getElementById("pauseMenu").style.display=
        paused?"flex":"none";
}

function resume(){
    paused=false;
    document.getElementById("pauseMenu").style.display="none";
}

function backToMenu(){
    location.reload();
}

/* =========================================================
    COLLISION
========================================================= */

function collide(a,b){
    return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
}

/* =========================================================
    LOOP
========================================================= */

function loop(){

    ctx.fillStyle="#050814";
    ctx.fillRect(0,0,1100,650);

    // stars
    ctx.fillStyle="white";
    for(let s of stars){
        ctx.beginPath();
        ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
        ctx.fill();
    }

    // moon
    ctx.fillStyle="white";
    ctx.beginPath();
    ctx.arc(950,100,50,0,Math.PI*2);
    ctx.fill();

    if(gameStarted && !paused && !winner){

        controls(p1);
        controls(p2);

        p1.update();
        p2.update();

        if(collide(p1,p2)){
            if(p1.dy>0 && p1.y<p2.y){
                p1.score++;
            }
            if(p2.dy>0 && p2.y<p1.y){
                p2.score++;
            }
        }

        if(p1.score>=3)winner=p1.name;
        if(p2.score>=3)winner=p2.name;
    }

    for(let p of platforms()){
        ctx.fillStyle="#334155";
        ctx.fillRect(p.x,p.y,p.w,p.h);
    }

    p1.draw();
    p2.draw();

    document.getElementById("hud").innerHTML=
        p1.name+" "+p1.score+" | "+p2.name+" "+p2.score;

    if(winner){
        ctx.fillStyle="white";
        ctx.font="50px Arial";
        ctx.fillText(winner+" gewinnt!",350,300);
    }

    requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=900)
