% rebase('base.tpl')

<div class="container">
  <h1>转发—用户列表</h1>
  <table class="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>Weibo ID</th>
        <th>名字</th>
        <th>个人微博主页</th>
        <th>来自于</th>
        <th>创建于</th>
      </tr>
    </thead>
    <tbody>
      % for user in users:
        <tr>
          <td>{{user.id}}</td>
          <td>{{user.weibo_id}}</td>
          <td>{{user.name}}</td>
          <td>{{user.link}}</td>
          <td>{{user.agent}}</td>
          <td>{{user.created_at}}</td>
        </tr>
      % end
    </tbody>
  </table>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
