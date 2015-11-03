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
  <div class="row auto-overflow">
    <div class="col-xs-12">
      <table class="table table-hover">
        <thead>
          <tr>
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
              <td>{{user.id}}</td>
              <td>{{user.weibo_id}}</td>
              <td><a target="_blank" href="{{user.link}}">{{user.name}}</a></td>
              <td><a target="_blank" href="{{user.link}}">{{user.link}}</a></td>
              <td></td>
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
