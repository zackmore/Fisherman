% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">新的转发微博抓取</h1>
      <div class="pull-right"></div>
    </div>
  </div>
  <div class="row auto-overflow">
    <div class="col-xs-6">
      <form method="post">
        <div class="form-group">
          <label for="weibo-url">新话题</label>
          <br>
          <input id="weibo-url" name="weibo-url" class="form-control" type="text" placeholder="格式：https://weibo.cn/repost/CEF36dVY7?uid=1810274375&rl=0" />
        </div>
        <br>
        <br>
        <div class="form-group">
          <button type="submit" class="btn btn-primary">提交</button>
        </div>
      </form>
    </div>
  </div>
</div>
