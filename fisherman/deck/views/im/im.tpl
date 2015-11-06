% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">私信</h1>
      <div class="pull-right"></div>
    </div>
  </div>
  <div class="row auto-overflow">
    <div class="col-xs-6">
      <form method="post" action="/pipeline/im">
        <div class="form-group">
          <label for="weibo-ids">Weibo ID</label>
          <br>
          % if weibo_ids:
            <input type="text" placeholder="用逗号分隔多个 weibo ID" class="form-control" value="{{weibo_ids}}" disabled>
            <input type="hidden" value="{{weibo_ids}}" name="weibo-ids">
          % else:
            <input type="text" placeholder="用逗号分隔多个 weibo ID" name="weibo-ids" class="form-control">
          % end
        </div>
        <div class="form-group">
          <label for="im-content">内容</label>
          <br>
          <textarea id="im-content" name="im-content" class="form-control" style="height: 340px"></textarea>
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
