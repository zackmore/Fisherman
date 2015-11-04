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
      <h1>Fisherman | Deck</h1>
    </header>
    <main id="main">
      <aside id="sidebar">
        <nav id="menu">
          <ul>
            <li><a href="/dashboard">Dashboard</a></li>
            <li>
                <strong>Pelicans</strong>
                <ul>
                    <li><a href="/topics">话题列表</a></li>
                    <li><a href="/topics/users">话题用户</a></li>
                    <li><a href="/topics/weibos">话题微博</a></li>
                    <li><a href="/topics/new">话题 <span class="label label-success">new</span></a></li>
                    <li><hr></li>
                    <li><a href="/reposts">转发微博列表</a></li>
                    <li><a href="/reposts/users">转发用户</a></li>
                    <li><a href="/reposts/new">转发微博 <span class="label label-success">new</span></a></li>
                    <li><hr></li>
                    <li><a href="/bigvs">大 V 列表</a></li>
                    <li><a href="/bigvs/followers">大 V 粉丝</a></li>
                    <li><a href="/bigvs/new">大 V <span class="label label-success">new</span></a></li>
                </ul>
            </li>
            <li>
                <strong>Pipeline</strong>
                <ul>
                    <li></li>
                </ul>
            </li>
            <li>
                <strong>Settings</strong>
                <ul>
                    <li><a href="/settings/token">Token</a></li>
                </ul>
            </li>
          </ul>
        </nav>
      </aside>
      <div id="content">
        {{!base}}
      </div>
    </main>
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/main.js"></script>
  </body>
</html>
