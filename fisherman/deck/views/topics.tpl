% rebase('base.tpl')

<div class="container">
  <h1>话题列表</h1>
  <table class="table">
    <thead>
      <tr>
        <th>ID</th>
        <th>话题</th>
        <th>状态(TODO)</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      % for topic in topics:
        <tr>
          <td>{{topic.id}}</td>
          <td>{{topic.name}}</td>
          <td></td>
          <td></td>
        </tr>
      % end
    </tbody>
  </table>
</div>
