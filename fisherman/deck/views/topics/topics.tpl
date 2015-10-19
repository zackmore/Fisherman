% rebase('base.tpl')

<div class="container">
  <h1>话题列表</h1>
  <table class="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>话题</th>
        <th>上次抓取时间</th>
        <th>创建于</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      % for topic in topics:
        <tr>
          <td>{{topic.id}}</td>
          <td>{{topic.name}}</td>
          <td>{{topic.last_fetched_at}}</td>
          <td>{{topic.created_at}}</td>
          <td>
            <a href="#" class="btn btn-xs btn-primary">Fetch</a>
          </td>
        </tr>
      % end
    </tbody>
  </table>
</div>
