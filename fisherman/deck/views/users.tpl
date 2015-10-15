% rebase('base.tpl')

<div class="container">
  <h1>用户列表</h1>
  <table class="table table-hover">
    <thead>
      <tr>
        <th><input type="checkbox">(TODO)</th>
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
          <td><input type="checkbox"></td>
          <td>{{user.id}}</td>
          <td></td>
          <td>{{user.name}}</td>
          <td>{{user.link}}</td>
          <td></td>
        </tr>
      % end
    </tbody>
  </table>
</div>
