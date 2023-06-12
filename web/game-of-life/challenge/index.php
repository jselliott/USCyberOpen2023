<?php

class GOLSave
{
  public $hook;
  public $board;
  function __construct($boardData){
    $this->hook = "//todo - add php callback hooks";
    $this->board = $boardData;
  }
  function __wakeup(){
    if (isset($this->hook)) eval($this->hook);
  }
}

$loadedBoard = false;

if(isset($_POST)) {

    if(isset($_FILES['loadFile']))
    {
        $compressed = file_get_contents($_FILES['loadFile']['tmp_name']);
        $save = unserialize(gzuncompress($compressed));
        $loadedBoard = $save->board;
    }

    else if(isset($_POST["saveData"])){
        $board = json_decode(base64_decode($_POST["saveData"]));
        $save = new GOLSave($board);
        $export = gzcompress(serialize($save));
        header('Content-Type: application/octet-stream');
        header("Content-Transfer-Encoding: Binary"); 
        header("Content-disposition: attachment; filename=\"".uniqid().".golsave\"");
        echo($export);
        exit();
    }
} 

?><!DOCTYPE html>
<html>
<head>
    <title>USCG's Game of Life</title>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script type="text/javascript" src="/static/js/game.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css"/>
    <script type="text/javascript">
        var loadedBoard = <?
        echo $loadedBoard != false ? json_encode($loadedBoard) : "false";
        ?>; 
    </script>
</head>
<body>
    <div id="container">
        <p style="font-style:italic; font-size:0.8em; color:#333"><a href="https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life" target="_blank">The Game of Life</a>, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing machine.</p>
        <p style="font-style:italic; font-size:0.8em; color:#333">Instructions: Click on the cells below to mark live cells and then click Play to begin the simulation.</p>
        <div id="game_bar">
            <button id="play_button">Play</button>
            <button id="reset_button">Reset</button>
            <div style='font-size:0.8em; margin-left:10px; display:inline'>Live Cells: <span id="live_count">0</span></div>
            <form action="/" method="POST" id="saveForm" style="float:right">
            <input type="hidden" name="saveData" value=""/>
            <button id="save_button">Save</button>
            </form>
            <form action="/" method="POST" id="loadForm" style="float:right" enctype="multipart/form-data">
            <input type="file" id="loadFile" name="loadFile" style="display:none"/>
            <button id="load_button">Load</button>
            </form>
        </div>
        <hr>
        <canvas id="game_area" width='800' height='500'></canvas>
    </div>
</body>
</html>
