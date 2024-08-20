const express = require('express');
const pug = require('pug');

const app = express();
const port = 8000;

app.set('view engine', 'pug');
app.set('views', './views');

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/result', (req, res) => {
    // Get the username from the query string
    const username = req.query.username || 'Guest';

    // Vulnerable Implementation
    const templateString = `
doctype html
html(lang="en")
  head
    meta(charset="UTF-8")
    meta(name="viewport" content="width=device-width, initial-scale=1.0")
    title Result
    style.
      body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5dc; /* beige background */
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
      }
      .container {
        text-align: center;
        background-color: #fff;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
      }
      h1 {
        color: #d7263d; /* pink color */
      }
      p {
        font-size: 1.2em;
        # pink color
        color: #d7263d;
      }
      .button {
        background-color: #084c61; /* dark green color */
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        font-size: 1em;
      }
  body
    .container
      h1 Welcome ${username}!
      p Give me a username and I will say hello to you.
    `;

    // Render the template without compiling
    const output = pug.render(templateString);

    // Send the rendered HTML as the response
    res.send(output);
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
