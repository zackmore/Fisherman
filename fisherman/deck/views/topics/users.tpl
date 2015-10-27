% rebase('base.tpl')

<div class="container">
  <div class="row">
    <h1 class="pull-left">话题—用户列表</h1>
    <div class="pull-right">
      % include('searchform.tpl')
    </div>
  </div>
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
          <td>{{user.name}}</td>
          <td>{{user.link}}</td>
          <td></td>
        </tr>
      % end
    </tbody>
  </table>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
