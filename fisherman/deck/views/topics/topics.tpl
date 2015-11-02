% rebase('base.tpl')

<div class="container">
  <div class="row">
    <h1 class="pull-left">话题列表</h1>
    <div class="pull-right">
      % include('searchform.tpl')
    </div>
  </div>
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
            <a href="/fetch/topic/{{topic.id}}" class="btn btn-xs btn-primary fetch-topic">Fetch</a>
          </td>
        </tr>
      % end
    </tbody>
  </table>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
