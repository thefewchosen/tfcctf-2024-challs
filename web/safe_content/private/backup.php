<?php

function isAllowedIP($url, $allowedHost) {
    $parsedUrl = parse_url($url);
    
    if (!$parsedUrl || !isset($parsedUrl['host'])) {
        return false;
    }
    
    return $parsedUrl['host'] === $allowedHost;
}

function fetchContent($url) {
    $context = stream_context_create([
        'http' => [
            'timeout' => 5 // Timeout in seconds
        ]
    ]);

    $content = @file_get_contents($url, false, $context);
    if ($content === FALSE) {
        $error = error_get_last();
        throw new Exception("Unable to fetch content from the URL. Error: " . $error['message']);
    }
    return base64_decode($content);
}

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['url'])) {
    $url = $_GET['url'];
    $allowedIP = 'localhost';
    
        if (isAllowedIP($url, $allowedIP)) {
            $content = fetchContent($url);
            // file upload removed due to security issues
            if ($content) {
                $command = 'echo ' . $content . ' | base64 > /tmp/' . date('YmdHis') . '.tfc';
                exec($command . ' > /dev/null 2>&1');
                // this should fix it
        }
    }

}
else {
    highlight_file(__FILE__);
    exit;
    }
?>
