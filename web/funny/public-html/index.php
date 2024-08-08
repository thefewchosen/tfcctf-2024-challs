<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hacker Files</title>
  </head>
  <body>
    <div class="main">
      <h1>We paid for a pixel art AI, it would be a shame not to use it.</h1>
      <img src="hacker.png" />
      <button onclick="window.location.href='?new_joke'">Generate Joke</button>
      <?php 
      
        $jokes = ["Why did the hacker go broke? He used up all his cache.", "Why was the JavaScript reality show cancelled after one episode? People thought it was too scripted.", "Why do programmers prefer dark mode? Light attracts bugs."];

        if (isset($_GET['new_joke'])) {
          echo $jokes[array_rand($jokes)];
        }

      ?>
    </div>
    <style>
        .main {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 2rem;
        }

        button {
            padding: .5rem 2rem;
            border: none;
            cursor: pointer;
            background: #d70ed1;
            border-radius: 5px;
            color: white;
        }

        button:hover {
            background: #b30aad;
        }

        h1 {
            font-family: sans-serif;
        }
    </style>
  </body>
</html>