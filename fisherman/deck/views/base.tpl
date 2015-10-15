<!DOCTYPE html>
<html>
  <head>
    <title>template page</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="static/css/main.css">
    <link rel="stylesheet" href="static/css/addon.css">
  </head>
  <body>
    <header id="header">
      <h1>Fisherman</h1>
    </header>
    <main id="main">
      <aside id="sidebar">
        <nav id="menu">
          <ul>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/topics">Topics</a></li>
            <li><a href="/users">Users</a></li>
            <li><a href="/weibos">Weibos</a></li>
          </ul>
        </nav>
      </aside>
      <div id="content">
        {{!base}}
      </div>
    </main>
    <script src="static/js/main.js"></script>
  </body>
</html>
