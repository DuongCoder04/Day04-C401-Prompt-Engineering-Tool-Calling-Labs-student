<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Only POST allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$message = trim($input['message'] ?? '');

if (!$message) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing message']);
    exit;
}

$bridge = __DIR__ . '/bridge.py';
$projRoot = getenv('PROJECT_ROOT');
if (!$projRoot) {
    $projRoot = dirname(__DIR__);
}

$pyPath = $projRoot . '/.venv/Scripts/python.exe';

$env = ['PYTHONIOENCODING' => 'utf-8', 'PROJECT_ROOT' => $projRoot] + getenv();
$descriptorspec = [['pipe', 'r'], ['pipe', 'w'], ['pipe', 'w']];
$cmdArgs = [$pyPath, $bridge, '--message', $message];

$process = @proc_open($cmdArgs, $descriptorspec, $pipes, null, $env);

if (!is_resource($process)) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to start Python process']);
    exit;
}

fclose($pipes[0]);
$stdout = stream_get_contents($pipes[1]);
$stderr = stream_get_contents($pipes[2]);
fclose($pipes[1]);
fclose($pipes[2]);
$exitCode = proc_close($process);

if ($exitCode !== 0 || !$stdout) {
    $result = json_decode($stdout, true);
    if ($result) {
        echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        exit;
    }
    http_response_code(500);
    echo json_encode([
        'error' => 'Python bridge failed',
        'exit_code' => $exitCode,
        'stderr' => $stderr,
        'stdout' => $stdout,
    ]);
    exit;
}

$result = json_decode($stdout, true);

if ($result === null) {
    http_response_code(500);
    echo json_encode([
        'error' => 'Invalid JSON from Python bridge',
        'stdout' => $stdout,
    ]);
    exit;
}

echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
