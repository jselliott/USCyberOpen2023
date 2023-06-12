$(document).ready(function(){
    var canvas = document.getElementById("game_area");
    var ctx = canvas.getContext("2d");
    var cellSize = 10;
    var boardWidth = 800;
    var boardHeight = 500;
    var cellsX = boardWidth / cellSize;
    var cellsY = boardHeight / cellSize;
    var play = false;

    var board = Array.from(Array(cellsX), _ => Array(cellsY).fill(0));

    if(loadedBoard){
        board = loadedBoard;
    }
    
    function drawBoard(){

        var liveCells = 0;

        ctx.strokeStyle = "#555";

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        //Draw vertical lines
        for(i=cellSize; i<boardWidth; i+=cellSize){
            ctx.beginPath();
            ctx.moveTo(i,0);
            ctx.lineTo(i, boardHeight);
            ctx.stroke();
        }

        //Draw horizontal lines
        for(i=cellSize; i<boardHeight; i+=cellSize){
            ctx.beginPath();
            ctx.moveTo(0,i);
            ctx.lineTo(boardWidth,i);
            ctx.stroke();
        }

        //Fill cells
        for(x=0; x<cellsX; x++){
            for(y=0; y<cellsY; y++){
                if(board[x][y] == 1){
                    ctx.beginPath();
                    ctx.fillStyle = "yellow";
                    ctx.rect(x*cellSize,y*cellSize,cellSize,cellSize);
                    ctx.fill();
                    liveCells++;
                }
            }
        }

        $("#live_count").html(liveCells);
    }

    canvas.addEventListener('click', function(event) {
        if(play){
            return;
        }
        var rect = canvas.getBoundingClientRect();
        var x = event.clientX - rect.left,
            y = event.clientY - rect.top;

        
        for(i=0; i<cellsX; i++){
            for(j=0; j<cellsY; j++){
                cellx = i*cellSize;
                celly = j*cellSize;
                
                if (y > celly && y < celly + cellSize 
                    && x > cellx && x < cellx + cellSize) {
                    board[i][j] = !board[i][j];
                }
            }
        }
        drawBoard();
    }, false);

    function liveNeighbors(x,y){
        count = 0;
        vec = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]];
        for(i=0; i<vec.length; i++){
            x1 = x + vec[i][0];
            y1 = y + vec[i][1];
            if(x1 >= 0 && x1 < cellsX && y1 >= 0 && y1 <cellsY && board[x1][y1] == 1){
                count ++;
            }
        } 
        return count;
    }

    function gameTick() {
        if(!play){
            return;
        }
        newBoard = Array.from(Array(cellsX), _ => Array(cellsY).fill(0));
        for(x=0; x<40; x++){
            for(y=0; y<25; y++){
                ln = liveNeighbors(x,y);
                if(board[x][y] && (ln == 2 || ln == 3)){ newBoard[x][y] = 1;}
                else if(!board[x][y] && ln == 3){ newBoard[x][y] = 1;}
            }
        }
        board = newBoard;
        drawBoard();
    }

    $("#play_button").click(function(e){
        e.preventDefault();
        if(play){
            play = false;
            $("#play_button").html("Play");
            $("#save_button").removeAttr("disabled");
            $("#load_button").removeAttr("disabled");
        } else {
            play = true;
            $("#play_button").html("Stop");
            $("#save_button").attr("disabled","disabled");
            $("#load_button").attr("disabled","disabled");
        }
        return false;
    });

    $("#reset_button").click(function(e){
        e.preventDefault();
        board = Array.from(Array(cellsX), _ => Array(cellsY).fill(0));
        play = false;
        $("#play_button").html("Play");
        $("#save_button").removeAttr("disabled");
        $("#load_button").removeAttr("disabled");
        drawBoard();
        return false;
    });

    $("#save_button").click(function(e){
        e.preventDefault();
        $("input[name='saveData']").val(btoa(JSON.stringify(board)));
        $("#saveForm").submit();
    });

    $("#load_button").click(function(e){
        e.preventDefault();
        $("input[name='loadFile']").click();
    });

    $("input[name='loadFile']").change(function(){
        $("#loadForm").submit();
    });


    drawBoard();

    setInterval(gameTick,500);
});