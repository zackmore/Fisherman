<!DOCTYPE html>
<html>
  <head>
    <title>template page</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/main.css">
    <link rel="stylesheet" href="/static/css/addon.css">
  </head>
  <body>
    <header id="header">
      <h1>Fisherman</h1>
    </header>
    <main id="main">
      <aside id="sidebar">
        <nav id="menu">
          <ul>
            <li><a href="/dashboard">首页</a></li>
            <li><hr></li>
            <li><a href="/topics">话题</a></li>
            <li><a href="/topics/users">参与话题的用户</a></li>
            <li><a href="/topics/weibos">话题的相关微博</a></li>
            <li><hr></li>
            <li><a href="/reposts">被转发的微博</a></li>
            <li><a href="/reposts/users">参与转发的用户</a></li>
            <li><hr></li>
            <li><a href="/bigvs">大V</a></li>
            <li><a href="/bigvs/followers">大V 粉丝</a></li>
          </ul>
        </nav>
      </aside>
      <div id="content">
        {{!base}}
      </div>
    </main>
  </body>
</html>
