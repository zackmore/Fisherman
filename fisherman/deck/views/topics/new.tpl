% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">新的话题抓取</h1>
      <div class="pull-right"></div>
    </div>
  </div>
  <div class="row auto-overflow">
    <div class="col-xs-6">
      <form method="post">
        <div class="form-group">
          <label for="topic-name">新话题</label>
          <br>
          <input id="topic-name" name="topic-name" class="form-control" type="text" placeholder="格式：#要抓取的话题#" />
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
