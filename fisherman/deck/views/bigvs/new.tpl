% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">新的大 V 粉丝抓取</h1>
      <div class="pull-right"></div>
    </div>
  </div>
  <div class="row auto-overflow">
    <div class="col-xs-6">
      <form method="post">
        <div class="form-group">
          <label for="weibo-id">大 V Weibo ID</label>
          <br>
          <input id="weibo-id" name="weibo-id" class="form-control" type="text" placeholder="格式：纯数字的 weibo id" />
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
