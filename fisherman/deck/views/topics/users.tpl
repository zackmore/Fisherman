% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">话题—用户列表</h1>
      <div class="pull-right">
        % include('searchform.tpl')
      </div>
    </div>
  </div>
  <br>
  <div class="row">
      <div class="col-xs-12">
          <a href="/im?weibo_ids=" class="im btn btn-primary">统一私信</a>
      </div>
  </div>
  <br>
  <br>
  <div class="row auto-overflow">
    <div class="col-xs-12">
      <table class="table table-hover">
        <thead>
          <tr>
            <th><input type="checkbox">&nbsp;全选</th>
            <th>ID</th>
            <th>Weibo ID</th>
            <th>名字</th>
            <th>个人微博主页</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          % for user in users:
            <tr>
              <td><input type="checkbox" value="{{user.weibo_id}}"></td>
              <td>{{user.id}}</td>
              <td>{{user.weibo_id}}</td>
              <td><a target="_blank" href="{{user.link}}">{{user.name}}</a></td>
              <td><a target="_blank" href="{{user.link}}">{{user.link}}</a></td>
              <td>
                <a href="/im?weibo_ids={{user.weibo_id}}" class="btn btn-xs btn-primary">私信</a>
                <a href="/topics/weibos?user_id={{user.id}}" class="btn btn-xs btn-primary">相关微博</a>
              </td>
            </tr>
          % end
        </tbody>
      </table>
    </div>
  </div>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
