<?php
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$uiDir = __DIR__ . '/ui';

if ($uri === '/' || $uri === '') {
    require $uiDir . '/index.php';
    return true;
}

$realPath = realpath($uiDir . $uri);
if ($realPath && str_starts_with($realPath, realpath($uiDir))) {
    $ext = pathinfo($realPath, PATHINFO_EXTENSION);
    $staticExts = ['css', 'js', 'png', 'jpg', 'jpeg', 'svg', 'gif', 'ico'];
    if (in_array($ext, $staticExts)) {
        $mime = ['css' => 'text/css', 'js' => 'application/javascript', 'png' => 'image/png', 'svg' => 'image/svg+xml', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg', 'gif' => 'image/gif', 'ico' => 'image/x-icon'];
        header('Content-Type: ' . ($mime[$ext] ?? 'application/octet-stream') . '; charset=utf-8');
        readfile($realPath);
        return true;
    }
    require $realPath;
    return true;
}

http_response_code(404);
echo '404 Not Found';
return true;
