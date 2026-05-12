# app.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">

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

canvas{
    display:block;
    width:100vw;
    height:100vh;
}

/* MENU */

#menu{
    position:absolute;
    width:100%;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:rgba(0,0,0,0.75);
    z-index:10;
}

.menu-box{
    width:min(520px,90vw);
    background:#1e293b;
    padding:40px;
    border-radius:25px;
    text-align:center;
    color:white;
}

.menu-box h1{
    font-size:52px;
    margin-bottom:10px;
}

.menu-box input{
    width:100%;
    padding:14px;
    margin-top:12px;
    border-radius:12px;
    border:none;
    background:#334155;
    color:white;
    font-size:18px;
}

.menu-box button{
    width:100%;
    margin-top:20px;
    padding:16px;
    border:none;
    border-radius:14px;
    font-size:20px;
    font-weight:bold;
    color:white;
    background:linear-gradient(to right,#2563eb,#38bdf8);
}

/* POPUP */

#popup{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:60px;
    color:white;
    display:none;
    z-index:20;
    font-weight:bold;
}

/* COIN */

.coin{
    position:absolute;
    width:20px;
    height:20px;
    border-radius:50%;
    background:gold;
}

</style>
</head>

<body>

<div id="menu">
    <div class="menu-box">
        <h1>Jump Battle</h1>

        <input id="p1name" placeholder="Spieler 1">
        <input id="p2name" placeholder="Spieler 2">

        <button onclick="startGame()">Start</button>
    </div>
</div>

<div id="popup"></div>

<canvas id="game"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resize(){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize",resize);

const gravity = 0.8;

let gameStarted=false;
let winner=null;

let coins=[];
let boost = {p1:0,p2:0};

function spawnCoin(){
    coins.push({
        x:Math.random()*canvas.width,
        y:Math.random()*canvas.height/2
    });
}

setInterval(()=>{
    if(gameStarted && !winner){
        if(Math.random()<0.6){
            spawnCoin();
        }
    }
},3000);

function showPopup(text){
    const p=document.getElementById("popup");
    p.innerText=text;
    p.style.display="block";
    setTimeout(()=>p.style.display="none",2000);
}

/* PLATFORMS */

function platforms(){
    return [
        {x:0,y:canvas.height-50,w:canvas.width,h:50},

        {x:150,y:canvas.height-220,w:300,h:20},
        {x:canvas.width-450,y:canvas.height-220,w:300,h:20},

        {x:canvas.width/2-150,y:canvas.height-380,w:300,h:20},

        {x:120,y:canvas.height-540,w:260,h:20},
        {x:canvas.width-380,y:canvas.height-540,w:260,h:20}
    ];
}

/* PLAYER */

class Player{
    constructor(x,y,color,controls){
        this.x=x;
        this.y=y;
        this.w=60;
        this.h=90;
        this.color=color;
        this.dx=0;
        this.dy=0;
        this.score=0;
        this.controls=controls;
        this.onGround=false;
        this.name="";
    }

    speed(){
        return (boost[this.id]>0)?12:7;
    }

    draw(){
        ctx.fillStyle=this.color;
        ctx.fillRect(this.x,this.y,this.w,this.h);
    }

    update(){
        this.dy+=gravity;
        this.x+=this.dx;
        this.y+=this.dy;

        this.onGround=false;

        for(let p of platforms()){
            const hit =
                this.x<p.x+p.w &&
                this.x+this.w>p.x &&
                this.y<p.y+p.h &&
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
        if(this.x+this.w>canvas.width)this.x=canvas.width-this.w;
    }
}

/* INPUT */

const keys={};

window.addEventListener("keydown",e=>keys[e.code]=true);
window.addEventListener("keyup",e=>keys[e.code]=false);

/* PLAYERS */

const p1=new Player(200,100,"#ef4444",{l:"KeyA",r:"KeyD",j:"KeyW"});
const p2=new Player(700,100,"#3b82f6",{l:"ArrowLeft",r:"ArrowRight",j:"ArrowUp"});

p1.id="p1";
p2.id="p2";

/* CONTROLS */

function controls(p){
    p.dx=0;

    let sp=(boost[p.id]>0)?11:7;

    if(keys[p.controls.l])p.dx=-sp;
    if(keys[p.controls.r])p.dx=sp;

    if(keys[p.controls.j] && p.onGround){
        p.dy=-16;
    }
}

/* GAME */

function startGame(){
    p1.name=document.getElementById("p1name").value||"P1";
    p2.name=document.getElementById("p2name").value||"P2";
    document.getElementById("menu").style.display="none";
    gameStarted=true;
}

function reset(){
    p1.x=200;p1.y=100;p1.dy=0;
    p2.x=700;p2.y=100;p2.dy=0;
}

function collide(a,b){
    return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
}

/* COINS */

function drawCoins(){
    ctx.fillStyle="gold";
    for(let c of coins){
        ctx.beginPath();
        ctx.arc(c.x,c.y,8,0,Math.PI*2);
        ctx.fill();
    }
}

function checkCoins(p){
    coins=coins.filter(c=>{
        let hit=
            p.x<c.x+10&&p.x+p.w>c.x&&
            p.y<c.y+10&&p.y+p.h>c.y;

        if(hit){
            boost[p.id]=8*60;
            showPopup(p.name+" SPEED BOOST!");
            return false;
        }
        return true;
    });
}

/* LOOP */

function loop(){
    ctx.clearRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle="#0b1020";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    if(gameStarted&&!winner){

        controls(p1);
        controls(p2);

        p1.update();
        p2.update();

        checkCoins(p1);
        checkCoins(p2);

        if(boost.p1>0)boost.p1--;
        if(boost.p2>0)boost.p2--;

        if(collide(p1,p2)){
            if(p1.dy>0&&p1.y<p2.y){
                p1.score++;
                showPopup(p1.name+" +1");
                reset();
            }
            if(p2.dy>0&&p2.y<p1.y){
                p2.score++;
                showPopup(p2.name+" +1");
                reset();
            }
        }

        if(p1.score>=3)winner=p1.name;
        if(p2.score>=3)winner=p2.name;
    }

    for(let p of platforms()){
        ctx.fillStyle="#334155";
        ctx.fillRect(p.x,p.y,p.w,p.h);
    }

    drawCoins();

    p1.draw();
    p2.draw();

    ctx.fillStyle="white";
    ctx.font="24px Arial";
    ctx.fillText(p1.name+": "+p1.score,30,40);
    ctx.fillText(p2.name+": "+p2.score,canvas.width-180,40);

    if(winner){
        ctx.font="60px Arial";
        ctx.fillText(winner+" gewinnt!",canvas.width/2-200,canvas.height/2);
    }

    requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=1200)
